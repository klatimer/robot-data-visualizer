"""
This file is the main viewing window of the application.
"""
import os
import sys
sys.path.append('..')

import warnings
warnings.filterwarnings("ignore")

from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.lines as lines
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

from tools.get_dates_umich import get_dates_umich
from tools.staticmap_for_gps import map_for_gps
from tools.data_manager import DataManager


class VisualizerFrame(tk.Frame):
    """
    This class represents the frame where the main visualization takes place.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label = None
        self.ax_map = None
        self.ax_gps = None
        self.map_plot = None
        self.gps_plot = None
        self.gps_on = False
        self.canvas = None
        self.data_manager = None
        self.gps_data = None
        self.gps_on = False
        self.map_on = False
        self.map_image = None
        self.widgets()

    def widgets(self):
        # Label for visualizer
        self.label = tk.Label(self, text="Viewer")
        self.label.pack(side=tk.TOP)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax_map = self.fig.add_subplot(111)
        self.ax_gps = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def callback_initialize_data_manager(self):
        # only setup a new dataset if this is the first load or the date has changed
        date = self.parent.toolbar.date.get()
        if self.data_manager is None:
            self.setup_data(date)
        else:
            if self.data_manager.date is not date:
                os.chdir('../..') # TODO patched here - add this to end of load_gps() / load_lidar() functions
                self.setup_data(date)
            else:
                pass

    def setup_data(self, date):
        if self.data_manager is not None:
            self.ax_map.clear()
            self.canvas.draw()
            self.gps_on = False
            self.map_on = False
        self.parent.set_status('DM_START', hold=True)
        self.data_manager = DataManager(date)
        self.data_manager.setup_data_files('sensor_data')
        self.data_manager.load_gps()
        x_coords, y_coords = map_for_gps(self.data_manager.data_dict, self.data_manager.data_dir)
        self.gps_data = [x_coords, y_coords] # in image coords
        self.map_image = mpimg.imread(os.path.join(self.data_manager.data_dir, 'map.png'))
        self.label.config(text='Viewer')
        self.parent.set_status('DM_READY')

    def callback_gps_on(self):
        if not self.gps_on:
            self.gps_on = True
            self.parent.set_status('GPS_START')
            idx = self.get_idx_for_gps_update()
            self.update_timestamp(idx)
            self.gps_plot = self.ax_gps.plot(self.gps_data[0][:idx], self.gps_data[1][:idx], 'r')[0]
            self.canvas.show()
            self.parent.set_status('GPS_READY')
        else:
            pass

    def callback_gps_off(self):
        if self.gps_on:
            self.gps_on = False
            self.update_gps(0)
            self.label.config(text='Viewer')
            self.parent.set_status('GPS_REMOVE')
        else:
            pass

    def callback_gps_slider_changed(self, event):
        self.gps_on = True
        idx = self.get_idx_for_gps_update()
        self.update_gps(idx)
        self.update_timestamp(idx)
        self.parent.set_status('GPS_UPDATE')

    def update_gps(self, idx):
        if self.gps_data is not None:
            self.gps_plot.set_xdata(self.gps_data[0][:idx])
            self.gps_plot.set_ydata(self.gps_data[1][:idx])
            self.canvas.draw()
        else:
            pass

    def update_timestamp(self, idx):
        curr_tstamp = self.get_timestamp_for_gps_update(idx)
        self.label.config(text=str('time stamp: ' + curr_tstamp))

    def get_idx_for_gps_update(self):
        slider_val = self.parent.control.gps_control.selection_scale.get()
        idx_ratio = len(self.gps_data[0]) / 100
        return int(slider_val * idx_ratio)

    def get_timestamp_for_gps_update(self, gps_data_idx):
        idx_ratio = len(self.data_manager.data_dict['gps']['tstamp']) / len(self.gps_data[0])
        idx = int(gps_data_idx * idx_ratio) - 1
        ts = int(self.data_manager.data_dict['gps']['tstamp'][idx] / 1000000)
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def callback_map_on(self):
        # Generate map and save in the correct data directory
        if not self.map_on:
            self.map_on = True
            if self.map_image is not None:
                self.ax_map.imshow(self.map_image)
                # draw scale on the map
                map_scale = self.get_map_scale()
                line = lines.Line2D([0, 200], [0, 0], linewidth=4, color='b')
                self.ax_map.add_line(line)
                distance = map_scale * 200
                if distance > 1000:
                    scale_str = "scale = " + str(float("%.2f" % (distance / 1000))) + " kilometers"
                else:
                    scale_str = "scale = " + str(float("%.2f" % (distance))) + " meters"
                self.ax_map.text(0, -10, scale_str, fontsize=8)
                self.canvas.draw()
                self.parent.set_status('MAP_READY')
            else:
                self.parent.set_status('MAP_ERROR')
        else:
            pass

    def callback_map_off(self):
        if self.map_on:
            self.map_on = False
            self.ax_map.clear()
            if self.gps_on:
                self.gps_on = False
                self.callback_gps_on() # because the previous line clears both map and gps
            self.canvas.draw()
        else:
            pass

    def callback_date_changed(self):
        new_date = self.parent.toolbar.date.get() # Need to call get() because this is a StringVar object
        if self.parent.toolbar.date is not new_date:
            self.parent.toolbar.date.set(new_date)
        else:
            pass

    def get_map_scale(self):
        k = 111000 # meters per degree of latitude (approx.)
        lat_range = self.data_manager.data_dict['gps_range'][0]
        d_lat_range = abs(lat_range[0] - lat_range[1])
        d_x_pixels = abs(max(self.gps_data[0]) - min(self.gps_data[0]))
        map_scale = d_lat_range * k / d_x_pixels
        return map_scale # units of meters per pixel


class ToolbarFrame(tk.Frame):
    """
    This class represents the toolbar at the top of the window.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.date = None
        self.dates = get_dates_umich()
        self.load_button = None
        self.option_menu = None
        self.widgets()

    def widgets(self):
        self.dates = get_dates_umich()
        self.load_button = tk.Button(self, text="Load Data")
        self.load_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.date = tk.StringVar(self)
        self.date.set(self.dates[24])
        self.option_menu = tk.OptionMenu(self, self.date, *self.dates, command=self.callback_date_changed)
        self.option_menu.pack(side=tk.LEFT, padx=2, pady=2)
        #print_button = tk.Button(self, text="Print")
        #print_button.pack(side=tk.LEFT, padx=2, pady=2)

    def bind_widgets(self):
        self.load_button.config(command=self.parent.window.callback_initialize_data_manager)

    def callback_date_changed(self, event):
        self.parent.window.callback_date_changed()

class ControlFrame(tk.Frame):
    """
    This class represents the controls on the right hand side of the main
    window. There are two nested classes for the slam and map controls.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400)
        self.parent = parent
        self.root = parent
        self.slam_control = None
        self.map_control = None
        self.widgets()

    class GpsControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.selection_scale = None
            self.scale_val = None
            self.on_button = None
            self.off_button = None
            self.widgets()

        def widgets(self):
            label = tk.Label(self, text="GPS Control", bg="blue", fg="white")
            label.pack(side=tk.TOP, fill=tk.X)

            self.selection_scale = tk.Scale(self, orient=tk.HORIZONTAL, to=100, variable=self.scale_val)
            self.selection_scale.set(100)
            self.selection_scale.pack(side=tk.TOP)

            self.on_button = tk.Button(self, text="On", bg="green", fg="white")
            self.on_button.pack(side=tk.LEFT)

            self.off_button = tk.Button(self, text="Off", bg="red", fg="white")
            self.off_button.pack(side=tk.RIGHT)

        def bind_widgets(self):
            self.on_button.config(command=self.root.window.callback_gps_on)
            self.off_button.config(command=self.root.window.callback_gps_off)
            self.selection_scale.bind("<ButtonRelease-1>", self.root.window.callback_gps_slider_changed)


    class MapControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.on_button = None
            self.off_button = None
            self.widgets()

        def widgets(self):
            label = tk.Label(self, text="Map Control", bg="blue", fg="white")
            label.pack(fill=tk.X)

            self.on_button = tk.Button(self, text="On", bg="green", fg="white")
            self.on_button.pack(side=tk.LEFT)

            self.off_button = tk.Button(self, text="Off", bg="red", fg="white")
            self.off_button.pack(side=tk.RIGHT)

        def bind_widgets(self):
            self.on_button.config(command=self.root.window.callback_map_on)
            self.off_button.config(command=self.root.window.callback_map_off)

    def widgets(self):
        self.gps_control = self.GpsControlFrame(self, self.root)
        self.gps_control.pack(fill=tk.X)
        self.map_control = self.MapControlFrame(self, self.root)
        self.map_control.pack(fill=tk.X)

    def bind_widgets(self):
        self.gps_control.bind_widgets()
        self.map_control.bind_widgets()


class MainWindow(tk.Tk):
    """
    This is the main window for the application. Here the main layout is
    established using a combination of the above classes and individual
    tkinter widgets.
    """

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.status_text = dict(READY="Ready",
                                DM_START="Initializing data manager ...",
                                DM_READY="Data is ready",
                                DM_NOT_READY="Data not loaded",
                                GPS_START="GPS loading ...",
                                GPS_READY="GPS is ready",
                                GPS_REMOVE="GPS removed",
                                GPS_UPDATE="GPS updated",
                                MAP_START="Map loading ...",
                                MAP_READY="Map is ready",
                                MAP_REMOVE="Map removed",
                                MAP_ERROR="Must load data before map can be displayed")
        self.STATUS_DELAY = 2000 # (ms) delay between status changes
        self.title("Robot Data Visualizer")
        self.mainWidgets()


    def mainWidgets(self):
        # Toolbar
        self.toolbar = ToolbarFrame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Status bar
        self.status = tk.Label(self, text=self.status_text['READY'], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Controls - SLAM and Map
        self.control = ControlFrame(self)
        self.control.pack(side=tk.RIGHT, fill=tk.Y)

        # Main viewing window
        self.window = VisualizerFrame(self)
        self.window.pack(side=tk.LEFT, padx=2, pady=2)

        # Bind widgets to their callback functions
        self.toolbar.bind_widgets()
        self.control.bind_widgets()


    def set_status(self, status, hold=False):
        if status in self.status_text.keys():
            self.status.config(text=self.status_text[status])
            if not hold:
                self.status.after(self.STATUS_DELAY, lambda: self.status.config(text=self.status_text['READY']))
        else:
            self.status.config(text=str(status))


if __name__ == '__main__':
    app = MainWindow(None)
    app.mainloop()

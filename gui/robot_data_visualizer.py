"""
This file is the main viewing window of the application.
"""
import os
import sys
sys.path.append('..')

import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

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
        self.canvas = None
        self.data_manager = None
        self.gps_data = None
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
                os.chdir('../..') # patch for now - add this to end of load_gps() / load_lidar() functions
                self.setup_data(date)
            else:
                pass

    def setup_data(self, date):
        self.parent.set_status('DM_START', hold=True)
        self.data_manager = DataManager(date)
        self.data_manager.setup_data_files('sensor_data')
        self.data_manager.load_gps()
        x_coords, y_coords = map_for_gps(self.data_manager.data_dict, self.data_manager.data_dir)
        self.gps_data = [x_coords, y_coords]
        self.parent.set_status('DM_READY')

    def callback_gps_on(self):
        self.parent.set_status('GPS_START')
        idx = self.get_idx_for_gps_update()
        self.gps_plot = self.ax_gps.plot(self.gps_data[0][:idx], self.gps_data[1][:idx], 'r')[0]
        self.canvas.show()
        self.parent.set_status('GPS_READY')

    def callback_gps_off(self):
        self.update_gps(0)
        self.parent.set_status('GPS_REMOVE')

    def callback_gps_slider_changed(self, event):
        self.update_gps(self.get_idx_for_gps_update())
        self.parent.set_status('GPS_UPDATE')

    def update_gps(self, idx):
        if self.gps_data is not None:
            self.gps_plot.set_xdata(self.gps_data[0][:idx])
            self.gps_plot.set_ydata(self.gps_data[1][:idx])
            self.canvas.draw()
        else:
            pass

    def get_idx_for_gps_update(self):
        slider_val = self.parent.control.gps_control.selection_scale.get()
        idx_ratio = len(self.gps_data[0]) / 100
        return int(slider_val * idx_ratio)

    def callback_map_on(self):
        # Generate map and save in the correct data directory
        map_for_gps(self.data_manager.data_dict, self.data_manager.data_dir)
        im = mpimg.imread(os.path.join(self.data_manager.data_dir, 'map.png'))
        self.ax_map.imshow(im)
        self.canvas.draw()
        self.parent.set_status('MAP_READY')

    def callback_map_off(self):
        self.ax_map.clear()
        self.canvas.draw()

    def callback_date_changed(self):
        new_date = self.parent.toolbar.date.get() # Need to call get() because this is a StringVar object
        if self.parent.toolbar.date is not new_date:
            self.parent.toolbar.date.set(new_date)
            # self.callback_initialize_data_manager(new_date)
        else:
            pass


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
                                MAP_REMOVE="Map removed")
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

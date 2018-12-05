"""
This file is the main viewing window of the application.
"""
import os
import sys
sys.path.append('..')

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

import tkinter as tk

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
        self.canvas = None
        self.data_manager = None
        self.widgets()

    def widgets(self):
        # Label for visualizer
        self.label = tk.Label(self, text="Viewer")
        self.label.pack(side=tk.TOP)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.a = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)

    def callback_initialize_data_manager(self):
        if self.data_manager is None:
            self.parent.set_status('DM_START', hold=True)
            self.data_manager = DataManager('2013-01-10')
            self.data_manager.setup_data_files('sensor_data')
            self.data_manager.load_gps()
        else:
            pass
        self.parent.set_status('DM_END')

    def load_map(self):
        # Generate map and save in the correct data directory
        self.parent.set_status('MAP_START', hold=True)
        data_dir = self.data_manager.data_dir
        data_dict = self.data_manager.data_dict
        map_for_gps(data_dict, data_dir)
        im = mpimg.imread(os.path.join(data_dir, 'map.png'))
        self.a.imshow(im)
        self.canvas.draw()
        self.parent.set_status('MAP_END')

    def on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas)


class ToolbarFrame(tk.Frame):
    """
    This class represents the toolbar at the top of the window.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.insert_button = None
        self.widgets()

    def widgets(self):
        self.insert_button = tk.Button(self, text="Load Data")
        self.insert_button.pack(side=tk.LEFT, padx=2, pady=2)

        print_button = tk.Button(self, text="Print", command=self.do_nothing)
        print_button.pack(side=tk.LEFT, padx=2, pady=2)

    def bind_widgets(self):
        self.insert_button.config(command=self.parent.window.callback_initialize_data_manager)

    def do_nothing(self):
        print("Ok, ok, I won't ...")


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

    class SlamControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.widgets()

        def widgets(self):
            label = tk.Label(self, text="SLAM Control", bg="blue", fg="white")
            label.pack(side=tk.TOP, fill=tk.X)

            speed_scale = tk.Scale(self, orient=tk.HORIZONTAL)
            speed_scale.pack(side=tk.TOP)

            show_its_button = tk.Checkbutton(self, text="show iterations")
            show_its_button.pack(side=tk.TOP)

            run_button = tk.Button(self, text="Run", bg="green", fg="white")
            run_button.pack(side=tk.LEFT)

            stop_button = tk.Button(self, text="Stop", bg="red", fg="white")
            stop_button.pack(side=tk.RIGHT)


    class MapControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.widgets()

        def load_map(self):
            self.root.window.load_map()

        def widgets(self):
            label = tk.Label(self, text="Map Control", bg="blue", fg="white")
            label.pack(fill=tk.X)

            on_button = tk.Button(self, text="On", bg="green", fg="white", command=self.load_map)
            on_button.pack(side=tk.LEFT)

            off_button = tk.Button(self, text="Off", bg="red", fg="white")
            off_button.pack(side=tk.RIGHT)

    def widgets(self):
        self.slam_control = self.SlamControlFrame(self, self.root)
        self.slam_control.pack(fill=tk.X)
        self.map_control = self.MapControlFrame(self, self.root)
        self.map_control.pack(fill=tk.X)


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
                                DM_START="Initializing ...",
                                DM_END="Data is ready",
                                DM_NOT_READY="Data not loaded",
                                MAP_START="Map loading ...",
                                MAP_END="Map is ready")
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


    def set_status(self, status, hold=False):
        if status in self.status_text.keys():
            self.status.config(text=self.status_text[status])
            if not hold:
                self.status.after(self.STATUS_DELAY, lambda: self.status.config(text=self.status_text['READY']))
        else:
            self.status.config(text=self.status_text['READY'])


if __name__ == '__main__':
    app = MainWindow(None)
    app.mainloop()

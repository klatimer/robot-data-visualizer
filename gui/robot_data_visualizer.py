"""
This file is the main viewing window of the application.
"""
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

from numpy import arange, sin, pi

import tkinter as tk


class VisualizerFrame(tk.Frame):
    """
    This class represents the frame where the main visualization takes place.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label = None
        self.canvas = None
        self.widgets()

    def widgets(self):
        # Label for visualizer
        self.label = tk.Label(self, text="Viewer")
        self.label.pack(side=tk.TOP)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.a = self.fig.add_subplot(111)
        """
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        a.plot(t, s)
        """

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)

    def load_map(self):
        print('Loading map ...')
        im = mpimg.imread('../data/2013-01-10/umich.png')
        self.a.imshow(im)
        self.canvas.draw()

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
        self.widgets()

    def widgets(self):
        insert_button = tk.Button(self, text="Insert Image", command=self.do_nothing)
        insert_button.pack(side=tk.LEFT, padx=2, pady=2)

        print_button = tk.Button(self, text="Print", command=self.do_nothing)
        print_button.pack(side=tk.LEFT, padx=2, pady=2)

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
                                DM_START="Data Manager Initializing ...",
                                DM_END="Data Manager loaded data")
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


    def set_status(self, status):
        if status in self.status_text.keys():
            self.status.config(text=status)
        else:
            self.status.config(text=self.status_text['READY'])


if __name__ == '__main__':
    app = MainWindow(None)
    app.mainloop()

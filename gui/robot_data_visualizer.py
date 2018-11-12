"""
This file is the main viewing window of the application.
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

from numpy import arange, sin, pi

import tkinter as tk


class VisualizerFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.canvas = None
        self.widgets()

    def widgets(self):
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        a.plot(t, s)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)

        # Label for visualizer
        self.label = tk.Label(self, text="Viewer")
        self.label.pack()

    def on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas)


class ToolbarFrame(tk.Frame):
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

class SlamControl(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400)
        self.parent = parent
        self.widgets()

    def widgets(self):
        label = tk.Label(self, text="SLAM Control Frame", bg="red", fg="white")
        label.pack(fill=tk.X)


# Main window for the application
class MainWindow(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.title("Robot Data Visualizer")
        self.mainWidgets()

    def mainWidgets(self):
        self.toolbar = ToolbarFrame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Status bar
        self.status = tk.Label(self, text="Preparing to do nothing", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Controls for running the SLAM algorithm
        self.control = SlamControl(self)
        self.control.pack(side=tk.RIGHT, fill=tk.Y)

        # Main viewing window
        self.window = VisualizerFrame(self)
        self.window.pack(side=tk.LEFT)


if __name__ == '__main__':
    app = MainWindow(None)
    app.mainloop()

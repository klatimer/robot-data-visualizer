"""
This file is the main viewing window of the application.
"""
import tkinter as tk

from numpy import arange, sin, pi

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler


class RobotDataVisualizer(tk.Frame):


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Robot Data Visualizer")
        self.create_widgets()

    def create_widgets(self):

        self.label = tk.Label(self.master, text="This is a label")
        self.label.pack()

        self.greet_button = tk.Button(self.master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy)

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        a.plot(t, s)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)


    def on_key_event(self, event):

        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas)


    def greet(self):

        print("Greetings!")



if __name__ == '__main__':
    root = tk.Tk()
    gui = RobotDataVisualizer(master=root)
    root.mainloop()

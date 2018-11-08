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


class RobotDataVisualizer(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Robot Data Visualizer")
        self.canvas  = None
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.master, text="This is a label")
        label.pack()

        greet_button = tk.Button(self.master, text="Greet", command=self.greet)
        greet_button.pack()

        close_button = tk.Button(self.master, text="Close", command=self.master.destroy)
        close_button.pack()

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        a.plot(t, s)

        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.mpl_connect('key_press_event', self.on_key_event)
        self.canvas = canvas

    def on_key_event(self, event):

        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas)


    def greet(self):

        print("Greetings!")


if __name__ == '__main__':
    root = tk.Tk()
    gui = RobotDataVisualizer(master=root)
    root.mainloop()

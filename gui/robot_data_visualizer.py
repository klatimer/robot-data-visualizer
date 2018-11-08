"""
This file is the main viewing window of the application.
"""
from tkinter import *

class RobotDataVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Robot Data Visualizer")

        self.label = Label(master, text="This is a label")
        self.label.pack()

        # greet is the "event handler" function for the button press
        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)

        """
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 2, 8, 7, 1, 9, 8])
        canvas = FigureCanvasTkAgg(f, )
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        """

    def greet(self ):
        print("Greetings!")


if __name__ == '__main__':
    root = Tk()
    gui = RobotDataVisualizer(root)
    root.mainloop()
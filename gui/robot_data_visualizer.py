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

    def greet(self ):
        print("Greetings!")


if __name__ == '__main__':
    root = Tk()
    gui = RobotDataVisualizer(root)
    root.mainloop()
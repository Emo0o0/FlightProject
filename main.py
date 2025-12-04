import tkinter as tk

from Flight_Project.ui_elems.app import FlightBookingSystem

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()

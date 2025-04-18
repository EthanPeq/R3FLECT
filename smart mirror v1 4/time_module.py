from tkinter import Label
from time import strftime

class TimeModule:
    def __init__(self):
        self.time_label = Label(font=("Helvetica", 24), fg="white", bg="black")

    def update_time(self):
        """Update the time every minute (no seconds) in 12-hour format with AM/PM."""
        current_time = strftime('%I:%M %p')  # Format the time (12-hour format with AM/PM)
        self.time_label.config(text=current_time)
        self.time_label.after(60000, self.update_time)  # Update every minute

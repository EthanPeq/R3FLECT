import threading
import time
from tkinter import Tk
from vision_state import VisionState
from controllers.face_recognition_controller import FaceRecognition
from controllers.gesture_controller import GestureControl
from camera_stream import SharedCamera
from widgets.weather_module import WeatherModule
from tkinter import Label
from tkinter import Frame, Label
from time_module import TimeModule
from widgets.skincare_module import SkincareModule


def update_name_callback(name):
    print(f"User: {name}")
    app.update_greeting(name)


class SmartMirrorApp:
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='black')
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.config(cursor="none")

        # Initialize vision state, camera, face recognition, and gesture controllers
        self.vision_state = VisionState()
        self.shared_camera = SharedCamera()
        self.face_recognition_controller = FaceRecognition(self.vision_state, update_name_callback)
        self.gesture_control_controller = GestureControl(self.vision_state, self.handle_gesture)
        threading.Thread(       # face recognition thread
            target=self.face_recognition_controller.start,
            args=(self.shared_camera,),
            daemon=True
        ).start()
        threading.Thread(       # gesture control thread
            target=self.gesture_control_controller.start, 
            args=(self.shared_camera,), 
            daemon=True
        ).start()

        # Greeting Label (top-left)
        self.greeting_label = Label(self.root, text="R3FLECT", font=("Helvetica", 24), fg="white", bg="black")
        self.greeting_label.place(relx=0.0, rely=0.0, anchor="nw", x=20, y=20)

        # Time setup
        self.time_module = TimeModule()
        self.time_module.update_time()
        self.time_module.time_label.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Reduced vertical padding for time label

        # Widget container setup
        self.widget_container = Frame(self.root, bg='black', bd=2, relief="solid")
        self.widget_container.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=70)


        # Weather module has two separate pages/widgets
        self.weather_module = WeatherModule(self.widget_container, update_callback=self.update_widget)
        self.weather_module.create_widget()
        #self.weather_module.frame.pack(fill="both", expand=True)

        ## Skincare module setup
        self.skincare_module = SkincareModule(self.widget_container, update_callback=self.update_widget)
        self.skincare_module.create_widget()
        #self.skincare_module.frame.pack()

        # List of pages (can be frames, widgets, etc.)
        self.pages = [
            self.weather_module.current_weather_frame,
            self.weather_module.forecast_frame,
            self.skincare_module.frame
        ]

        self.current_page_index = 0
        self.show_current_page()

        # Create dots indicator for page navigation
        self.create_dots_indicator()


        # Gesture label setup
        self.gesture_label = Label(self.root, text=" ", font=("Helvetica", 16), fg="white", bg="black")
        self.gesture_label.pack(pady=10)

        # Gesture Timeout
        self.last_gesture_time = 0

        # Start gesture status updates
        self.update_gesture_status()

    def update_greeting(self, name):
        if name:
            self.greeting_label.config(text=f"Hello, {name}")
        else:
            self.greeting_label.config(text="R3FLECT")

        self.update_visible_pages(name)

        # Start weather updates only for recognized users
        if name in ["Ethan", "Melina"]:
            self.weather_module.start_weather_updates()

    
    def update_widget(self, widget_type, data):
        """Update the UI with new weather data"""
        if widget_type == 'weather_data':
            self.weather_module.update_current_weather(data)  # Update the current weather widget
            self.skincare_module.update_widget(data)  # Update the skincare routine widget
        elif widget_type == 'forecast_data':
            self.weather_module.display_forecast(data)  # Update the forecast widget

    
    def update_visible_pages(self, name):
        """Update which pages should be visible based on the user's name."""
        # Hide everything first
        for page in self.pages:
            page.pack_forget()

        if name == "Ethan":
            self.pages = [
                self.weather_module.forecast_frame,
                self.weather_module.current_weather_frame,
                self.skincare_module.frame
            ]
            self.weather_module.frame.pack(fill="both", expand=True)
            self.skincare_module.frame.pack(fill="both", expand=True)


        elif name == "Melina":
            self.pages = [
                self.weather_module.current_weather_frame,
                self.weather_module.forecast_frame
            ]
            self.weather_module.frame.pack(fill="both", expand=True)

        else:
            self.pages = []

        self.current_page_index = 0
        self.show_current_page()
        self.create_dots_indicator()



    def handle_gesture(self, direction):
        if direction == "left":
            self.prev_page(None)
        elif direction == "right":
            self.next_page(None)

    def update_gesture_status(self):
        gesture_status = self.vision_state.swipe_mode_active

        if gesture_status:
            self.last_gesture_time = time.time()  # Update the last seen time
            self.gesture_label.config(text="Gesture: Active")
        else:
            if time.time() - self.last_gesture_time > 1.0:  # 1 second passed
                self.gesture_label.config(text=" ")

        self.gesture_label.after(500, self.update_gesture_status)

    def create_dots_indicator(self):
        # Clear old dots if re-creating (for switching users)
        if hasattr(self, 'dots_frame'):
            self.dots_frame.destroy()

        self.dots_frame = Frame(self.root, bg='black')
        self.dots_frame.pack(pady=10)

        self.dots = []
        num_pages = len(self.pages)

        for _ in range(num_pages):
            dot = Label(self.dots_frame, width=2, height=1, bg='gray', relief="flat")
            dot.pack(side="left", padx=5)
            self.dots.append(dot)

        self.update_dots_indicator()



    def update_dots_indicator(self):
        # Reset all dots to default size and color
        for i, dot in enumerate(self.dots):
            dot.config(width=2, height=1)  # Smaller size for inactive dots
            dot.config(bg='gray')  # Default color for inactive dots

        # Ensure the current page index is valid
        if 0 <= self.current_page_index < len(self.dots):
            active_dot = self.dots[self.current_page_index]
            active_dot.config(width=4, height=2)  # Larger size for the active dot
            active_dot.config(bg='blue')  # Change color for active dot



    def show_current_page(self):
        # Avoid crashing if pages list is empty
        if not self.pages:
            return
        
        # Hide all pages
        for page in self.pages:
            page.pack_forget()
        
        # Get the current page
        current_page = self.pages[self.current_page_index]
        # Pack the current page consistently
        current_page.pack(fill="both", expand=False)
        
        # Force layout update
        self.widget_container.update_idletasks()

    def next_page(self, _event):
        if not self.pages:
            return
        
        # Move to the next page, but don't wrap around
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.show_current_page()
            self.update_dots_indicator() 
            
    def prev_page(self, _event):
        if not self.pages:
            return
        
        # Move to the previous page, but don't wrap around
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.show_current_page()
            self.update_dots_indicator()
            

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SmartMirrorApp()
    app.run()



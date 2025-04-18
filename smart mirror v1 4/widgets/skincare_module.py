from tkinter import Frame, Label
from datetime import datetime
from widgets.base_widget import BaseWidget

class SkincareModule(BaseWidget):
    def __init__(self, root, update_callback=None):
        super().__init__(root)
        self.update_callback = update_callback  # Store the callback function

    def create_widget(self):
        """Create the skincare routine widget UI"""
        self.frame = Frame(self.root, bg='black')

        self.skincare_label = Label(
            self.frame,
            text='Temp',
            font=('Helvetica', 18),
            fg='white',
            bg='black',
            justify="left",
            wraplength=300,  # Wrap text at 300
            anchor="ne"      # Align text to top-left
        )
        self.skincare_label.pack(padx=20, pady=10, fill="both", expand=True)


    def update_widget(self, weather_data):
        """
        Update skincare routine based on weather data
        :param weather_data: dict with keys: temp (°F), humidity (%), description (str)
        """
        temp = weather_data.get('temp')
        humidity = weather_data.get('humidity')
        description = weather_data.get('description', "")

        # Update skincare routine based on the weather data
        self.update_skincare_routine(temp, humidity, description)

    def update_skincare_routine(self, temperature, humidity, description):
        """Update skincare label with dynamic routine"""

       # if temperature is None:
       #     temperature = 70  # Default temperature in case of None
       # if humidity is None:
       #     humidity = 50  # Default humidity in case of None


        now = datetime.now()
        hour = now.hour
        day_of_month = now.day

        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 18 <= hour <= 23 or 0 <= hour < 2:
            time_of_day = "night"
        else:
            time_of_day = "none"

        routine_text = f"Skincare Routine ({time_of_day.title()}):\n"

        if time_of_day == "morning":
            routine_text += "1. Cleanser"

            if humidity > 80:
                routine_text += "\n2. Oil-control moisturizer"
            elif humidity < 30:
                routine_text += "\n2. Hydrating mist or serum"

            if temperature < 50:
                routine_text += "\n3. Rich hydrating serum (cold weather)"
                routine_text += "\n4. Lotion"
            elif 50 <= temperature < 85:
                routine_text += "\n3. Lotion"

            if "rain" in description.lower():
                routine_text += "\n5. Water-resistant sunscreen"
            elif "sun" in description.lower():
                routine_text += "\n5. Broad-spectrum sunscreen"

        elif time_of_day == "night":
            routine_text += "1. Cleanser"

            if day_of_month % 2 == 0:
                routine_text += "\n2. Exfoliate"
            else:
                routine_text += "\n2. (Skip exfoliation today)"

            routine_text += "\n3. Retinoid"

            if humidity > 80:
                routine_text += "\n4. Oil-control moisturizer"
                if temperature < 50:
                    routine_text += "\n5. Heavy Moisturizer"
            elif humidity < 30:
                routine_text += "\n4. Hydrating mist or serum"
                routine_text += "\n5. Heavy Moisturizer"
            else:
                routine_text += "\n4. Heavy Moisturizer"

        else:
            routine_text += "No routine scheduled for this time."

        self.skincare_label.config(text=routine_text)

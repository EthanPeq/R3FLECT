import requests
from tkinter import Frame, Label
from datetime import datetime
from widgets.base_widget import BaseWidget
from PIL import Image, ImageTk
import io

class WeatherModule(BaseWidget):
    def __init__(self, root, update_callback):
        super().__init__(root)
        self.update_callback = update_callback
        self.api_key = 'your_api_key'  # Securely store your API key
        self.lat = 39.1031  # Cincinnati latitude
        self.lon = -84.5120  # Cincinnati longitude

    def create_widget(self):
        """Create both current weather and forecast widget UI"""
        self.frame = Frame(self.root, bg='black')

        # Current weather
        self.current_weather_frame = Frame(self.frame, bg='black')
        self.current_weather_frame.pack()

        self.current_weather_label = Label(
            self.current_weather_frame,
            text="Loading...",
            font=('Helvetica', 18),
            fg='white',
            bg='black'
        )
        self.current_weather_label.pack()

        # Forecast section
        self.forecast_frame = Frame(self.frame, bg='black')
        self.forecast_frame.pack()

    def update_widget(self, weather_data):
        """Update the widget UI with weather data"""
        if isinstance(weather_data, dict):  # Current weather data
            self.update_current_weather(weather_data)
        elif isinstance(weather_data, list):  # Forecast data
            self.display_forecast(weather_data)

    def update_current_weather(self, weather_data):
        """Update current weather widget"""
        weather_text = f"Weather: {weather_data['temp']}°F, {weather_data['description']}"
        self.current_weather_label.config(text=weather_text)

    def display_forecast(self, forecast_data):
        """ Display forecast in a row with images and text """

        # Clear previous forecast
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        if not forecast_data:
            Label(
                self.forecast_frame,
                text="Forecast data unavailable",
                font=('Helvetica', 18),
                fg='white',
                bg='black'
            ).pack()
            return

        for index, entry in enumerate(forecast_data):
            day = entry['day']
            temp = entry['temp']
            desc = entry['description']
            icon_url = entry.get('icon_url', '')  # default to blank

            frame = Frame(self.forecast_frame, bg='black', padx=10, pady=10)
            frame.grid(row=0, column=index, sticky="n")

            # Fetch and display icon
            try:
                img_response = requests.get(icon_url, timeout=3)
                img_data = Image.open(io.BytesIO(img_response.content))
                img_data = img_data.resize((45, 45), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img_data)
                icon_label = Label(frame, image=icon, bg='black')
                icon_label.image = icon
                icon_label.pack()
            except Exception as e:
                print(f"Failed to load icon: {e}")

            Label(frame, text=day, font=('Helvetica', 12), fg='white', bg='black').pack()
            Label(frame, text=f"{temp:.1f}°F", font=('Helvetica', 12), fg='white', bg='black').pack()
            Label(frame, text=desc, font=('Helvetica', 12), fg='white', bg='black', wraplength=100).pack()

    def fetch_weather_data(self):
        """Fetch current weather data"""
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&units=imperial&appid={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('cod') == 200:
                weather_data = {
                    'temp': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'].capitalize()
                }
                self.update_callback('weather_data', weather_data)
            else:
                print(f"Error fetching weather data: {data.get('message')}")
        except Exception as e:
            print(f"Error: {e}")

    def fetch_forecast_data(self):
        """Fetch 5-day forecast data"""
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&units=imperial&appid={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('cod') == '200':
                forecast_data = []
                seen_dates = set()
                for entry in data['list']:
                    date = datetime.utcfromtimestamp(entry['dt']).strftime('%A')
                    if date not in seen_dates:
                        seen_dates.add(date)
                        temp = entry['main']['temp']
                        description = entry['weather'][0]['description'].capitalize()
                        icon_code = entry['weather'][0]['icon']
                        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                        forecast_data.append({
                            'day': date,
                            'temp': temp,
                            'description': description,
                            'icon_url': icon_url
                        })
                        if len(forecast_data) >= 5:
                            break
                self.update_callback('forecast_data', forecast_data)
            else:
                print(f"Error fetching forecast data: {data.get('message')}")
        except Exception as e:
            print(f"Error: {e}")

    def start_weather_updates(self):
        """Start fetching weather data periodically"""
        self.fetch_weather_data()
        self.fetch_forecast_data()

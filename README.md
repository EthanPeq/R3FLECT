# R3FLECT
R3FLECT is a modular smart mirror built for Raspberry Pi. It features face recognition, gesture control, real-time weather, and a dynamic skincare routine. Developed as a capstone in AI, it combines computer vision, IoT, and personalized user experiences.

-  Face recognition
-  Gesture controls (via OpenCV + Mediapipe)
-  Real-time weather updates
-  Dynamic skincare recommendations based on environmental data
-  Always-on time and greeting display
-  Scrollable UI pages for weather, skincare, and more

## Tech Stack

- Python 3
- OpenCV
- Mediapipe
- Dlib / face_recognition
- OpenWeatherMap API
- Raspberry Pi OS
- Tkinter (or your chosen UI library)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/r3flect.git
   cd r3flect

2. Get an OpenWeatherMAP API key:
   - Sign up at https://openweathermap.org/api
   - In widgets/weather_module change this WEATHER_API_KEY=your_api_key_here
  
3. Run the smart mirror:
   python main.py

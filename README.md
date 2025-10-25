====================================
        REAL-TIME WEATHER APP
====================================

PROJECT OVERVIEW:
-----------------
This is a simple Python-based web application that displays
real-time weather information and a 5-day forecast for any city
using the OpenWeatherMap API.

The app is built with Streamlit for the interface, and uses
Requests, Pandas, and Matplotlib for data handling and visualization.

------------------------------------
FEATURES:
------------------------------------
1. Enter any city name to view live weather data
2. Displays temperature, humidity, wind speed, sunrise/sunset
3. 5-day forecast with a temperature chart
4. Dynamic weather icons (sunny, cloudy, rainy, etc.)
5. Toggle between Celsius (°C) and Fahrenheit (°F)

------------------------------------
TOOLS AND TECHNOLOGIES USED:
------------------------------------
- Python 3.8 or higher
- Streamlit
- Requests
- Pandas
- Matplotlib
- OpenWeatherMap API

------------------------------------
INSTALLATION STEPS:
------------------------------------
1. Install Python 3.8 or higher (https://www.python.org/downloads)
   During installation, check the box “Add Python to PATH”.

2. Install required libraries using the terminal or command prompt:
   pip install streamlit requests pandas matplotlib pytz

3. Download the file "weather_app.py" and place it in a folder.

4. Get a free API key from:
   https://openweathermap.org/api
   (Sign up → My API Keys → Copy the key)

5. Open the file "weather_app.py" in a text editor.
   Replace the line:
       API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
   with your actual API key, for example:
       API_KEY = "abcd1234efgh5678ijkl"

6. Save the file.

------------------------------------
RUNNING THE APP:
------------------------------------
1. Open Command Prompt (Windows) or Terminal (Mac/Linux).

2. Navigate to the folder where weather_app.py is saved:
   Example:
   cd C:\Users\YourName\Desktop

3. Run the following command:
   python -m streamlit run weather_app.py

4. The app will open automatically in your default browser.
   If it doesn’t, go to:
   http://localhost:8501

------------------------------------
USAGE:
------------------------------------
- Enter the name of any city (e.g., Mumbai, London, Tokyo).
- Choose units (Celsius or Fahrenheit).
- View:
  * Current temperature
  * Humidity and wind speed
  * Sunrise and sunset times
  * Dynamic weather icon
  * 5-day forecast chart

------------------------------------
TROUBLESHOOTING:
------------------------------------
1. ERROR: 'streamlit not recognized'
   → Use:
       python -m pip install streamlit

2. ERROR: 'HTTP 401 Unauthorized'
   → Your API key is invalid or inactive.
     Check your key on:
       https://home.openweathermap.org/api_keys
     Or wait up to 1 hour for activation.

3. App doesn’t open automatically
   → Manually open your browser and visit:
       http://localhost:8501

------------------------------------
SAMPLE CITIES TO TRY:
------------------------------------
- Mumbai
- New York
- London
- Tokyo
- Sydney

------------------------------------
PROJECT FILES:
------------------------------------
- weather_app.py   → main Python app
- README.txt       → project documentation

------------------------------------
AUTHOR:
------------------------------------
Developed by: [M.V.Pavan Kumar]
Built with: Python + Streamlit
Data Source: OpenWeatherMap API
------------------------------------


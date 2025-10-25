# Real-Time-Weather-App
The Real-Time Weather App is a Python-based web application built with Streamlit. It provides current weather updates and a 5-day forecast for any city worldwide using the OpenWeatherMap API. Users can see temperature, humidity, wind speed, sunrise/sunset times, and dynamic weather icons. It also allows toggling between Celsius and Fahrenheit, making it easy to access real-time weather information in a clean and interactive interface.

⚙️ Features

Search weather by any city name

Display current temperature, humidity, wind speed, and weather description

Show sunrise and sunset times for the selected city

Toggle between Celsius and Fahrenheit

View 5-day weather forecast in a simple chart

Dynamic icons based on current weather conditions

Clean, responsive, and easy-to-use interface

🧰 Technologies Used

Python 3

Streamlit (Frontend UI)

Requests (API requests)

OpenWeatherMap API (Real-time weather data)

Plotly / Matplotlib (Forecast chart visualization)

🚀 Step-by-Step Installation & Usage Guide
1️⃣ Clone the Repository

Open your terminal (or command prompt) and run:

git clone <your-repo-link>
cd real-time-weather-app

2️⃣ Install Required Packages

Install Streamlit and other dependencies:

python -m pip install streamlit requests matplotlib plotly

3️⃣ Run the Weather App

Start the app using Streamlit:

python -m streamlit run weatherapp.py

4️⃣ Open the App in Your Browser

Once the app starts, it will automatically open a browser window at:
http://localhost:8501

If it doesn’t open automatically, copy the URL into your browser.

5️⃣ Using the App

Enter the city name in the input box.

Click Submit or press Enter.

View current weather details: temperature, humidity, wind speed, sunrise, and sunset times.

Toggle Celsius/Fahrenheit as needed.

Scroll down to see the 5-day forecast chart and dynamic weather icons.

6️⃣ Check Streamlit Version (Optional)

To verify your Streamlit installation:

python -m streamlit --version

🎯 Objective

To create an easy-to-use, interactive dashboard that provides real-time weather updates and a 5-day forecast, helping users access accurate weather information for any city quickly and efficiently.

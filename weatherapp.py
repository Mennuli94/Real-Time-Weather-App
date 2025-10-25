"""
Real-Time Weather App (Streamlit)
- Shows current weather + 5-day forecast for any city using OpenWeatherMap
- Features:
  * City input
  * Unit toggle (Celsius / Fahrenheit)
  * Current temp, humidity, sunrise/sunset (local times)
  * 5-day forecast chart (aggregated per-day)
  * Dynamic icons (OpenWeatherMap icons + simple emoji fallback)
  * Basic error handling & caching

Requirements:
pip install streamlit requests pandas matplotlib pytz
Run:
streamlit run weather_app.py
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz

# -----------------------
# Config - put your API key here
# -----------------------
# Get a free API key from: https://openweathermap.org/api
API_KEY = "6ad7041e1f1203e8049d10d481cf5756"  # <-- replace with your key

# -----------------------
# Helpers / caching
# -----------------------
BASE_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

@st.cache_data(ttl=300)
def fetch_current_weather(city: str, units: str):
    params = {"q": city, "appid": API_KEY, "units": units}
    r = requests.get(BASE_CURRENT, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=300)
def fetch_forecast(city: str, units: str):
    params = {"q": city, "appid": API_KEY, "units": units}
    r = requests.get(BASE_FORECAST, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def icon_url(icon_code: str) -> str:
    # OpenWeatherMap icon URL
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def emoji_for_weather(main: str) -> str:
    # Simple mapping for visual fallback
    m = main.lower()
    if "cloud" in m: return "☁"
    if "rain" in m or "drizzle" in m: return "🌧"
    if "thunder" in m: return "⛈"
    if "snow" in m: return "❄"
    if "clear" in m: return "☀"
    if "mist" in m or "fog" in m or "haze" in m: return "🌫"
    return "🌡"

def to_local_time(utc_ts: int, tz_offset_seconds: int):
    # Convert UTC timestamp (seconds) + timezone offset to a naive local datetime
    # Return human-friendly string.
    utc = datetime.utcfromtimestamp(utc_ts)
    local = utc + timedelta(seconds=tz_offset_seconds)
    return local.strftime("%Y-%m-%d %H:%M:%S")

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Real-Time Weather App", page_icon="🌤", layout="centered")
st.title("🌤 Real-Time Weather App")
st.caption("Displays current weather and 5-day forecast using OpenWeatherMap")

# Sidebar for API key (optional override) and sample queries
with st.sidebar:
    st.header("Settings")
    api_input = st.text_input("OpenWeatherMap API Key (optional)", value=API_KEY if API_KEY != "YOUR_OPENWEATHERMAP_API_KEY" else "")
    if api_input:
        st.write("Using API key from sidebar input.")
    use_api_key = api_input.strip() or API_KEY
    st.markdown("---")
    st.write("Sample queries:")
    st.write("- Mumbai")
    st.write("- London")
    st.write("- New York")
    st.write("- Tokyo")
    st.write("- Sydney")
    st.markdown("---")
    st.markdown("Notes:")
    st.caption("Get your key from openweathermap.org -> Sign Up -> API keys")

# main content controls
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("Enter city name", value="Mumbai")
with col2:
    unit_choice = st.radio("Units", ("Celsius (°C)", "Fahrenheit (°F)"))

units = "metric" if unit_choice.startswith("Celsius") else "imperial"
temp_unit = "°C" if units == "metric" else "°F"

# Use the API key chosen
API_KEY = use_api_key

if not API_KEY:
    st.error("No OpenWeatherMap API key provided. Paste it in the sidebar (or in the script).")
    st.stop()

if city.strip() == "":
    st.info("Type a city name to fetch weather.")
    st.stop()

try:
    with st.spinner(f"Fetching weather for {city}..."):
        current = fetch_current_weather(city.strip(), units)
        forecast = fetch_forecast(city.strip(), units)

    # --- Current weather display ---
    st.subheader(f"Current weather in {current.get('name')}, {current.get('sys', {}).get('country', '')}")
    weather = current["weather"][0]
    main = weather.get("main", "")
    desc = weather.get("description", "").title()
    icon = weather.get("icon")
    tz_offset = current.get("timezone", 0)  # seconds
    sunrise = current.get("sys", {}).get("sunrise")
    sunset = current.get("sys", {}).get("sunset")
    temp = current.get("main", {}).get("temp")
    feels_like = current.get("main", {}).get("feels_like")
    humidity = current.get("main", {}).get("humidity")
    wind_speed = current.get("wind", {}).get("speed")

    col1, col2 = st.columns([1, 2])
    with col1:
        # show OWM icon (dynamic)
        st.image(icon_url(icon), width=100)
        st.write(emoji_for_weather(main), f"{main}")
        st.caption(desc)
    with col2:
        st.metric("Temperature", f"{temp} {temp_unit}", delta=f"Feels like {feels_like} {temp_unit}")
        st.write(f"*Humidity:* {humidity}%")
        st.write(f"*Wind speed:* {wind_speed} m/s")
        if sunrise and sunset:
            st.write(f"*Sunrise:* {to_local_time(sunrise, tz_offset)} (local)")
            st.write(f"*Sunset:* {to_local_time(sunset, tz_offset)} (local)")

    # --- Forecast processing ---
    # The 5-day forecast endpoint returns 3-hourly points. We'll aggregate into daily min/mean/max.
    items = forecast.get("list", [])
    if not items:
        st.warning("No forecast data available.")
    else:
        df = pd.DataFrame(items)
        # extract useful columns
        df["dt_txt"] = pd.to_datetime(df["dt_txt"])
        df["date"] = df["dt_txt"].dt.date
        df["temp"] = df["main"].apply(lambda m: m.get("temp"))
        df["temp_min"] = df["main"].apply(lambda m: m.get("temp_min"))
        df["temp_max"] = df["main"].apply(lambda m: m.get("temp_max"))
        df["pop"] = df.get("pop", 0)  # probability of precipitation
        # group by date to produce daily stats (take next 5 distinct dates)
        grouped = df.groupby("date").agg({
            "temp": "mean",
            "temp_min": "min",
            "temp_max": "max",
            "pop": "mean"
        }).reset_index()
        # take next 5 days (sometimes response includes partial day)
        daily = grouped.head(5)

        st.subheader("5-Day Forecast")
        st.write("Aggregated daily: mean / min / max temperatures")

        # show table
        table_display = daily.copy()
        table_display["date"] = table_display["date"].astype(str)
        table_display = table_display.rename(columns={
            "temp": f"Mean ({temp_unit})",
            "temp_min": f"Min ({temp_unit})",
            "temp_max": f"Max ({temp_unit})",
            "pop": "Precip Prob"
        })
        st.dataframe(table_display.style.format({f"Mean ({temp_unit})":"{:.1f}", f"Min ({temp_unit})":"{:.1f}", f"Max ({temp_unit})":"{:.1f}", "Precip Prob":"{:.0%}"}))

        # --- Forecast chart (Matplotlib) ---
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.plot(daily["date"], daily["temp_max"], marker="o", label=f"Max ({temp_unit})")
        ax.plot(daily["date"], daily["temp_min"], marker="o", label=f"Min ({temp_unit})")
        ax.set_title("5-Day Temperature Forecast")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Temperature ({temp_unit})")
        ax.legend()
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)

        # Show a small 3-hour chart for the next 24 hours (optional)
        next_24 = df[df["dt_txt"] <= (pd.Timestamp.now() + pd.Timedelta(hours=24))]
        if not next_24.empty:
            st.subheader("Next 24 hours (3-hr interval)")
            fig2, ax2 = plt.subplots(figsize=(8, 3))
            ax2.plot(next_24["dt_txt"], next_24["temp"], marker="o")
            ax2.set_xticklabels(next_24["dt_txt"].dt.strftime("%m-%d %H:%M"), rotation=30, ha="right")
            ax2.set_title("Temperatures (3-hour steps)")
            ax2.set_ylabel(f"Temp ({temp_unit})")
            ax2.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
            plt.tight_layout()
            st.pyplot(fig2)

    st.markdown("---")
    st.caption("Data source: OpenWeatherMap (Current weather & 5-day/3-hour forecast).")

except requests.HTTPError as e:
    if e.response is not None and e.response.status_code == 404:
        st.error("City not found. Try a different city name (e.g. 'Mumbai' or 'London').")
    else:
        st.error(f"HTTP error: {e}")
except Exception as e:
    st.error(f"Error fetching weather: {e}")
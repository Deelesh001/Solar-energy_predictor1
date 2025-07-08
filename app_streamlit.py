import streamlit as st
import requests
import json
import joblib
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = st.secrets["API_KEY"]
if not API_KEY:
    st.error("API key not found. Please check your .env file.")

# Location (Gerdshagen, Germany)
LATITUDE = 53.9574
LONGITUDE = 12.2534

# OpenWeatherMap Free Forecast API (5-day forecast, every 3 hours)
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"

# Load the trained AI model
MODEL_PATH = 'model/solar_energy_model.pkl'
model = joblib.load(MODEL_PATH)

# Streamlit Page Configuration
st.set_page_config(page_title="Solar Energy Prediction", page_icon="☀️", layout="wide")

# Sidebar with Toggle Navigation
st.sidebar.image("logo.png", use_column_width=True)
page = st.sidebar.radio("Navigation", ["Home", "Notifications", "About"])

if page == "Home":
    # Streamlit App Title
    st.title("ÖkoStrom Solarpark 2.0")
    st.write("This app predicts solar energy production and provides dynamic pricing notifications based on weather forecasts.")
    
    # Fetch weather forecast from OpenWeatherMap API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tomorrow_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Filter the forecast list for entries starting with tomorrow's date
        tomorrow_forecasts = [entry for entry in data.get("list", []) if entry.get("dt_txt", "").startswith(tomorrow_date)]
        
        if tomorrow_forecasts:
            avg_temp = sum(forecast["main"]["temp"] for forecast in tomorrow_forecasts) / len(tomorrow_forecasts)
            avg_clouds = sum(forecast["clouds"]["all"] for forecast in tomorrow_forecasts) / len(tomorrow_forecasts)
            
            # Estimate solar irradiance
            solar_irradiance_estimate = max(0, 100 - avg_clouds)
            
            st.write(f"### Forecast for Tomorrow ({tomorrow_date})")
            st.write(f"🌡️ Average Temperature: {avg_temp:.2f} °C")
            st.write(f"☁️ Average Cloud Cover: {avg_clouds:.2f}%")
            st.write(f"☀️ Estimated Solar Irradiance: {solar_irradiance_estimate:.2f} W/m²")
            
            # Prepare input for model (only using solar irradiance and temperature)
            input_data = np.array([[solar_irradiance_estimate, avg_temp]])
            
            # Prediction Button
            if st.button("Predict Energy Production"):
                prediction = model.predict(input_data)[0]
                st.write(f"### Predicted Energy Production: {prediction:.2f} kWh")
                
                # Dynamic Pricing Notifications
                if prediction > 80:
                    st.success("🔋 Use energy now! Prices might be low.")
                elif 50 <= prediction <= 80:
                    st.warning("⚡ Prices are moderate. Consider efficient usage.")
                else:
                    st.error("💰 Prices might be high. Reduce energy consumption.")
        else:
            st.warning("⚠️ No forecast data available for tomorrow!")
    else:
        st.error("⚠️ Failed to fetch weather data. Please check the API connection.")

elif page == "Notifications":
    st.title("🔔 Notifications")
    st.write("Here you can find the latest updates on energy production and pricing.")
    st.info("✅ Most of your energy is coming from Gerdshagen Solar Park.")

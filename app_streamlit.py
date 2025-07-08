import streamlit as st
import requests
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

# OpenWeatherMap Free Forecast API
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"

# Load the trained AI model
MODEL_PATH = 'model/solar_energy_model.pkl'
model = joblib.load(MODEL_PATH)

# Streamlit Page Configuration
st.set_page_config(page_title="Solar Energy Prediction", page_icon="☀️", layout="wide")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
page = st.sidebar.radio("Navigation", ["Home", "Notifications", "About"])

if page == "Home":
    st.title("☀️ ÖkoStrom Solarpark 2.0")
    st.write("AI-powered forecast of solar energy production based on weather conditions.")

    # Fetch weather data
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Forecast Selector
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)

        options = {
            f"📅 Today ({today.strftime('%d %b')})": 0,
            f"🌤️ Tomorrow ({tomorrow.strftime('%d %b')})": 1,
            f"⛅ Day After Tomorrow ({day_after.strftime('%d %b')})": 2
        }

        selected_label = st.selectbox("Select a Day to Forecast Solar Output", list(options.keys()))
        day_offset = options[selected_label]
        selected_date = (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')

        # Filter forecast entries
        selected_forecasts = [
            entry for entry in data.get("list", [])
            if entry.get("dt_txt", "").startswith(selected_date)
        ]

        if selected_forecasts:
            # Calculate weather averages
            avg_temp = sum(f["main"]["temp"] for f in selected_forecasts) / len(selected_forecasts)
            avg_clouds = sum(f["clouds"]["all"] for f in selected_forecasts) / len(selected_forecasts)
            solar_irradiance_estimate = max(0, 100 - avg_clouds)

            # 🌤️ Weather Summary Card
            with st.container():
                st.markdown("### 📊 Weather Summary")
                st.subheader(f"📅 Forecast for {selected_label}")

                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Temperature", f"{avg_temp:.1f} °C")
                col2.metric("☁️ Cloud Cover", f"{avg_clouds:.0f} %")
                col3.metric("☀️ Irradiance", f"{solar_irradiance_estimate:.0f} W/m²")

            st.write("")  # spacing between cards

            # 🔋 Prediction Card
            with st.container():
                st.markdown("### 🔮 Energy Production Forecast")

                input_data = np.array([[solar_irradiance_estimate, avg_temp]])

                if st.button("Predict Energy Production"):
                    prediction = model.predict(input_data)[0]
                
                    # Big bold prediction display (card-style)
                    st.markdown(
                        f"""
                        <div style='background-color:#22c55e;padding:1rem 1.5rem;border-radius:0.75rem;margin-top:1rem;margin-bottom:1rem;'>
                            <h2 style='text-align:center;color:white;margin:0;'>🔋 Predicted Energy Output</h2>
                            <p style='text-align:center;font-size:2rem;color:white;margin:0;'><strong>{prediction:.2f} kWh</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                    # Tip heading
                    st.markdown("### 💡 Smart Energy Tip")
                
                    # Dynamic pricing notification
                    if prediction > 80:
                        st.success("☀️ Excellent solar generation expected today! Consider feeding energy into the grid or running high-load systems now to maximize profit.")
                    elif 50 <= prediction <= 80:
                        st.warning("🌤️ Moderate solar output forecast. It's a good time for balanced usage or storing excess energy if available.")
                    else:
                        st.error("☁️ Low solar energy expected. Minimize heavy usage or rely on storage/backups. Consider delaying high-consumption tasks.")

        else:
            st.warning("⚠️ No forecast data available for that day.")
    else:
        st.error("⚠️ Failed to fetch weather data. Please check the API connection.")




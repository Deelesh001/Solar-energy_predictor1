import os
from datetime import datetime, timedelta

import numpy as np
import requests
import joblib
import streamlit as st

# ---------------- Constants ----------------
LATITUDE = 53.9574
LONGITUDE = 12.2534
MODEL_PATH = 'model/solar_energy_model.pkl'
HIGH_OUTPUT_THRESHOLD = 80
MEDIUM_OUTPUT_THRESHOLD = 50

# ---------------- Load API Key ----------------
API_KEY = st.secrets.get("API_KEY")
if not API_KEY:
    st.error("API key not found. Please add it to .streamlit/secrets.toml.")
    st.stop()

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Solar Energy Prediction", page_icon="☀️", layout="wide")
st.sidebar.image("assets/logo.png", width=150)


page = st.sidebar.radio("Navigation", ["Home", "About"])

# ---------------- Helper Functions ----------------
@st.cache_data(show_spinner=False)
def load_model(path):
    try:
        return joblib.load(path)
    except FileNotFoundError:
        st.error("⚠️ Model file not found.")
        st.stop()

@st.cache_data(show_spinner=False)
def fetch_weather_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch weather data: {e}")
        return None

def summarize_forecast(forecast_list):
    temps = [entry["main"]["temp"] for entry in forecast_list]
    clouds = [entry["clouds"]["all"] for entry in forecast_list]
    avg_temp = np.mean(temps)
    avg_clouds = np.mean(clouds)
    irradiance = max(0, 100 - avg_clouds)
    return avg_temp, avg_clouds, irradiance

# ---------------- Load Model ----------------
model = load_model(MODEL_PATH)

# ---------------- Home Page ----------------
if page == "Home":
    st.title("☀️ ÖkoStrom Solarpark 2.0")
    st.write("AI-powered forecast of solar energy production in Gerdshagen based on real-time weather conditions.")

    weather_data = fetch_weather_data(LATITUDE, LONGITUDE, API_KEY)

    if weather_data:
        # Date selection
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

        selected_forecasts = [
            entry for entry in weather_data.get("list", [])
            if entry.get("dt_txt", "").startswith(selected_date)
        ]

        if selected_forecasts:
            avg_temp, avg_clouds, irradiance = summarize_forecast(selected_forecasts)

            # --- Weather Summary ---
            with st.container():
                st.markdown("### 📊 Weather Summary")
                st.subheader(f"📅 Forecast for {selected_label}")

                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Temperature", f"{avg_temp:.1f} °C")
                col2.metric("☁️ Cloud Cover", f"{avg_clouds:.0f} %")
                col3.metric("☀️ Irradiance", f"{irradiance:.0f} W/m²")

            st.write("")  # spacing

            # --- Energy Prediction ---
            with st.container():
                st.markdown("### 🔮 Energy Production Forecast")

                input_data = np.array([[irradiance, avg_temp]])

                if st.button("Predict Energy Production"):
                    prediction = model.predict(input_data)[0]

                    # Display prediction result
                    st.markdown(
                        f"""
                        <div style='background-color:#22c55e;padding:1rem 1.5rem;border-radius:0.75rem;margin-top:1rem;margin-bottom:1rem;'>
                            <h2 style='text-align:center;color:white;margin:0;'>🔋 Predicted Energy Output</h2>
                            <p style='text-align:center;font-size:2rem;color:white;margin:0;'><strong>{prediction:.2f} kWh</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Smart notification
                    st.markdown("### 💡 Smart Energy Tip")
                    if prediction > HIGH_OUTPUT_THRESHOLD:
                        st.success("☀️Excellent solar generation expected today!  "
                                    "It’s a good time to run high-consumption appliances or systems to take advantage of clean, abundant energy.")
                    elif prediction >= MEDIUM_OUTPUT_THRESHOLD:
                        st.warning("🌤️ Moderate solar output forecast. It's a good time for balanced usage or storing excess energy if available.")
                    else:
                        st.error("☁️ Low solar energy expected.Consider delaying high-consumption tasks.")
        else:
            st.warning("⚠️ No forecast data available for that day.")
    else:
        st.error("⚠️ Weather data unavailable. Check API settings.")

# ---------------- About Page ----------------
elif page == "About":
    st.title("ℹ️ About ÖkoStrom Solarpark")

    st.markdown("""
    **ÖkoStrom Solarpark 2.0** is a smart, AI-powered web app that forecasts solar energy production based on local weather conditions in Gerdshagen, Germany.

    The goal is to help users—such as solar operators or energy planners—better understand daily solar output trends and make informed decisions about energy use or storage.

    ---
    ### 👥 Team & Collaboration

    This project was developed by **Deelesh Puttyah** and **Akhilesh Sohotoo**  
    as part of a university collaboration between **XU Exponential University** and **E.ON**, one of Europe’s leading energy providers.

    ---
    ### 🌱 Why This Matters

    Forecasting renewable energy is a key step toward building more reliable and sustainable energy systems.  
    ÖkoStrom Solarpark 2.0 is a small step toward making green energy smarter, more accessible, and more impactful.

    ---
    _For more technical details, visit our GitHub portfolio (coming soon)._
    """)







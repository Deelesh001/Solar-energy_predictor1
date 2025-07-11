<p align="center">
  <img src="assets/logo.png" width="180" alt="Logo">
</p>

# ÖkoStrom Companion – Solar Forecast & Dynamic Pricing

Welcome! This is a Streamlit web app I developed as part of a school project in collaboration with E.ON. The goal was to help users understand when solar energy is most available and use that insight to make smarter, greener energy choices.

The app predicts solar energy production based on weather forecasts and gives friendly, dynamic feedback about energy usage — especially tailored to those on E.ON’s Ökostrom package.

## 🌟 What the App Does

- Lets users pick between Today, Tomorrow, or Day After Tomorrow to see the solar forecast.
- Pulls real-time weather data (temperature and cloud cover) from OpenWeatherMap.
- Estimates solar irradiance and predicts how much energy will be generated using a trained ML model.
- Visualizes the forecast with a simple, interactive line chart for the next 3 days.
- Shows smart, encouraging messages about when to use more or less energy — without making the user feel guilty on cloudy days.

## 🔍 How the Prediction Works

The prediction is based on two key weather features: average temperature and cloud cover. I trained a regression model (in scikit-learn) to estimate daily solar output (in kWh) from these inputs.

While the model itself is included in this repo as a `.pkl` file, the training data and code are not shared here due to confidentiality agreements related to the project.

## 🖥️ Try It Yourself

If you want to run this app locally, here's how:

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/solar-predictor-eon.git



Install the requirements:
pip install -r requirements.txt
Add a .env file with your own OpenWeatherMap API key. You can get a free one by signing up at openweathermap.org. Your .env file should look like this:
API_KEY=your_openweathermap_api_key
Run the app:
streamlit run app.py
📊 Tools and Technologies Used

Python and Streamlit for the web app
Scikit-learn and joblib for the ML model
OpenWeatherMap API for weather forecasts
Plotly for data visualization
GitHub + Streamlit Cloud for versioning and deployment
🎯 Project Background

This app was developed for a university project focused on renewable energy and customer engagement. The inspiration came from wanting to make green energy feel more human — encouraging users to feel good about their choices, even on cloudy days.

👤 Author

Hi, I'm Deelesh Sohotoo, a BSc (Hons) Computer Science with Network Security student. I enjoy building useful tools with AI, data, and clean UI — especially in the sustainability space.

If you’re reviewing this for a job or internship: thanks for reading, and I’d be happy to walk you through how I built it!

   cd solar-predictor-eon

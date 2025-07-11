<p align="center">
  <img src="assets/logo.png" width="180" alt="Logo">
</p>

#  Solar Forecast & Dynamic Pricing for E.ON 

This is a Streamlit web app I developed as part of a school project in collaboration with E.ON. The goal is to help users understand when solar energy is most available and use that insight to make smarter, greener energy choices.

The app predicts solar energy production based on weather forecasts and gives friendly, dynamic feedback about energy usage — especially useful for customers using E.ON’s Ökostrom package.

## 🌟 What the App Does

- Lets users choose between Today, Tomorrow, or Day After Tomorrow to view the solar forecast.
- Pulls real-time weather data (temperature and cloud cover) using the OpenWeatherMap API.
- Estimates solar irradiance and predicts energy output using a trained ML model.
- Shows an interactive line chart to visualize solar potential for the next 3 days.
- Provides smart and friendly messages based on predicted energy output — encouraging sustainable usage, even in cloudy weather.

## 🔍 How the Prediction Works

The model uses two features — average temperature and cloud cover — to predict solar energy output in kWh. I trained this model using historical solar and weather data.

The model is included in this repo as a `.pkl` file for real-time inference.  
However, the training data and code are not shared due to confidentiality agreements with the school and project sponsor.

## 🖥️ Run It Locally

To run this app on your machine:

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/solar-predictor-E.ON.git
   cd solar-predictor-E.on
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenWeatherMap API key.

   Sign up at ([https://openweathermap.org/api]) to get a free API key.

   Create a file named:

   ```
   .streamlit/secrets.toml
   ```

   Paste this inside:

   ```toml
   API_KEY = "your_openweathermap_api_key"
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

If you're using **Streamlit Cloud**, you can add the API key under **"Secrets"** in the app settings instead of using `secrets.toml`.

## 📁 Folder Structure

Here's how the project is organized:

```
solar-predictor-eon/
├── app.py
├── model/
│   └── solar_energy_model.pkl
├── assets/
│   └── logo.png
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── README.md
```

## 📊 Tools and Technologies Used

- Python and Streamlit for the web interface
- Scikit-learn and joblib for the machine learning model
- OpenWeatherMap API for real-time weather forecasts
- GitHub and Streamlit Cloud for version control and deployment

## 🎯 Project Background

This app was developed for a university project on renewable energy and customer engagement.  
The main idea was to promote green behavior in a way that feels human — celebrating good solar days and staying supportive on cloudy ones.

## 👤 Author

Hi, I'm **Deelesh Puttyah**, a Data Science student.  
I enjoy building practical, data-driven tools with clean UI — especially in the sustainability space.





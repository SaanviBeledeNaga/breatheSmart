import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model", "aqi_model.pkl")
model = joblib.load(model_path)


def predict_tomorrow_aqi(city):
    csv_path = os.path.join(BASE_DIR, "data", "aqi_data.csv")
    df = pd.read_csv(csv_path)
    # Normalize city names
    df["city"] = df["city"].str.lower()
    city = city.lower()

    city_data = df[df["city"] == city]

    if city_data.empty:
        return 100  # fallback safe value

    last_7_days = city_data.tail(7)

    features = last_7_days[["pm25","pm10","no2","so2"]].mean().values.reshape(1, -1)

    prediction = model.predict(features)[0]

    return round(prediction, 1)

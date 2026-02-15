import pandas as pd
def prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    X = df[["pm25","pm10","no2","so2"]]
    y = df["aqi"]

    return X, y

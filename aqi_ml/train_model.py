import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from aqi_ml.preprocess import prepare_data

X, y = prepare_data("data/aqi_data.csv")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, "model/aqi_model.pkl")

print("AQI model trained and saved successfully.")

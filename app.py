from flask import Flask, render_template, request, jsonify

from aqi_ml.predictor import predict_tomorrow_aqi
from aqi_ml.aqi_utils import classify_aqi

from carbon.calculator import calculate_total_emission
from carbon_ai.recommender import recommend_actions

app = Flask(__name__)

# ---------------- HOME / AQI PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict-aqi")
def predict_aqi_only():
    city = request.args.get("city", "Delhi")

    predicted_aqi = predict_tomorrow_aqi(city)
    aqi_level = classify_aqi(predicted_aqi)

    return jsonify({
        "predicted_aqi": predicted_aqi,
        "aqi_level": aqi_level
    })


# ---------------- CARBON PAGE ----------------

@app.route("/carbon")
def carbon_page():
    return render_template("carbon.html")


@app.route("/carbon", methods=["POST"])
def carbon_calculation():
    data = request.json

    emissions = calculate_total_emission(
        data["distance"],
        data["mode"]
    )

    # Use Delhi as default AQI context for suggestions
    predicted_aqi = predict_tomorrow_aqi("Delhi")
    aqi_level = classify_aqi(predicted_aqi)

    suggestions = recommend_actions(emissions, aqi_level)

    return jsonify({
        "emissions": emissions,
        "suggestions": suggestions
    })


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)

// ---------------- AQI PREDICTION ----------------

function predictAQI() {
  const city = document.getElementById("city").value;

  fetch(`/predict-aqi?city=${city}`)
    .then(res => res.json())
    .then(result => {
      const aqiEl = document.getElementById("aqiResult");

      aqiEl.innerText =
        result.predicted_aqi + " AQI (" + result.aqi_level + ")";
    })
    .catch(() => {
      document.getElementById("aqiResult").innerText =
        "Unable to fetch AQI";
    });
}




// ---------------- CARBON CALCULATION ----------------

function calculateCarbon() {
  const distance = Number(document.getElementById("distance").value);
  const mode = document.getElementById("mode").value;

  fetch("/carbon", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      distance: distance,
      mode: mode
    })
  })
  .then(res => {
    if (!res.ok) {
      throw new Error("Server error");
    }
    return res.json();
  })
  .then(result => {
    document.getElementById("carbonResult").innerText =
      result.emissions.total + " kg CO₂";

    document.getElementById("suggestions").innerHTML =
      result.suggestions.map(s => `<li>${s}</li>`).join("");
  })
  .catch(error => {
    console.error(error);
    document.getElementById("carbonResult").innerText =
      "Error calculating footprint";
  });
}

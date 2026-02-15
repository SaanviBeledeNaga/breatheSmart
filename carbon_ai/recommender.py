def recommend_actions(emissions, aqi_level):
    suggestions = []

    total = emissions.get("total", 0)

    if total > 20:
        suggestions.append("Consider using public transport or carpooling.")
    elif total > 5:
        suggestions.append("Try reducing unnecessary vehicle trips.")
    else:
        suggestions.append("Great job! Your transport footprint is low.")

    if aqi_level in ["Poor", "Severe"]:
        suggestions.append("Avoid outdoor activities and use masks if necessary.")
        suggestions.append("Consider remote work or public transport options.")

    return suggestions

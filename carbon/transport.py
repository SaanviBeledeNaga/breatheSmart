from carbon.emission_factors import TRANSPORT_EMISSIONS

def calculate_transport_emission(distance_km, mode):
    return round(distance_km * TRANSPORT_EMISSIONS[mode], 2)

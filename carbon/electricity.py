from carbon.emission_factors import ELECTRICITY_EMISSION_FACTOR

def calculate_electricity_emission(units):
    return round(units * ELECTRICITY_EMISSION_FACTOR, 2)

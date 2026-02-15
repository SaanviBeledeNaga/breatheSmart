from carbon.transport import calculate_transport_emission

def calculate_total_emission(distance, mode):
    transport = calculate_transport_emission(distance, mode)

    return {
        "transport": round(transport, 2),
        "total": round(transport, 2)
    }

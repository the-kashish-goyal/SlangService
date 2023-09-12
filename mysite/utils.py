import json


def covert_to_json_serializable(decimal_value):
    serializable_value = float(decimal_value)  # Convert to float

    # Serialize the serializable value to JSON
    json_data = json.dumps({'decimal_value': serializable_value})
    return json_data

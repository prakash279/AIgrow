import json

def json_format(weather_data, location):
    weather_entries = []
    
    for line in weather_data.strip().split('\n'):
        date, details = line.split(': ', 1)
        temp_info, conditions = details.split('Conditions: ')
        min_temp = temp_info.split(', ')[0].split(': ')[1]
        max_temp = temp_info.split(', ')[1].split(': ')[1]
        conditions_list = [condition.strip() for condition in conditions.split(',')]
        
        weather_entries.append({
            "date": date,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "conditions": conditions_list
        })
        
    location_parts = location.split(', ')
    location_dict = {
        "city_or_village": location_parts[0] if len(location_parts) > 0 else "",
        "state": location_parts[1] if len(location_parts) > 1 else "",
        "country": location_parts[2] if len(location_parts) > 2 else ""
    }
    
    output_data = {
        "location": location_dict,
        "weather_data": weather_entries
    }
    
    weather_json = json.dumps(output_data, indent=4)
    return weather_json
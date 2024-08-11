from datetime import datetime
from collections import defaultdict

def process_weather_data(data):
    daily_summary = defaultdict(lambda: {'temp_min': float('inf'), 'temp_max': float('-inf'), 'weather': set()})

    for forecast in data["list"]:
        dt = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        day = dt.date()
        temp = forecast["main"]["temp"]
        weather = forecast["weather"][0]["description"]
        
        if temp < daily_summary[day]['temp_min']:
            daily_summary[day]['temp_min'] = temp
        if temp > daily_summary[day]['temp_max']:
            daily_summary[day]['temp_max'] = temp
        daily_summary[day]['weather'].add(weather)

    summary_text = ""
    for day, summary in daily_summary.items():
        weather_conditions = ', '.join(summary['weather'])
        summary_text += f"{day}: Min Temp: {summary['temp_min']:.1f}°C, Max Temp: {summary['temp_max']:.1f}°C, Conditions: {weather_conditions}\n"

    return summary_text

# def fetch_location 
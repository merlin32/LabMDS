import requests
import json

lat = 44.4375
long = 26.091
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
response = requests.get(url)
data = response.json()
timezone = data["timezone"]
temperature = str(data["current_weather"]["temperature"]) + " " + data["current_weather_units"]["temperature"]
print(f"Timezone: {timezone}")
print(f"Temperature: {temperature}")

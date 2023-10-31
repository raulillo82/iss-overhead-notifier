import requests
from datetime import datetime

API_SUNRISE_SUNSET = "https://api.sunrise-sunset.org/json"

parameters_Vitoria = {
    "name": "Vitoria-Gasteiz",
    "latitude": 42.8465088,
    "longitude": -2.6724025,
    "country": "ES",
    "state": "Autonomous Community of the Basque Country",
    }

parameters = {
        "lat": parameters_Vitoria["latitude"],
        "lng": parameters_Vitoria["longitude"],
        "formatted": 0,
        }

response = requests.get(API_SUNRISE_SUNSET, params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
print(sunrise.split("T")[1].split(":"), sunset)


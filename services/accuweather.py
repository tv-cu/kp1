import requests

BASE_URL = "https://dataservice.accuweather.com"


class AccuWeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_location_key(self, latitude: float, longitude: float) -> str:
        url = f"{BASE_URL}/locations/v1/cities/geoposition/search"
        params = {
            "apikey": self.api_key,
            "q": f"{latitude},{longitude}",
            "language": "ru"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data["Key"]

    def get_weather(self, location_key: str, days: int) -> list:
        url = f"{BASE_URL}/forecasts/v1/daily/5day/{location_key}"
        params = {
            "apikey": self.api_key,
            "language": "ru",
            "metric": True,
            "details": True
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        daily_forecasts = data["DailyForecasts"][:days]

        results = []
        for forecast_day in daily_forecasts:
            date_str = forecast_day["Date"].split("T")[0]
            temp_min = forecast_day["Temperature"]["Minimum"]["Value"]
            temp_max = forecast_day["Temperature"]["Maximum"]["Value"]
            precip_probability = forecast_day["Day"]["PrecipitationProbability"]

            results.append({
                "date": date_str,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "precipitation_probability": precip_probability
            })

        return results

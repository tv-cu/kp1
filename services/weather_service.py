import logging

import requests
from geopy.exc import GeopyError
from geopy.geocoders import Nominatim

from config import API_KEY
from services.accuweather import AccuWeatherAPI
from utils.exceptions import WeatherServiceError

weather_api = AccuWeatherAPI(API_KEY)
geolocator = Nominatim(user_agent="telegram-weather-bot")


def get_weather_forecast(start_point: str,
                         end_point: str,
                         intermediate_points: list,
                         interval: int) -> list:
    all_points = [(start_point, "start")] + \
                 [(p, "inter") for p in intermediate_points] + \
                 [(end_point, "end")]

    results = []

    for place, _ in all_points:
        try:
            location = geolocator.geocode(place)
            if not location:
                raise WeatherServiceError(f"Не удалось определить координаты для города {place}")

            loc_key = weather_api.get_location_key(latitude=location.latitude,
                                                   longitude=location.longitude)

            daily_data = weather_api.get_weather(loc_key, days=interval)

            days_data = []
            for d in daily_data:
                days_data.append({
                    "date": d["date"],
                    "temp_min": d["temp_min"],
                    "temp_max": d["temp_max"],
                    "precip": d["precipitation_probability"]
                })

            results.append({
                "point": place,
                "days": days_data
            })

        except (GeopyError, requests.RequestException) as e:
            logging.exception(e)
            raise WeatherServiceError(f"Ошибка при запросе геоданных/AccuWeather для {place}")
        except WeatherServiceError as we:
            raise WeatherServiceError(str(we))
        except Exception as ex:
            logging.exception(ex)
            raise WeatherServiceError(f"Непредвиденная ошибка при обработке точки {place}")

    return results

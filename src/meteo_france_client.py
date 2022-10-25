from datetime import datetime
from typing import List, Tuple
from meteofrance_api import MeteoFranceClient
from aggregate_data import aggregate_data
from message import get_complete_message, get_driest_moments_message

NB_DAYS_FROM_NOW = [2, 7]
HUMIDITY_THRESHOLD = 70


class MyMeteoFranceClient(MeteoFranceClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_days_data(self, city: str) -> List:
        """Get forecast data for the next few days for the given city."""
        # Search a location from name.
        list_places = self.search_places(city)
        my_place = list_places[0]

        # Fetch weather forecast for the location
        my_place_weather_forecast = self.get_forecast_for_place(my_place)

        # Get the daily forecast
        my_place_forecast = my_place_weather_forecast.forecast

        next_days_data = []
        # Format the data
        for forecast in my_place_forecast:
            forecast_data = {
                "date": datetime.fromtimestamp(forecast["dt"]),
                "temperature": forecast["T"]["value"],
                "humidity": forecast["humidity"],
            }
            next_days_data.append(forecast_data)
        return next_days_data

    def get_dry_weather_messages(self, city: str) -> Tuple[str, str]:
        next_days_data = self.get_next_days_data(city)
        aggregated_data = aggregate_data(next_days_data)

        short_message = get_driest_moments_message(aggregated_data, NB_DAYS_FROM_NOW)
        complete_message = get_complete_message(aggregated_data, HUMIDITY_THRESHOLD)
        return (short_message, complete_message)

from .base_client import BaseClient

class WeatherAPI(BaseClient):
    ALLOWED_FORECAST_DAYS = {1, 5, 10, 15}

    def __init__(self, api_key: str, language: str):
        super().__init__(base_url="http://dataservice.accuweather.com")
        self.api_key = api_key
        self.language = language

    async def get_cities_autocomplete(self, city: str):
        params = {
            "q": city,
            "language": self.language,
            "apikey": self.api_key
        }
        return await self.get("locations/v1/cities/autocomplete", params=params)

    async def get_forecast_daily(self, days: int, location_key: str, details: bool = True, metric: bool = True):
        if days not in self.ALLOWED_FORECAST_DAYS:
            raise ValueError(
                f"Некорректное значение для параметра 'days': {days}. Допустимые значения: {self.ALLOWED_FORECAST_DAYS}.")

        params = {
            "language": self.language,
            "details": str(details).lower(),  # Преобразуем bool в "true"/"false"
            "metric": str(metric).lower(),  # Преобразуем bool в "true"/"false"
            "apikey": self.api_key
        }
        endpoint = f"forecasts/v1/daily/{days}day/{location_key}"
        response = await self.get(endpoint, params=params)

        forecast_data = []
        for day_forecast in response.get("DailyForecasts", []):
            day_data = {
                "date": day_forecast["Date"],
                "temperature_max": day_forecast["Temperature"]["Maximum"]["Value"],
                "temperature_min": day_forecast["Temperature"]["Minimum"]["Value"],
                "humidity": day_forecast["Day"].get("RelativeHumidity", {}).get("Average"),
                "wind_speed": day_forecast["Day"]["Wind"]["Speed"]["Value"],
                "rain_probability": day_forecast["Day"]["PrecipitationProbability"],
            }
            forecast_data.append(day_data)

        return forecast_data

    async def get_nearest_city(self, lat: float, lon: float):
        """
        Получение ближайшего города по координатам.
        """
        params = {
            "q": f"{lat},{lon}",
            "apikey": self.api_key,
            "language": self.language
        }
        return await self.get("locations/v1/cities/geoposition/search", params=params)



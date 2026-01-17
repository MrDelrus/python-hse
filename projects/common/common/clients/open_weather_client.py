import logging
import httpx

from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class OpenWeatherClient:
    def __init__(self, api_key: str) -> None:
        self._owm = OWM(api_key)
        self._manager = self._owm.weather_manager()

    def get_temperature(self, city: str, units: str = "celsius") -> float:
        logger.info("Request current temperature in %s", city)

        try:
            observation = self._manager.weather_at_place(city)
        except NotFoundError:
            error_msg = f"City not found: {city}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        weather = observation.weather
        temperature = weather.temperature(units)["temp"]

        logger.info("Received temperature in city %s is %.2f", city, temperature)

        return float(temperature)


class AsyncOpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def get_temperature(self, city: str, units: str = "metric") -> float:
        logger.info("Request current temperature in %s", city)

        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        data = response.json()
        temperature = data["main"]["temp"]

        logger.info("Received temperature in city %s is %.2f", city, temperature)

        return float(temperature)

# weather_client_async.py
import httpx
from datetime import datetime, timedelta

class AsyncWeatherClient:
    """Async client for WeatherAPI.com"""

    BASE_CURRENT = "http://api.weatherapi.com/v1/current.json"
    BASE_FORECAST = "http://api.weatherapi.com/v1/forecast.json"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_current(
        self,
        location: str = None,
        start_date: str = None,
        end_date: str = None,
        aqi: str = "no"
    ) -> list:
        """
        Fetch current weather data asynchronously.
        If start_date and end_date are provided, fetch weather for each date in the range.
        Dates should be in 'YYYY-MM-DD' format.
        """
        if location is None:
            return {"error": "Location is required."}

        # If date range is provided, fetch for each date
        if start_date and end_date:
            BASE_HISTORY = "http://api.weatherapi.com/v1/history.json"
            results = []
            async with httpx.AsyncClient() as client:
                # start = datetime.strptime(start_date, "%Y-%m-%d")
                # Ensure start_date and end_date are strings
                if not isinstance(start_date, str):
                    start_date = start_date.strftime("%Y-%m-%d")
                if not isinstance(end_date, str):
                    end_date = end_date.strftime("%Y-%m-%d")
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                current = start
                delta = timedelta (days=1)
                while current <= end:
                    params = {
                        "key": self.api_key,
                        "q": location,
                        "dt": current.strftime("%Y-%m-%d"),
                        "aqi": aqi
                    }
                    res = await client.get(BASE_HISTORY, params=params)
                    if res.status_code == 200:
                        results.append(res.json())
                    else:
                        results.append({"error": f"Failed for {params['dt']}: {res.status_code}"})
                    current += delta
            return results

        # Otherwise, fetch current weather
        params = {"key": self.api_key, "q": location, "aqi": aqi}
        async with httpx.AsyncClient() as client:
            res = await client.get(self.BASE_CURRENT, params=params)
        if res.status_code == 200:
            return res.json()
        return {"error": f"Failed to retrieve current weather: {res.status_code}"}

    # async def get_forecast(self, location: str, days: int = 5) -> dict:
    #     """Fetch forecast asynchronously."""
    #     params = {"key": self.api_key, "q": location, "days": days}
    #     async with httpx.AsyncClient() as client:
    #         res = await client.get(self.BASE_FORECAST, params=params)
    #     if res.status_code == 200:
    #         return res.json()
    #     return {"error": f"Failed to retrieve forecast: {res.status_code}"}

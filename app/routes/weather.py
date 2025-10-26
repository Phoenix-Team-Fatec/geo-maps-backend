from fastapi import APIRouter, HTTPException, Query
import os
import requests
from dotenv import load_dotenv

load_dotenv()

weather_router = APIRouter(prefix="/weather", tags=["Weather"])

@weather_router.get("")
def get_weather(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch current weather data from OpenWeatherMap API

    Parameters:
    - lat: Latitude of the location (-90 to 90)
    - lng: Longitude of the location (-180 to 180)

    Returns:
    - Weather data in JSON format from OpenWeatherMap
    """

    api_key = os.environ.get("WEATHER_API_KEY")
    print(api_key)
    print(api_key)
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenWeather API key not configured on server"
        )

    api_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lng}"
        f"&appid={api_key}"
        f"&units=metric"
        f"&lang=pt_br"
    )

    try:
        response = requests.get(api_url, timeout=10)

        if response.status_code == 401:
            raise HTTPException(
                status_code=500,
                detail="Invalid OpenWeather API key"
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenWeatherMap API error: {response.text}"
            )

        data = response.json()
        return data

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Weather service timeout. Please try again."
        )
    except requests.RequestException as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weather data: {str(error)}"
        )

import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")

mcp = FastMCP("weather-server")

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: City name, e.g. "Seattle" or "London,UK"
    """
    if not API_KEY:
        return "Error: OWM_API_KEY is not set in .env"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "imperial"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 401:
        return "Error: API key not active yet (can take up to 2 hours) or invalid."
    if response.status_code == 404:
        return f"Error: City '{city}' not found."
    if response.status_code != 200:
        return f"Error: OpenWeatherMap returned status {response.status_code}"

    data = response.json()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    return (
        f"Weather in {city}: {description}, {temp}°F "
        f"(feels like {feels_like}°F), {humidity}% humidity"
    )

if __name__ == "__main__":
    mcp.run(transport="stdio")
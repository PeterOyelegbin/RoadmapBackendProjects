from fastapi import FastAPI, HTTPException, Path
from decouple import config
import requests, redis, json


app = FastAPI(
    title="Weather API",
    description="A weather API that fetches and returns weather data from a 3rd party API. This project will help you understand how to work with 3rd party APIs, caching, and environment variables.",
    version="v1",
    docs_url="/",
    contact={
        "name": "Peter Oyelegbin",
        "email": "peteroyelegbin@gmail.com",
    }
)

# Redis configuration
redis_client = redis.StrictRedis(host=config("REDIS_HOST"), port=config("REDIS_PORT"), db=0, decode_responses=True, username=config("REDIS_USER"), password=config("REDIS_PASSWD"))

# Visual Crossing API configuration
VISUAL_CROSSING_API_KEY = config("VISUAL_CROSSING_API_KEY")
VISUAL_CROSSING_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


@app.get("/weather/{city}")
async def get_weather(city: str = Path(..., min_length=2)):
    try:
        # Check if the weather data is in the cache
        cached_weather = redis_client.get(city)
        if cached_weather:
            response_data = {
                'status': 200,
                'message': 'data retrieved from cached successfully',
                'data': json.loads(cached_weather),
            }
            return response_data
        # If not in cache, fetch from Visual Crossing API
        response = requests.get(f"{VISUAL_CROSSING_API_URL}/{city}/today?unitGroup=metric&include=current&key={VISUAL_CROSSING_API_KEY}")
        if response.status_code == 200:
            weather_data = response.json()
            # Cache the weather data with an expiration time of 5 minutes
            redis_client.set(city, json.dumps(weather_data), ex=300)
            response_data = {
                'status': response.status_code,
                'message': 'data retrieved successfully',
                'data': weather_data,
            }
            return response_data
        else:
            response_data = {
                "status": response.status_code,
                "message": response.json(),
            }
            return response_data
    except requests.RequestException as e:
        response_data = {
            "status": 500,
            "message": str(e),
        }
        raise HTTPException(status_code=500, detail=response_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
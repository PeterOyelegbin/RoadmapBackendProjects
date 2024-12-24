# Weather API [RoadMap Project](https://roadmap.sh/projects/weather-api-wrapper-service)
**Project Overview**
In this project, we will build a weather API that fetches and returns weather data from a third-party API. This project will help you understand how to work with third-party APIs, implement caching, and manage environment variables using FastAPI, Redis, and Visual Crossing’s API.


## Problem Statement
Fetching weather data can be a resource-intensive process, especially if the data needs to be requested frequently. Constantly querying a third-party API can lead to increased costs and slower response times due to network latency. Moreover, without proper management of environment variables, sensitive information like API keys can be exposed.


## Solution
To address these challenges, we will create a weather API that:
1. **Fetches Weather Data**: Retrieves real-time weather data from a third-party API (Visual Crossing’s API).
2. **Implements Caching**: Uses Redis for in-memory caching to store weather data, reducing the number of API requests and improving response times.
3. **Manages Environment Variables**: Utilizes `python-decouple` to manage sensitive information securely.


## Technology Stack
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Redis**: An in-memory data structure store, used as a distributed, in-memory key–value database, cache, and message broker.
- **Visual Crossing API**: A third-party API that provides weather data. It is free and easy to use.


## Installation and Setup
---
### Prerequisites
- Python 3.6+
- Redis Server

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd weather-api
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the root directory and add the following environment variables:
   ```env
   VISUAL_CROSSING_API_KEY=<your_visual_crossing_api_key>
   REDIS_HOST=<your_redis_host>
   REDIS_PORT=<your_redis_port>
   REDIS_USER=<your_redis_username>
   REDIS_PASSWD=<your_redis_password>
   ```

5. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API Documentation**:
   Open your browser and navigate to `http://127.0.0.1:8000/` to view the API documentation.

## Usage
---
### Endpoints
- **GET /weather/{city}**: Fetches weather data for the specified city. If the data is not available in the cache, it retrieves it from the Visual Crossing API and caches it with a 5-minutes expiration time.

### Example Request
```bash
curl -X GET "http://127.0.0.1:8000/weather/Lagos?filter=current" -H "accept: application/json"
```

### Response
```json
{
  "status": 200,
  "message": "data retrieved successfully",
  "data": {
    "queryCost": 1,
    "latitude": 6.4547,
    "longitude": 3.38877,
    "resolvedAddress": "Lagos, Nigeria",
    "address": "Lagos",
    "timezone": "Africa/Lagos",
    "tzoffset": 1.0,
    "days": [
      {
        "datetime": "2024-12-24",
        "tempmax": 35.0,
        "tempmin": 23.0,
        "temp": 28.1,
        "conditions": "Partially cloudy",
        "description": "Becoming cloudy in the afternoon."
      }
    ],
    "currentConditions": {
      "datetime": "18:00:00",
      "temp": 29.5,
      "feelslike": 30.4,
      "conditions": "Clear"
    }
  }
}
```

## Conclusion
This project demonstrates how to integrate a third-party weather API, implement caching using Redis, and manage environment variables securely with FastAPI and `python-decouple`. By following the steps outlined in this README, you can set up and run your own weather API, improving performance and security.

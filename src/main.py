from fastapi import FastAPI, HTTPException, Query, Body # type: ignore
from typing import Optional, List
# Use relative imports since we're in a package
from .models import WeatherRequestCreate, WeatherRequestUpdate, WeatherResponse
from .repositories import create_request, get_requests, get_request_by_id, update_request, delete_request
from .weather_client import AsyncWeatherClient
from datetime import datetime
from dotenv import load_dotenv # type: ignore
import os

app = FastAPI(title="Weather App API", description="API for managing weather requests and fetching weather data.")
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set in .env file")

# DEFAULT ROUTE
@app.get ("/")
def home ():
    return {"message": "Welcome to the Weather App API! Use the endpoints to manage weather requests and fetch weather data."}  


# CREATE
@app.post("/requests", response_model=List[WeatherResponse], status_code=201)
async def create_weather_request(request: WeatherRequestCreate):
    client = AsyncWeatherClient(API_KEY)
    try:
        weather_data = await client.get_current(
            request.location_input,
            request.start_date,
            request.end_date
        )
        print("Weather API Response:", weather_data)  # Debug print
        
        if isinstance(weather_data, dict):
            weather_data = [weather_data]
        
        if not weather_data:
            raise HTTPException(status_code=404, detail="No weather data found for the given location and dates")
        
        created_data = []
        for item in weather_data:
            if not isinstance(item, dict):
                continue
            last_updated = item.get("current", {}).get("last_updated")
            if last_updated:
                date_only = datetime.strptime(last_updated, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d")
            else:
                date_only = request.start_date.strftime("%Y-%m-%d") if request.start_date else datetime.now().strftime("%Y-%m-%d") 
            request_data = {
                "user_name": request.user_name,
                "location_input": item.get("location", {}).get("name", request.location_input),
                "date_": date_only,
                "type": "current",
                "data": item
            }
            
            print("Inserting data:", request_data)  # Debug print
            created = create_request(request_data)
            if "error" in created:
                print(f"Database error: {created['error']}")  # Debug print
                raise HTTPException(status_code=500, detail=created["error"])
            created_data.append(created)
            
        if not created_data:
            raise HTTPException(status_code=500, detail="Failed to create any weather records")
            
        return created_data
    except Exception as e:
        print(f"Unexpected error: {e}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))
    
# READ ALL
@app.get("/requests", response_model=List[WeatherResponse])
def get_all_requests(filters: Optional[str] = Query(None, description="Filters as JSON string")):
    # You may want to parse filters from JSON string if needed
    requests = get_requests(filters)
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found")
    return requests

# READ ONE
@app.get("/requests/{request_id}", response_model=WeatherResponse)
def get_one_request(request_id: int):
    request = get_request_by_id(request_id)
    if "error" in request:
        raise HTTPException(status_code=404, detail=request["error"])
    return request

# UPDATE
@app.patch("/requests/{request_id}", response_model=WeatherResponse)
async def update_weather_request(request_id: int, request: WeatherRequestUpdate):
    updated_data = {}
    if request.location_input is not None:
        updated_data["location_input"] = request.location_input
    if request.start_date is not None:
        updated_data["start_date"] = request.start_date
    if request.end_date is not None:
        updated_data["end_date"] = request.end_date
    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated = update_request(request_id, updated_data)
    if "error" in updated:
        raise HTTPException(status_code=500, detail=updated["error"])
    return updated

# DELETE
@app.delete("/requests/{request_id}", status_code=204)
def delete_weather_request(request_id: int):
    deleted = delete_request(request_id)
    if "error" in deleted:
        raise HTTPException(status_code=500, detail=deleted["error"])
    return {"message": "Request deleted successfully"}

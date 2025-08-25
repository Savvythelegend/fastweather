# Weather Tracker API

A FastAPI-based weather tracking application that allows users to fetch and store weather forecasts for specific locations and date ranges. The application provides a simple web interface and RESTful API endpoints.

## Features

- Weather forecast retrieval using WeatherAPI.com
- Historical weather data storage and retrieval
- User-based request tracking
- Date range validation
- Responsive web interface
- RESTful API endpoints
- Supabase PostgreSQL database integration
- Row Level Security (RLS) for data access control

## Project Structure

```
weather-app/
├─ src/
│  ├─ main.py                # FastAPI app, routes
│  ├─ models.py              # Pydantic request/response models
│  ├─ db.py                  # Supabase client and database config
│  ├─ repositories.py        # CRUD functions
│  ├─ weather_client.py      # Weather API calls
│  ├─ services.py           # Business logic
│  └─ templates/
│     └─ index.html         # Web interface
├─ requirements.txt
├─ README.md
├─ .env.example             # Environment variables template
└─ demo_video_link.txt
```

## Prerequisites

- Python 3.8 or higher
- WeatherAPI.com API key
- Supabase account and project
- Supabase project URL and API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Savvythelegend/fastweather.git
   cd weather-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:
   ```bash
   cp .env.example .env
   ```
   Edit .env and add your:
   - WeatherAPI.com API key
   - Supabase Project URL
   - Supabase API key
   - Other configuration variables as needed

## Running the Application

1. Start the server:
   ```bash
   cd src
   uvicorn main:app --reload --host 0.0.0.0 --port 3000
   ```

2. Access the application:
   - Web Interface: http://localhost:3000
   - API Documentation: http://localhost:3000/docs

## API Endpoints

### POST /requests
Create a new weather forecast request

Request body:
```json
{
  "user_name": "string",
  "location_input": "string",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

### GET /requests/{user_name}
Retrieve all weather requests for a specific user

Response:
```json
[
  {
    "user_name": "string",
    "location": "string",
    "weather_data": {
      "location": "string",
      "forecast": [
        {
          "date": "YYYY-MM-DD",
          "temperature": number,
          "condition": "string"
        }
      ]
    }
  }
]
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid date ranges
- Invalid locations
- API rate limiting
- Database connection issues
- Missing or invalid API keys

## Development

This project uses several development tools:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- pytest for testing

To run the development tools:

```bash
# Format code
black src/
isort src/

# Type checking
mypy src/

# Run tests
pytest tests/
```

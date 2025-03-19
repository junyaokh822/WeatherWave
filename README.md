# Weather Wave

## Project Description

Weather Wave is a web application that provides current weather information and forecasts for any city using the OpenWeatherMap API. The application allows users to:

- Get the current weather for a specific city.
- View a 5-day weather forecast with optional temperature filters.
- Find the hottest or coldest day within the forecast period.
- Filter the forecast by specific weather conditions (e.g., clear sky, rain, snow).
- Calculate the average temperature over the forecast period.

The frontend is built using HTML, CSS, and JavaScript, while the backend is powered by Flask, a Python web framework.

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS
- OpenWeatherMap API Key

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/junyaokh822/weather-wave.git
   cd weather-wave

2. Install the required Python packages:

   ```bash
   pip install flask flask-cors requests

3. Obtain an OpenWeatherMap API Key:

- Go to OpenWeatherMap and sign up for a free account.

- Navigate to the API keys section in your account and generate a new API key.

- Replace the API_KEY variable in weather_api.py with your new API key.

    ```bash
    API_KEY = 'your_openweathermap_api_key_here'

4. Run the Flask application:

    ```bash
    python weather_api.py

5. Access the application:

    Open your web browser and navigate to http://127.0.0.1:5000/.


## API Details

### OpenWeatherMap API

The application uses the OpenWeatherMap API to fetch weather data. The following endpoints are used:

- Current Weather: https://api.openweathermap.org/data/2.5/weather

- 5-Day Forecast: https://api.openweathermap.org/data/2.5/forecast

### API Key Acquisition

To use the OpenWeatherMap API, you need to obtain an API key:

1. Sign up for a free account at OpenWeatherMap.

2. Once registered, navigate to the API keys section in your account.

3. Generate a new API key and replace the placeholder in the weather_api.py file with your key.

## How to Run the Program

1. Start the Flask server:
    ```bash
    python weather_api.py
2. Open your web browser:

    Navigate to http://127.0.0.1:5000/ to access the Weather Wave application.

3. Use the application:

- Enter a city name in the "City" field and click "Get Weather" to view the current weather.

- Use the "Weather Forecast" form to get a 5-day forecast, with optional temperature filters.

- Find the hottest or coldest day within the forecast period using the "Hottest / Coldest Day" form.

- Filter the forecast by specific weather conditions using the "Filter by Weather Condition" form.

- Calculate the average temperature over the forecast period using the "Calculate Average Temperature" form.

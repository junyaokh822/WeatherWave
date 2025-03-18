from flask import Flask, jsonify, request, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

API_KEY = '335a302c1e16d19f9502ce076aa973e0'  #OpenWeatherMap API Key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    params = {'q': city, 'appid': API_KEY, 'units': 'imperial'} # Change 'metric' to 'imperial'
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), response.status_code

    weather_data = response.json()

    result = {
        'city': weather_data.get('name'),
        'temperature': weather_data['main']['temp'],
        'weather_description': weather_data['weather'][0]['description'],
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data['wind']['speed']
    }

    return jsonify(result)

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    days = int(request.args.get('days', 5))
    min_temp = request.args.get('min_temp', None)
    max_temp = request.args.get('max_temp', None)
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    params = {'q': city, 'appid': API_KEY, 'units': 'imperial', 'cnt': days * 8}
    response = requests.get(FORECAST_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), response.status_code

    forecast_data = response.json()
    forecast_list = forecast_data['list']

    # Filter the forecast list if min_temp or max_temp is provided
    if min_temp is not None or max_temp is not None:
        min_temp = float(min_temp) if min_temp else -float('inf')
        max_temp = float(max_temp) if max_temp else float('inf')
        forecast_list = [
            entry for entry in forecast_list
            if min_temp <= entry['main']['temp'] <= max_temp
        ]

    processed_forecast = [
        {
            'date': entry['dt_txt'],
            'temperature': entry['main']['temp'],
            'weather_description': entry['weather'][0]['description'],
            'humidity': entry['main']['humidity'],
            'wind_speed': entry['wind']['speed']
        }
        for entry in forecast_list
    ]

    return jsonify({'city': forecast_data['city']['name'], 'country': forecast_data['city']['country'], 'forecast': processed_forecast})

@app.route('/extreme_day', methods=['GET'])
def get_extreme_day():
    city = request.args.get('city')
    days = int(request.args.get('days', 5))  # Default to 5 days
    type = request.args.get('type', 'hottest')  # Default to 'hottest'

    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    days = min(days, 5)

    # Prepare API request parameters
    params = {'q': city, 'appid': API_KEY, 'units': 'imperial', 'cnt': days * 8}
    response = requests.get(FORECAST_URL, params=params)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), response.status_code

    # Parse the forecast data
    forecast_data = response.json()
    forecast_list = forecast_data['list']

    # Find the hottest or coldest day
    if type == 'hottest':
        extreme_day = max(forecast_list, key=lambda x: x['main']['temp'])
    else:
        extreme_day = min(forecast_list, key=lambda x: x['main']['temp'])

    # Prepare the response
    result = {
        'city': forecast_data['city']['name'],
        'country': forecast_data['city']['country'],
        'type': type,
        'date': extreme_day['dt_txt'],
        'temperature': extreme_day['main']['temp'],
        'weather_description': extreme_day['weather'][0]['description'],
        'humidity': extreme_day['main']['humidity'],
        'wind_speed': extreme_day['wind']['speed']
    }

    return jsonify(result)

@app.route('/filter_by_condition', methods=['GET'])
def filter_by_condition():
    city = request.args.get('city')
    days = int(request.args.get('days', 5))
    condition = request.args.get('condition', '').lower()

    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    days = min(days, 5)

    params = {'q': city, 'appid': API_KEY, 'units': 'imperial', 'cnt': days * 8}
    response = requests.get(FORECAST_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), response.status_code

    forecast_data = response.json()
    forecast_list = forecast_data['list']

    # Filter entries based on the selected weather condition
    filtered_forecast = [
        entry for entry in forecast_list
        if condition in entry['weather'][0]['description'].lower()
    ]

    result = {
        'city': forecast_data['city']['name'],
        'country': forecast_data['city']['country'],
        'condition': condition,
        'forecast': [
            {
                'date': entry['dt_txt'],
                'temperature': entry['main']['temp'],
                'weather_description': entry['weather'][0]['description'],
                'humidity': entry['main']['humidity'],
                'wind_speed': entry['wind']['speed']
            }
            for entry in filtered_forecast
        ]
    }

    return jsonify(result)

@app.route('/average_temperature', methods=['GET'])
def get_average_temperature():
    city = request.args.get('city')
    days = int(request.args.get('days', 5))
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    days = min(days, 5)

    params = {'q': city, 'appid': API_KEY, 'units': 'imperial', 'cnt': days * 8}
    response = requests.get(FORECAST_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), response.status_code

    forecast_data = response.json()
    forecast_list = forecast_data['list']

    total_temp = sum(entry['main']['temp'] for entry in forecast_list)
    average_temp = total_temp / len(forecast_list)

    result = {
        'city': forecast_data['city']['name'],
        'country': forecast_data['city']['country'],
        'average_temperature': average_temp
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


# run python weather_api.py
# Go to website browser, copy and paste http://127.0.0.1:5000/




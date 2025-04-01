import unittest
import logging
from weather_api import app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='test_weather_api.log',  # Log file path
    filemode='w'  # Overwrite the log file every time the tests run
)

logger = logging.getLogger(__name__)

class WeatherApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        logger.info("Setup for test")

    def test_weather_invalid_city(self):
        logger.info("Running test_weather_invalid_city")
        response = self.app.get('/weather?city=invalidcityname123')
        message = "invalid city name"
        logger.info(f"Response status: {response.status_code}, data: {response.get_json()}")
        self.assertEqual(response.status_code, 200, message)
        self.assertIn('error', response.get_json())
        logger.info("test_weather_invalid_city passed")

    def test_average_temperature(self):
        logger.info("Running test_average_temperature")
        response = self.app.get('/average_temperature?city=Staten%20Island')
        logger.info(f"Response status: {response.status_code}, data: {response.get_json()}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('average_temperature', data)
        logger.info("test_average_temperature passed")

    def tearDown(self):
        logger.info("Tear down after test")

if __name__ == '__main__':
    unittest.main()

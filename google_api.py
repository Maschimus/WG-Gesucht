import requests
import api_keys

class GoogleAPI:
    @staticmethod
    def calculate_distance(origin, destination):
        # API endpoint for distance matrix
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json'

        # Set parameters for the API request
        params = {
            'origins': origin,
            'destinations': destination,
            'mode': 'bicycling',
            'key': api_keys.api_key
        }

        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()

        # Extract the distance value from the response
        distance = data['rows'][0]['elements'][0]['distance']['text']
        return distance
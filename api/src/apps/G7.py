from datetime import datetime, timedelta
import requests
import json

class G7():
    def __init__(self):
        self.header = {
            'origin': 'https://www.g7booking.com',
            'language': 'fr',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Basic RzdCOjEyMzQ1Njc4',
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://www.g7booking.com/tunnel/resultats',
            'consumername': 'Taxis+Paris',
            'authority': 'gateway.g7booking.com',
        }
        self.api_url = 'https://gateway.g7booking.com/services/structuredProducts'

    def get_estimation(self, from_, to, seat_count, iteration):
        if seat_count > 4:
            return {}
        date = datetime.now() + timedelta(minutes=5)
        payload = json.dumps({
            "dateTime": date.strftime("%Y-%m-%dT%H:%M:00.00+0200"),
            "nbPassengersAdult": seat_count,
            "nbPassengersChild":0,
            "nbPassengersBaby":0,
            "nbBaggagesLarge":0,
            "nbBaggagesMedium":0,
            "nbBaggagesSmall":0,
            "pickpointAddress": {
                "latitude": from_["coordinates"]["lat"],
                "longitude": from_["coordinates"]["long"]
            },
            "destinationAddress": {
                "latitude": to["coordinates"]["lat"],
                "longitude": to["coordinates"]["long"]
            }
        })
        estimations = {}
        response = requests.post(self.api_url, headers=self.header, data=payload)
        if response.status_code == 200:
            data = response.json()
            car_types = data["carTypes"]
            for product in data["products"]:
                for car_type in car_types:
                    if car_type["id"] == product["carType"]["id"]:
                        mode = car_type["label"]
                for partner in product["partners"]:
                    estimations[mode] = {
                        "price": partner["cost"],
                        "duration": partner["duration"] / 60,
                        "distance": partner["distance"] / 1000,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "iteration": iteration
                    }
            return estimations
        print("[Error] G7 API return {} {}".format(response.status_code, response.json()))
        return {}

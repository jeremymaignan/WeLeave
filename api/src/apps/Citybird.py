from datetime import datetime
import requests
import json
import logging

class Citybird():

    def __init__(self):
        self.api_url = 'https://api.classnco.com/api/v3/CityBird/passenger_requests'
        self.header = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://citybird.yusofleet.com/new_front',
            'Origin': 'https://citybird.yusofleet.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        self.available_seats = {
            "Moto": {
                "seats": 1,
                "id": 17
            },
            "Scooter": {
                "seats": 1,
                "id": 18
            },
            "E-Scooter": {
                "seats": 1,
                "id": 10
            }, 
            "Berline": {
                "seats": 4,
                "id": 4
            },
            "Van": {
                "seats": 7,
                "id": 6
            }
        }

    def get_estimation(self, address_pick_up, address_drop_off, seat_count, iteration, duration, distance):
        estimations = {}
        from_ = {
            "lat": address_pick_up["coordinates"]["lat"],
            "long": address_pick_up["coordinates"]["long"],
            "zip_code": address_pick_up["zip_code"],
            "name": address_pick_up["address"]
        }
        to = {
            "lat": address_drop_off["coordinates"]["lat"],
            "long": address_drop_off["coordinates"]["long"],
            "zip_code": address_drop_off["zip_code"],
            "name": address_drop_off["address"]
        }
        for mode, params in self.available_seats.items():
            if params["seats"] >= seat_count:
                payload = json.dumps({
                    "locale":"fr",
                    "address_pick_up": from_,
                    "address_drop_off": to,
                    "stops":[],
                    "package_types":[],
                    "channel": 2,
                    "type": 1,
                    "ride_date": datetime.now().strftime("%Y%m%dT%H:%M"), 
                    "vehicle_type": {
                        "id": params["id"]
                    },
                    "activeFreeRide": False,
                "options":[]
                })

                response = requests.post(self.api_url, headers=self.header, data=payload)
                if response.status_code == 201:
                    data = response.json()
                    estimations[mode] = {
                        "distance" : data["distance"] / 1000,
                        "duration" : data["duration"],
                        "price": data["customer_price"] / 100,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "iteration": iteration
                    }
                else:
                    logging.error("HiCab API return {} for mode {} [{}]".format(response.status_code, mode, response.json()['error']['message']))
        return estimations

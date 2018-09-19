from datetime import datetime
import requests
import json 

class Allocab():
    def __init__(self):
        self.api_url = {
            "create": "https://allocab-prod.appspot.com/_ah/api/anonymous/v2/booking/fare/create",
            "estimations": 'https://allocab-prod.appspot.com/_ah/api/anonymous/v2/booking/fare/panels'
        }
        self.header = {}
        #     "Accept": "application/json, text/plain, */*",
        #     "Referer": "https://www.allocab.com/widget-booker/",
        #     "Origin": "https://www.allocab.com",
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        #     "Content-Type": "application/json;charset=UTF-8" 
        # }
        self.available_seats = {
            "Berline classe affaires": 4,
            "Van classe éco": 7,
            "Moto prestige": 1,
            "Berline classe éco": 1
        }

    def create_ride(self, from_, to):
        payload = json.dumps({
            "startPosition": {
                "formattedAddress": from_,
            },
            "endPosition": {
                "formattedAddress": to,
            },
            "tripType": "DIRECTION",
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:00.000Z"),
            "flashFare": True,
            "timezone": "Europe/Paris",
            "session": None,
            "id": None,
            "adgroupid": None,
            "feeditemid": None,
            "source": "WEBAPP"
        })
        #            "date": "sam. 15 septembre 2018",
        response = requests.post(self.api_url["create"], headers=self.header, data=payload)
        if response.status_code == 200:
            data = response.json()
            return data["id"], data["instantFareToken"]
        print("[Error] Allocab API return {}".format(response.status_code))
        return None, None

    def get_estimation(self, from_, to, seat_count, iteration):
        estimations = {}
        id, token = self.create_ride(from_["address"], to["address"])
        if not id or not token:
            return {}
        payload = json.dumps({
            "fareId": id,
            "token": token,
            "timeout":{}
        })
        response = requests.post(self.api_url["estimations"], headers=self.header, data=payload)
        if response.status_code == 200:
            data = response.json()
            for estimation in data["items"]:
                if self.available_seats[estimation["name"]] >= seat_count:
                    if estimation["driverFound"]:
                        estimations[estimation["name"]] = {
                            "price": estimation["price"] / 100,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "iteration": iteration
                        }
            return estimations
        print("[Error] Allocab API return {}".format(response.status_code))
        return {}

# a = Allocab()
# print(a.get_estimations("5 Rue Joseph Rivi\\xe8re, Courbevoie, France", "4 Boulevard Haussmann, Paris-9E-Arrondissement, France", 60, 1))

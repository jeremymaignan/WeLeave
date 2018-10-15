import requests
import json
from datetime import datetime
import logging

from apps.Uber import Uber

class Taxify():
    def __init__(self):
        self.api_url = "https://ride.guru/api/fares.json"
        self.headers = {
            #'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            #'referer': 'https://ride.guru/estimate/5%20Rue%20Joseph%20Rivi%C3%A8re,%2092400%20Courbevoie,%20France/7%20Rue%20De%20Rivoli,%2075004%20Paris,%20France',
            'authority': 'ride.guru'
        }    

    def get_distance_and_duration(self, from_, to):
        u = Uber()
        distance, duration = u.get_distance_and_duration(from_, to)
        return distance, duration

    def get_estimation(self, from_, to, seat_count, iteration):
        if 4 < seat_count:
            return {}
        # Get distance and duration from Uber sdk
        distance, duration = self.get_distance_and_duration(from_, to)
        if not distance or not duration:
            logging.error("Cannot get duration and distance from uber sdk")
            return {}
        params = (
            ('start', '{},{}'.format(from_["coordinates"]["lat"], from_["coordinates"]["long"])),
            ('start_a', from_["address"]),
            ('end', '{},{}'.format(to["coordinates"]["lat"], to["coordinates"]["long"])),
            ('end_a', to["address"]),
            ('distance', str(distance)),
            ('duration', str(duration)),
        )
        response = requests.get(self.api_url,  headers=self.headers, params=params)
        if response.status_code != 200:
            logging.error("Taxify API return {} {}".format(response.status_code, response.json()))
            return {}
        # Get taxify data
        taxify_data = {}
        for mode in response.json()["fare_estimates"]:
            try:
                if mode["service"]["company"]["handle"] == "TAXIFY":
                    taxify_data = mode
                    break
            except:
                pass
        if not taxify_data:
            logging.error("Did not find Taxify in response")
            return {}
        return {
            "berline": {
                "price": round(taxify_data['total_fare'] * 1.1, 2),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "iteration": iteration
            }
        }
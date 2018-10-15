from utils.ConfManager import get_conf

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from datetime import datetime
import logging

class Uber():
    def __init__(self):
        self.token = get_conf("uber_app_id")
        self.available_seats = {
            "Pool": 2,
            "UberX": 4,
            "Green": 4,
            "Van": 6,
            "ACCESS": 4,
            "Berline": 4
        }

    def get_distance_and_duration(self, from_, to):
        session = Session(server_token=self.token)
        client = UberRidesClient(session)
        response = client.get_price_estimates(
            start_latitude= from_["coordinates"]["lat"],
            start_longitude= from_["coordinates"]["long"],
            end_latitude= to["coordinates"]["lat"],
            end_longitude= to["coordinates"]["long"],
            seat_count=2
        )
        response = response.json.get('prices')
        for mode in response:
            if "UberX" == mode["localized_display_name"]:
                return round(float(mode["distance"]) * 1.6093 * 1000.0, 2) , float(mode["duration"])
        return None, None

    def get_estimation(self, from_, to, seat_count, iteration):
        if seat_count > 2:
            seat_count_uber_format = 2
        else:
            seat_count_uber_format = seat_count
        session = Session(server_token=self.token)
        client = UberRidesClient(session)
        response = client.get_price_estimates(
            start_latitude= from_["coordinates"]["lat"],
            start_longitude= from_["coordinates"]["long"],
            end_latitude= to["coordinates"]["lat"],
            end_longitude= to["coordinates"]["long"],
            seat_count=seat_count_uber_format
        )
        estimations = {}
        response = response.json.get('prices')
        for mode in response:
            if self.available_seats[mode["localized_display_name"]] >= seat_count:
                estimations[mode["localized_display_name"]] = {
                    "price": (int(mode["low_estimate"]) + int(mode["high_estimate"])) / 2.0,
                    "distance": mode["distance"],
                    "duration": mode["duration"] / 60,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "iteration": iteration
                }
        return estimations



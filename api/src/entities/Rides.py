from datetime import datetime

from utils.Geo import Geo
from utils.ConfManager import get_conf

class Rides:
    def __init__(self, data):
        geo = Geo()
        from_geopos = geo.get_geoloc(data["from"]["address"])
        if {} == from_geopos:
            print("[ERROR] Cannot find coordinates for {}".format(data["from"]["address"])) 
            self.ride = None
            return
        to_geopos = geo.get_geoloc(data["to"]["address"])
        if {} == to_geopos:
            print("[ERROR] Cannot find coordinates for {}".format(data["to"]["address"])) 
            self.ride = None
            return
        self.ride = {
            "user_id": data["user_id"],
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "start_at": data["start_at"],
            "from": {
                "address": data["from"]["address"],
                "zip_code": data["from"]["zip_code"],
                "coordinates": from_geopos
            },
            "to": {
                "address": data["to"]["address"],
                "zip_code": data["to"]["zip_code"],
                "coordinates": to_geopos
            },
            "iteration": {
                "todo": get_conf("number_of_iteration"),
                "done": 0
            },
            "status": "pending",
            "seat_count": data["number_seat"],
            "prices": {
            }
        }
    
    def get_ride(self):
        return self.ride

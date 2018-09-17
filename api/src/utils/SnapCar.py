from datetime import datetime
import requests

class SnapCar():
    def __init__(self):
        self.api_url = "https://www.snapcar.com/price.php"
        self.available_seats = {
            "executive": 4,
            "classic": 4,
            "van": 6
        }
    
    def get_estimation(self, from_, to, seat_count, iteration):
        payload = {
            "start_lng": from_["coordinates"]["long"],
            "start_lat": from_["coordinates"]["lat"],
            "end_lng": to["coordinates"]["long"],
            "end_lat": to["coordinates"]["lat"]
        }
        response = requests.post(self.api_url, data=payload)
        if response.status_code == 200:
            response = response.json()
            estimations = {}
            for mode in response:
                if self.available_seats[mode] >= seat_count:
                    estimations[mode] = {
                        "price": int(response[mode].split(' ')[0]),
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "iteration": iteration
                    }
            return estimations
        print("[Error] Snapcar API return {}".format(response.status_code))
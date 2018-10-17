import requests
from datetime import datetime
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Drive():
    def __init__(self):
        self.api_url = 'https://www.drive.gt/order/getPrice/'
        self.header = {
            'Origin': 'https://www.drive.gt',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.drive.gt/order/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        self.available_seats = {
            "Premium": {
                "seats": 4,
                "id": '1'
            },
            "Van": {
                "seats": 6,
                "id": '5'
            }
        }

    def get_estimation(self, from_, to, nb_seats, iteration):
        estimations = {}
        for mode, params in self.available_seats.items():
            if params["seats"] >= nb_seats:
                paylaod = {
                    'OrderForm[vehicle_type]': params["id"],
                    'OrderForm[fromAdr]': from_["address"],
                    'OrderForm[toAdr]': to["address"],
                    'OrderForm[transacType]': 'OFFLINE',
                    'OrderForm[useCredit]': '0',
                    'OrderForm[fromAirport]': '',
                    'OrderForm[toAirport]': '',
                    'OrderForm[messageDriver]': ''
                }
                response = requests.post(self.api_url, headers=self.header, data=paylaod, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    estimations[mode] = {
                        "price": data["price"],
                        "distance": data["distance"],
                        "duration": data["time"],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "iteration": iteration
                    }
                else: 
                    logging.error("Drive API return {}".format(response.status_code))        
        return estimations
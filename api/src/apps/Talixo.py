import requests
import json
from datetime import datetime, timedelta

class Talixo():
    def __init__(self):
        self.api_url = "https://ride.guru/api/fares.json"
        self.headers = {
            #'cookie': '_ga=GA1.2.1862728486.1539694466; _gid=GA1.2.153801215.1539694466; _gac_UA-38999325-1=1.1539694466.CjwKCAjwmJbeBRBCEiwAAY4VVb_HLWGMIlXjO0I_-HxTXZmT7swe6w9N8qPQwL7L7qEXGzU3RptZcxoCHS0QAvD_BwE; _gac_UA-38999325-16=1.1539694466.CjwKCAjwmJbeBRBCEiwAAY4VVb_HLWGMIlXjO0I_-HxTXZmT7swe6w9N8qPQwL7L7qEXGzU3RptZcxoCHS0QAvD_BwE; _gac_UA-111271718-1=1.1539694466.CjwKCAjwmJbeBRBCEiwAAY4VVb_HLWGMIlXjO0I_-HxTXZmT7swe6w9N8qPQwL7L7qEXGzU3RptZcxoCHS0QAvD_BwE; _pk_ref.1.f135=%5B%22search%22%2C%22%22%2C1539694467%2C%22https%3A%2F%2Fwww.google.fr%2F%22%5D; _pk_id.1.f135=76265d04f956dfa2.1539694467.1.1539694467.1539694467.; _pk_ses.1.f135=*; _hjIncludedInSample=1; __zlcmid=ouhiiXjwH9o2qM; _gat=1',
            'origin': 'https://talixo.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'content-type': 'application/json',
            'accept': 'application/json',
            #'referer': 'https://talixo.com/airport-taxi-paris-orly/?utm_source=search&utm_keyword=&device=c&creative=0&gclid=CjwKCAjwmJbeBRBCEiwAAY4VVb_HLWGMIlXjO0I_-HxTXZmT7swe6w9N8qPQwL7L7qEXGzU3RptZcxoCHS0QAvD_BwE',
            'authority': 'talixo.com',
            'x-requested-with': 'XMLHttpRequest',
        }    

    def get_address_id(self, address):
        params = (
            ('address', address),
            ('house_number', ''),
            ('iata_code', ''),
        )
        response = requests.get('https://talixo.com/geo/get_talixo_id/', headers=self.headers, params=params)
        if 200 == response.status_code:
            return response.json()["talixo_id"]
        return None
    
    def get_estimation(self, from_, to, seat_count, iteration):
        # Get addresses id
        from_id = self.get_address_id(from_["address"])
        to_id = self.get_address_id(to["address"])
        if not from_id or not to_id:
            print("Cannot get id of addresses")
            return {}
        print(from_id, to_id)



        payload = json.dumps({
            "start_time_date": (datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d"),
            "start_time_time": (datetime.now() + timedelta(hours=12)).strftime("%H:%M"),
            "passengers": seat_count,
            "animals": 0,
            "luggage": 0,
            "sport_luggage": 0,
            "start_talixo_id": "b0cb59f7fcf68633962a4e66631b3b7b54ca15c56d8045487bfee446",  
            "end_talixo_id": "d04d78918acd4fe90c1491e57929894c2c4fdb318162dc1905043425",
            "terms": False,
            "promo_code": "AdWords18",
            "affiliate_reference": None
        })
        response = requests.post('https://talixo.com/en/mapi/vehicles/booking_query/', headers=self.headers, data=payload)
        if response.status_code != 200:
            print("Cannot get estimations from Talixo")
            return {}
        data = response.json()
        limo = data["limousines"]
        estimations = {}
        for item in limo:
            estimations[item["extended_booking_category"].replace("_", " ").capitalize()] =  {
                "distance": data["distance"],
                "price": item["discount_price"],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "iteration": iteration
            }
        return estimations
        
# t = Talixo()
# a = t.get_estimation(
#     {"address": "5 rue joseph riviere courbevoie"},
#     {"address": "8 rue de rivoli paris"},
#     1,
#     1)

# print(a)
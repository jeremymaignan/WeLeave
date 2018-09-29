from datetime import datetime
import requests
import json
import logging 

class LeCab():

    def __init__(self):
        self.api_url = 'https://book.lecab.fr/sherbook/calculate/price'
        self.header = {
            'origin': 'https://book.lecab.fr',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://book.lecab.fr/portal/',
            'authority': 'book.lecab.fr',
            'cookie': 'JSESSIONID=2F42FDA8407EC98A4D8BC5611D342F64.node2; __cfduid=df916ce61b7bddabc46c668589c1d632f1534095002; _ga=GA1.2.2144266183.1536335773; commercialOffers_timeout=1567871775287; statistical_timeout=1565193375288; cb-enabled=accepted; _gcl_au=1.1.1661671262.1538145718; _gcl_aw=GCL.1538145718.CjwKCAjworfdBRA7EiwAKX9HeDuWaHOuwgAFr3MRB6TcaNUnn98UwL4185EXDS3fFvt0Di7Sbk2scRoCJcUQAvD_BwE; _gid=GA1.2.1846009235.1538145719; _gac_UA-36208134-4=1.1538145719.CjwKCAjworfdBRA7EiwAKX9HeDuWaHOuwgAFr3MRB6TcaNUnn98UwL4185EXDS3fFvt0Di7Sbk2scRoCJcUQAvD_BwE; _gac_UA-36208134-6=1.1538145764.CjwKCAjworfdBRA7EiwAKX9HeDuWaHOuwgAFr3MRB6TcaNUnn98UwL4185EXDS3fFvt0Di7Sbk2scRoCJcUQAvD_BwE; WUF=eJwFwYENwCAMA7CTKEla2n0zCZB2w8Tv2N9vTyYXyrzWJMIGXNSLKhO4pdad2eUjdC4j8QuB; _ga=GA1.3.2144266183.1536335773; _gid=GA1.3.1846009235.1538145719; _gac_UA-36208134-6=1.1538145764.CjwKCAjworfdBRA7EiwAKX9HeDuWaHOuwgAFr3MRB6TcaNUnn98UwL4185EXDS3fFvt0Di7Sbk2scRoCJcUQAvD_BwE; _scid=d6571edc-11bc-42a9-a27d-c20b1a37a888; _dc_gtm_UA-36208134-6=1; _sp_ses.4a46=*; _sp_id.4a46=50bf359d-b113-4872-8c03-06f4cf7d3c96.1538145779.2.1538212378.1538145805.4fd9dd40-7042-414c-b2ab-5ffe7a86cb73',
            'api-version': '2.3',
        }
        self.available_seats = {
            "Berline": {
                "seats": 4,
                "id": "65bff4bc-6fb8-4a1f-a31e-aa2f0ff36bdc"
            },
            "Van": {
                "seats": 7,
                "id": "6153a7d3-d400-4e81-97a2-3f4caa13aa6a"
            }
        }

    def get_estimation(self, address_pick_up, address_drop_off, seat_count, iteration):
        estimations = {}
        for mode, params in self.available_seats.items():
            if params["seats"] >= seat_count:
                payload = json.dumps({
                    "requestId": "52135c8f-8475-4025-b8e5-316fe32567a4",
                    "routeInfo": {
                        "waitAndReturn": False,
                        "destinationUnknown": False,
                        "asDirected": False,
                        "asDirectedMinutes": None
                    },
                    "service": {
                        "availablePaymentTypes": ["CREDIT_CARD"],
                        "customerType": "ANONYMOUS",
                        "id": params["id"],
                        "caption": "LECAB",
                        "description": mode,
                        "pricePrefix": None
                    },
                    "paymentType": {
                        "customerType": "ANONYMOUS",
                        "name": "Carte de cr\\xe9dit",
                        "code": "CREDIT_CARD",
                        "description": "",
                        "defaultType": True,
                        "creditCardsAvailable": True,
                        "cvcRequiredForNewCreditCards": True,
                        "cvcRequiredForExistingCreditCards": False,
                        "merchantIdentifier": None
                    },
                    "instructions": [],
                    "operationType": "CREATE",
                    "asap": True,
                    "date": None,
                    "stops": [{
                        "address": {
                            "addressId": None,
                            "caption": address_pick_up["address"],
                            "latitude": address_pick_up["coordinates"]["lat"],
                            "longitude": address_pick_up["coordinates"]["long"],
                            "source": "GOOGLE_GEO",
                            "data": "QURSe0ZMRDF7NX1GTEQye1J1ZSBKb3NlcGggUml2acOocmV9RkxEM3s5MjQwMH1GTEQ0e0NvdXJiZXZvaWV9RkxENXvDjmxlLWRlLUZyYW5jZX1GTEQ2e0ZyYW5jZX1GUk17NSBSdWUgSm9zZXBoIFJpdmnDqHJlLCA5MjQwMCBDb3VyYmV2b2llfX0=",
                            "note": None,
                            "fields": None,
                            "available": None
                        },
                        "arrivalDetails": None,
                        "contact": None,
                        "id": None,
                        "notes": None
                    }, {
                        "address": {
                            "addressId": "1d17e78d-cd21-4c71-6a53-63b9cc0a40e0",
                            "caption": address_drop_off["address"],
                            "latitude": address_drop_off["coordinates"]["lat"],
                            "longitude": address_drop_off["coordinates"]["long"],
                            "source": "SPECIAL_PLACE",
                            "data": "TUNOe3RheGkkU3BlY2lhbFBsYWNlfUlEezFkMTdlNzhkLWNkMjEtNGM3MS02YTUzLTYzYjljYzBhNDBlMH0=",
                            "note": None,
                            "fields": None,
                            "available": None
                        },
                        "arrivalDetails": None,
                        "contact": None,
                        "id": None,
                        "notes": None
                    }],
                    "customerType": "ANONYMOUS"
                })

                response = requests.post(self.api_url, headers=self.header, data=payload)
                if response.status_code == 200:
                    data = response.json()
                    try:
                        estimations[mode] = {
                            "distance" : data["priceIncreaseDetails"]["distance"],
                            #"duration" : data["duration"],
                            "price": data["price"]["gross"]["value"],
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "iteration": iteration
                        }
                    except Exception as err:
                        logging.error("LeCab API return {} [{}]".format(response.status_code, data["errorMessage"]))
                else:
                    logging.error("LeCab API return {} [{}]".format(response.status_code, data["errorMessage"]))
        return estimations
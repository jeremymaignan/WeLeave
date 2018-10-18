from datetime import datetime, timedelta
import requests
import json
import logging
import bs4 as BeautifulSoup

class Backlane():

    def __init__(self):
        self.api_url = 'https://www.blacklane.com/fr/booking_requests/transfers/vehicle_class'
        self.header = {
            'authority': 'www.blacklane.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://www.blacklane.com/fr?booking_request%5Bat_date%5D=2018-10-17&booking_request%5Bat_time%5D=11%3A15&booking_request%5Bdropoff%5D=8+Rue+de+Rivoli%2C+Paris%2C+France&booking_request%5Bdropoff_place_id%5D=ChIJszk8if1x5kcRKwKtmO1OErw&booking_request%5Bpickup%5D=5+Rue+Joseph+Rivi%C3%A8re%2C+Courbevoie%2C+France&booking_request%5Bpickup_place_id%5D=ChIJQdMUjaFl5kcRh6ti5Cf4NnM&error=api.errors.messages.depart_at_too_early&model_class=BookingRequests%3A%3ATransfer',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            #'cookie': 'viewedOuibounceModal=true; AWSELB=8D1F815B1C2DF7C4974A1E3277C08A7CA4A855877588D56DA03CAB50010D39A142FA3C796E6E2E228609D19741B870EBB0FB920004082119F75683C581DAD20B1679D8AD29; optimizelyEndUserId=oeu1539701412259r0.9004784585370578; _gcl_au=1.1.119915759.1539701413; blcookie=1; _ga=GA1.2.1111922356.1539701413; _gid=GA1.2.918456373.1539701413; rmStore=amid:43404; raygun4js-userid=b4357157-f3e3-3143-247d-e21054fc1351; _ym_uid=1539701417847081685; _ym_d=1539701417; _ym_isad=1; _gcl_aw=GCL.1539701480.CjwKCAjwmJbeBRBCEiwAAY4VVZcTGmIK4bBWzWQB8HY_SmRel19UgGoqbpMOIEgg5MsQcfTlrM4g9hoC7mAQAvD_BwE; _gac_UA-26582165-13=1.1539701484.CjwKCAjwmJbeBRBCEiwAAY4VVZcTGmIK4bBWzWQB8HY_SmRel19UgGoqbpMOIEgg5MsQcfTlrM4g9hoC7mAQAvD_BwE; wisepops_props=%7B%22voucher_percentage%22%3A5%7D; wisepops_visits=%5B%222018-10-16T14%3A51%3A32.884Z%22%5D; bl_sdses.506c=*; _aphrodite_session=bnNVZWNyeEpXN3NoaUVSMDZnZGNtUTd4NHIzcWREUjhEY2d6elNsTVh3RUVrbEJqdXRDR2lDTFZzKy83aDAzT09QbnMwTGZzSGRwTUJ0V01RWFNqZUN3bXdoYjdqY1lEMUFwQklDdDFibi9RSWF0NXV3cy9XRlZlc3Rjc3EwNUdNdkxPbHhobUtENnpvWnhmeFJXaElCMGhhS3UxMzU0eCtPRmdLa0huZzQ5NEpVNGFRNTNzUDIwUFBLaW5SVjMvLS1WNFRaNExYWnhYdUtQeHYrRmNwUjVnPT0%3D--539216c30f0ded90d6a0c68af91e1bcb537188be; _dc_gtm_UA-26582165-13=1; _gat_UA-26582165-13=1; wisepops=%7B%22cross_subdomain%22%3Atrue%2C%22last_req_date%22%3Anull%2C%22popins%22%3A%7B%22123213%22%3A%7B%22display_count%22%3A5%2C%22display_date%22%3A%222018-10-17T08%3A20%3A34.911Z%22%7D%7D%2C%22ucrn%22%3A94%2C%22uid%22%3A%2233272%22%2C%22version%22%3A3%7D; wisepops_session=%7B%22arrivalOnSite%22%3A%222018-10-17T08%3A17%3A54.282Z%22%2C%22mtime%22%3A%222018-10-17T08%3A20%3A34.911Z%22%2C%22pageviews%22%3A4%2C%22popins%22%3A%7B%22123213%22%3A0%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%7D; stc115416=env:1539764101%7C20181117081501%7C20181017085039%7C10%7C1049871:20191017082039|uid:1539701413474.1585947801.4574318.115416.1572158206:20191017082039|srchist:1049864%3A1%3A20181116145013%7C1049871%3A1539764101%3A20181117081501:20191017082039|tsa:1506029389:20181017085039; bl_sdid.506c=02e2b323c987d7ed.1539701413.2.1539764445.1539701413',
        }
        self.available_seats = {
            "Business Class": {
                "seats": 3
            },
            "Green Class": {
                "seats": 3
            },
            "Business Van/SUV": {
                "seats": 5
            }, 
            "First Class": {
                "seats": 3
            }
        }

    def get_estimation(self, address_pick_up, address_drop_off, seat_count, iteration):
        estimations = {}
        params = (
            ('utf8', '\u2713'),
            ('booking_request[pickup_uuid]', ''),
            ('booking_request[pickup_airport_iata]', ''),
            #('booking_request[pickup_place_id]', 'ChIJQdMUjaFl5kcRh6ti5Cf4NnM'),
            ('booking_request[dropoff_uuid]', ''),
            ('booking_request[dropoff_airport_iata]', ''),
            #('booking_request[dropoff_place_id]', 'ChIJszk8if1x5kcRKwKtmO1OErw'),
            ('booking_request[pickup]', address_pick_up["address"]),
            ('booking_request[dropoff]', address_drop_off["address"]),
            ('booking_request[at_date]', (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d")),
            ('booking_request[at_time]', (datetime.now() + timedelta(hours=12)).strftime("%H:%M")),
        )
        response = requests.get(self.api_url, headers=self.header, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup.BeautifulSoup(response.text, features="html.parser")
            for i in soup.find_all('div'):
                price = 0
                mode = ""
                try:
                    if u'vehicle' in i["class"]:
                        for a in i.find_all('div'):
                            if "vehicle-title__name" in a["class"]:
                                if self.available_seats[a.text]["seats"] >= seat_count:
                                    mode = a.text
                            if 'vehicle-price-box__price' in a["class"]:
                                price = float(a.text.split(" ")[0].replace(",", "."))
                            if mode != "" and price != 0:
                                estimations[mode] = {
                                    "price": price,
                                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "iteration": iteration
                                }
                                break
                except:
                    pass
        else:
            print("Backlane API return {}".format(response.status_code))
        return estimations


# b = Backlane()
# e = b.get_estimation(
#     {"address": "5 rue joseph riviere courbevoie"},
#     {"address": "8 rue de rivoli paris"},
#     4,1
# )
# print(e)

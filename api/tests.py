import requests

hostname = "http://35.158.219.60:5000"

def create_job():
    payload = {
        "from": {
            "address": "5 rue joseph riviere courbevoie",
            "zip_code": "92400"
        },
        "to": {
            "address": "5 rue joseph riviere courbevoie",
            "zip_code": "92400"
        },
        "number_seat": 2,
        "user_id": "jeremy",
        "start_at": "2018-09-13 21:40:18"
    }
    res = requests.post("{}/rides".format(hostname), json=payload)
    if 201 == res.status_code:
        print("Create ride [OK]")
        return res.json()["id"]
    else:
        print("Create ride [KO]")
        return None

def get_estimation(id):
    res = requests.get("{}/rides/{}?size=10&update=True&apps=*".format(hostname, id))
    if 200 == res.status_code:
        print("Get estimation [OK]")
        return True
    else:
        print("Get estimation [KO]")
        return False

def get_user():
    res = requests.get("{}/users/jeremy".format(hostname))
    if 200 == res.status_code:
        print("Get user [OK]")
        return True
    else:
        print("Get user [KO]")
        return False

def get_app():
    res = requests.get("{}/apps".format(hostname))
    if 200 == res.status_code:
        print("Get app [OK]")
        return True
    else:
        print("Get app [KO]")
        return False

id = create_job()
if id:
    get_estimation(id)
get_user()
get_app()
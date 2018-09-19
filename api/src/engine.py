from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf

from apps.Uber import Uber
from apps.Marcel import Marcel

from apps.SnapCar import SnapCar
from apps.Allocab import Allocab
from apps.G7 import G7
from apps.Drive import Drive
from apps.HiCab import HiCab
from apps.Felix import Felix

from datetime import datetime
from pprint import pprint

# def get_last_min_max(iteration, job, mode_name, new):
#     if 0 == iteration:
#         min_ = new["average"]
#         max_ = new["average"]
#     else:
#         last = job["prices"]["uber"][mode_name][-1]
#         if new["average"] < last["min"]:
#             print("[INFO] {} new min {}".format(mode_name, new["average"]))
#             min_ = new["average"]
#         else:
#             min_ = last["min"]
#         if new["average"] > last["max"]:
#             print("[INFO] {} new max {}".format(mode_name, new["average"]))
#             max_ = new["average"]
#         else:
#             max_ = last["max"]
#     return min_, max_

# def get_trends(iteration, job, mode_name, new):
#     if 0 == iteration:
#         dynamic = 0.0
#         global_ = 0.0
#     else:
#         dynamic = new["average"] - job["prices"]["uber"][mode_name][-1]["average"]
#         global_ = new["average"] - job["prices"]["uber"][mode_name][0]["average"]
#     return dynamic, global_

def algo():
    print("[INFO] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mongo = Mongodb()
    providers = {
        "uber": Uber(),
        "marcel": Marcel(),
        "snapcar": SnapCar(),
        "allocab": Allocab(),
        "g7": G7(),
        "drive": Drive(),
        "hicab": HiCab(),
        "felix": Felix()
    }

    jobs = mongo.get_pending_jobs(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for job in jobs:
        iteration = job["iteration"]["done"]
        print("[INFO] {} [{}] Seats: {} ".format(job["_id"], iteration + 1, job["seat_count"]))

        for provider_name, provider in providers.items():
            # Create key in dict
            if provider_name not in job["prices"].keys():
                job["prices"][provider_name] = {}
            print("- {}".format(provider_name.capitalize() ))
            # Get estimations
            data = provider.get_estimation(job["from"], job["to"], job["seat_count"], iteration)
            for mode, estimation in data.items():
                if mode not in job["prices"][provider_name].keys():
                    job["prices"][provider_name][mode] = []
                job["prices"][provider_name][mode].append(estimation)

        job["iteration"]["todo"] -= 1
        job["iteration"]["done"] += 1
        if 0 == job["iteration"]["todo"]:
            job["status"] = "done"
        mongo.update_item(job)
algo()

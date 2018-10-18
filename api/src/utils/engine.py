from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf
from bson import ObjectId
import logging

from apps.Uber import Uber
from apps.Marcel import Marcel
from apps.SnapCar import SnapCar
from apps.Allocab import Allocab
from apps.G7 import G7
from apps.Drive import Drive
from apps.Citybird import Citybird
from apps.Felix import Felix
from apps.LeCab import LeCab
from apps.Taxify import Taxify
from apps.Talixo import Talixo
from apps.Backlane import Backlane

def get_fresh_estimation(job_id, asynch):
    mongo = Mongodb('rides')
    job = mongo.get_item({"_id": ObjectId(job_id)})
    if job["status"] == "done":
        logging.info("Ride is already done")
        return 200
    if not job:
        logging.error('Job {} not found in DB'.format(job_id))
        return 404
    providers = {
        "uber": Uber(),
        "marcel": Marcel(),
        "snapcar": SnapCar(),
        "allocab": Allocab(),
        "g7": G7(),
        "drive": Drive(),
        "citybird": Citybird(),
        "felix": Felix(),
        #"lecab": LeCab(),
        "taxify": Taxify(),
        "talixo": Talixo(),
        "backlane": Backlane()
    }

    iteration = job["iteration"]["done"]
    logging.info("[{}] Iter: {} Seats: {} ".format(job["_id"], iteration + 1, job["seat_count"]))

    for provider_name, provider in providers.items():
        # Create key (app_name) in dict
        if provider_name not in job["prices"].keys():
            job["prices"][provider_name] = {}
        logging.info("{}".format(provider_name.capitalize() ))
        # Get estimations
        data = provider.get_estimation(job["from"], job["to"], job["seat_count"], iteration)
        for mode, estimation in data.items():
            # Create key (mode) in dict
            if mode not in job["prices"][provider_name].keys():
                job["prices"][provider_name][mode] = []
            job["prices"][provider_name][mode].append(estimation)
            if asynch:
                mongo.update_item(job)
            
    # Increase iteration
    job["iteration"]["todo"] -= 1
    job["iteration"]["done"] += 1
    if 0 == job["iteration"]["todo"]:
        job["status"] = "done"

    mongo_response = mongo.update_item(job)
    if str(job_id) != str(mongo_response):
        logging.error("Cannot update job in DB. Error: {}".format(mongo_response))
        return 500
    logging.info("{} [{}] Estimations updated".format(job["_id"], job["iteration"]["done"]))
    return 200



# def get_last_min_max(iteration, job, mode_name, new):
#     if 0 == iteration:
#         min_ = new["price"]
#         max_ = new["price"]
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
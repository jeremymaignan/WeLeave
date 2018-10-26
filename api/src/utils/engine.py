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

def get_providers():
    return {
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

def get_min_and_max(estimations, new_price):
    if [] == estimations:
        return new_price, new_price
    last_estimation = estimations[-1]
    if last_estimation["max"] > new_price:
        max = last_estimation["max"]
    else:
        max = new_price
    if last_estimation["min"] <  new_price:
        min = last_estimation["min"]
    else:
        min = new_price
    return min, max

def get_trends(estimations, new_price):
    if [] == estimations:
        return 0.0, 0.0
    first_estimation = estimations[0]
    last_estimation = estimations[-1]
    
    dynamic = round(new_price - last_estimation["price"], 2)
    global_ = round(new_price - first_estimation["price"], 2)
    return dynamic, global_

def get_fresh_estimation(job_id, asynch):
    mongo = Mongodb('rides')
    job = mongo.get_item({"_id": ObjectId(job_id)})
    if job["status"] == "done":
        logging.info("Ride is already done")
        return 200
    if not job:
        logging.error('Job {} not found in DB'.format(job_id))
        return 404
    providers = get_providers()

    iteration = job["iteration"]["done"]
    logging.info("[{}] Iter: {} Seats: {} ".format(job["_id"], iteration + 1, job["seat_count"]))
    duration = job["duration"]
    distance = job["distance"]
    for provider_name, provider in providers.items():
        # Create key (app_name) in dict
        if provider_name not in job["prices"].keys():
            job["prices"][provider_name] = {}
        logging.info("{}".format(provider_name.capitalize() ))
        # Get estimations
        data = provider.get_estimation(job["from"], job["to"], job["seat_count"], iteration, duration, distance)
        for mode, estimation in data.items():
            # Create key (mode) in dict
            if mode not in job["prices"][provider_name].keys():
                job["prices"][provider_name][mode] = []
            # Calculate min & max
            min, max = get_min_and_max(job["prices"][provider_name][mode], estimation["price"]) 
            estimation["min"] = min
            estimation["max"] = max
            # Calculate trends
            dynamic, global_ = get_trends(job["prices"][provider_name][mode], estimation["price"])
            estimation["dynamic_trends"] = dynamic
            estimation["global_trends"] = global_
            # Save new estimation
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

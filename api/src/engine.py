from utils.Mongodb import Mongodb
from utils.Uber import Uber
from utils.ConfManager import get_conf

from datetime import datetime
from pprint import pprint

def get_last_min_max(last, new):
    if new["average"] < last["min"]:
        print("[INFO] New min {}".format(new["average"]))
        min_ = new["average"]
    else:
        min_ = last["min"]
    if new["average"] > last["max"]:
        print("[INFO] New max {}".format(new["average"]))
        max_ = new["average"]
    else:
        max_ = last["max"]
    return min_, max_

def algo():
    print("[INFO] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mongo = Mongodb()
    uber = Uber()
    jobs = mongo.get_pending_jobs()
    for job in jobs:
        iteration = get_conf("number_of_iteration") - job["iteration"] + 1
        print("[INFO] {} iter: {}".format(job["_id"], iteration))
        res = uber.get_estimation(job["from"]["coordinates"], job["to"]["coordinates"], job["seat_count"])
        for mode_name, mode in res["modes"].items():
            d = {
                "iteration": iteration,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "low": mode["prices"]["low"],
                "high": mode["prices"]["high"],
                "average": mode["prices"]["estimation"]
            }
            if 1 == iteration:
                d["min"] = d["average"]
                d["max"] = d["average"]
            else:
                min_, max_ = get_last_min_max(job["prices"]["uber"][mode_name][-1], d)
                d["min"] = min_
                d["max"] = max_
            print(d)
            if "uber" not in job["prices"].keys():
                job["prices"]["uber"] = {}
            if mode_name not in job["prices"]["uber"].keys():
                job["prices"]["uber"][mode_name] = []
            job["prices"]["uber"][mode_name].append(d)
        job["iteration"] -= 1
        if 0 == job["iteration"]:
            job["status"] = "done"
        mongo.update_item(job)
algo()

from utils.Mongodb import Mongodb
from utils.Uber import Uber
from utils.ConfManager import get_conf

from datetime import datetime
from pprint import pprint

def get_last_min_max(iteration, job, mode_name, new):
    if 0 == iteration:
        min_ = new["average"]
        max_ = new["average"]
    else:
        last = job["prices"]["uber"][mode_name][-1]
        if new["average"] < last["min"]:
            print("[INFO] {} new min {}".format(mode_name, new["average"]))
            min_ = new["average"]
        else:
            min_ = last["min"]
        if new["average"] > last["max"]:
            print("[INFO] {} new max {}".format(mode_name, new["average"]))
            max_ = new["average"]
        else:
            max_ = last["max"]
    return min_, max_

def get_trends(iteration, job, mode_name, new):
    if 0 == iteration:
        dynamic = 0.0
        global_ = 0.0
    else:
        dynamic = new["average"] - job["prices"]["uber"][mode_name][-1]["average"]
        global_ = new["average"] - job["prices"]["uber"][mode_name][0]["average"]
    return dynamic, global_

def algo():
    print("[INFO] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mongo = Mongodb()
    uber = Uber()
    jobs = mongo.get_pending_jobs(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for job in jobs:
        if "uber" not in job["prices"].keys():
            job["prices"]["uber"] = {}
            
        iteration = job["iteration"]["done"]

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
            d["min"], d["max"] = get_last_min_max(iteration, job, mode_name, d)
            d["dynamic_trend"], d["global_trend"] = get_trends(iteration, job, mode_name, d)

            if mode_name not in job["prices"]["uber"].keys():
                job["prices"]["uber"][mode_name] = []
            job["prices"]["uber"][mode_name].append(d)
        job["iteration"]["todo"] -= 1
        job["iteration"]["done"] += 1
        if 0 == job["iteration"]["todo"]:
            job["status"] = "done"
        mongo.update_item(job)
algo()

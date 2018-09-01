from utils.Mongodb import Mongodb
from utils.Uber import Uber
from utils.ConfManager import get_conf

from datetime import datetime
from pprint import pprint

def algo():
    print("[INFO] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mongo = Mongodb()
    uber = Uber()
    jobs = mongo.get_pending_jobs()
    if 0 == jobs.count():
        print("[INFO] No pending jobs")
        return
    for job in jobs:
        print("[INFO] {} iter: {}".format(job["_id"], get_conf("number_of_iteration") - job["iteration"] + 1))
        res = uber.get_estimation(job["from"]["coordinates"], job["to"]["coordinates"], job["seat_count"])
        for mode in res["modes"]:
            d = {
                "iteration": get_conf("number_of_iteration") - job["iteration"],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "low": res["modes"][mode]["prices"]["low"],
                "high": res["modes"][mode]["prices"]["high"],
                "average": res["modes"][mode]["prices"]["estimation"]
            }
            if "uber" not in job["prices"].keys():
                job["prices"]["uber"] = {}
            if mode not in job["prices"]["uber"].keys():
                job["prices"]["uber"][mode] = []
            job["prices"]["uber"][mode].append(d)
        job["iteration"] -= 1
        if 0 == job["iteration"]:
            job["status"] = "done"
        mongo.update_item(job)
algo()

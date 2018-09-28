from datetime import datetime
from utils.Mongodb import Mongodb

import logging
import grequests
# import gevent.monkey
# gevent.monkey.patch_all()

def scheduler():
    mongo = Mongodb()
    rides = list(mongo.get_pending_rides(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    logging.info("{} Rides found".format(len(rides)))
    async_list = []
    for ride in rides:
        logging.info(ride["_id"])
        action_item = grequests.get("http://0.0.0.0:5000/weleave/{}".format(ride["_id"])) #,  verify=False)
        async_list.append(action_item)
        #requests.get("http://0.0.0.0:5000/weleave/{}".format(ride["_id"]))
    grequests.map(async_list)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    scheduler()
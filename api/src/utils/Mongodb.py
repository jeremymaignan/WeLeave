from utils.ConfManager import get_conf

from pymongo import MongoClient
from bson import ObjectId
import logging

class Mongodb():
    def __init__(self, tablename):
        client = MongoClient(
            get_conf("mongodb_host"),
            get_conf("mongodb_port")
        ) 
        db = client['weleave']
        self.collection = db[tablename]
    
    def get_item(self, query):
        try:
            return self.collection.find_one(query)
        except Exception as err:
            logging.error("Cannot fetch item in DB. Error: {}".format(err))
            return None
            
    def insert_item(self, item):
        return self.collection.insert_one(item).inserted_id
    
    def update_ride(self, id, changes):
        try: 
            return self.collection.update_one(
                {'_id': ObjectId(id)},
                changes
            ).modified_count
        except Exception as err:
            logging.error("Cannot update iteration of ride in DB. Error: {}".format(err))
            return None

    def get_pending_rides(self, now):
        return self.collection.find({
            "status": "pending",
            "iteration.todo": { "$gt": 0 },
            "start_at": {"$lt": now} 
        })

    def update_item(self, ride):
        return self.collection.save(ride)

    def update_value(self, id, value):
        return self.collection.update(id, value)
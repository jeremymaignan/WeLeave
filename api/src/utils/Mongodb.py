from utils.ConfManager import get_conf

from pymongo import MongoClient
from bson import ObjectId

class Mongodb():
    def __init__(self):
        client = MongoClient(
            get_conf("mongodb_host"),
            get_conf("mongodb_port")
        )
        db = client['uber']
        self.collection = db['job']
    
    def get_item(self, id):
        return self.collection.find_one({"_id" :ObjectId(id)})

    def insert_item(self, item):
        return self.collection.insert_one(item).inserted_id
    
    def update_item_status(self, id, changes):
        return self.collection.update_one(
            {'_id': ObjectId(id)},
            {"$set": changes}
        ).modified_count

    def get_pending_jobs(self):
        query =  {
            "status": "pending",
            "iteration": { "$gt": 0 }
        }
        return self.collection.find(query)

    def update_item(self, job):
        return self.collection.save(job)
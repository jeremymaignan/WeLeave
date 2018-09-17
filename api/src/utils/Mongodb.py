from utils.ConfManager import get_conf

from pymongo import MongoClient
from bson import ObjectId

class Mongodb():
    def __init__(self):
        client = MongoClient(
            get_conf("mongodb_host"),
            get_conf("mongodb_port")
        ) 
        db = client['weleave']
        self.collection = db['rides']
    
    def get_item(self, id):
        try:
            return self.collection.find_one({"_id" :ObjectId(id)})
        except:
            return None
            
    def insert_item(self, item):
        return self.collection.insert_one(item).inserted_id
    
    def update_job(self, id, changes):
        try: 
            return self.collection.update_one(
                {'_id': ObjectId(id)},
                changes
            ).modified_count
        except:
            return None

    def get_pending_jobs(self, now):
        return self.collection.find({
            "status": "pending",
            "iteration.todo": { "$gt": 0 },
            "start_at": {"$lt": now} 
        })

    def update_item(self, job):
        return self.collection.save(job)

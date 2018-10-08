from utils.Mongodb import Mongodb

from flask import Flask, Response, Blueprint, request
import json
import logging
from datetime import datetime

add_user_address_route = Blueprint('add_user_address', __name__)
get_user_data_route = Blueprint('get_user_data', __name__)

@get_user_data_route.route("/users/<user_id>",  methods=['GET'])
def get_user_data(user_id):
    mongo = Mongodb('users')
    user = mongo.get_item({'user_id': user_id})
    if None == user:
        logging.error("User {} not found".format(user_id))
        return Response(status=404)
    user["id"] = str(user["_id"])
    del user["_id"]
    logging.info("Get user {}".format(user_id))
    return Response(
        response=json.dumps(user),
        status=200,
        mimetype='application/json'
    )

@add_user_address_route.route("/users/<user_id>/addresses",  methods=['POST'])
def add_user_address(user_id):
    # parse address
    try: 
        data = json.loads(request.data)
        address = data["address"]
        label = data["label"]
    except: 
        logging.error("Bad request")
        return Response(status=400)
    mongo = Mongodb('users')
    response = mongo.update_value({'user_id': user_id}, {
        '$set': {
            'addresses.{}'.format(label): address,
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    )
    if response["nModified"] == 0:
        return Response(status=404)
    logging.info("Address added to user {}".format(user_id))
    return Response(status=201)

def create_user(user_id):
    mongo = Mongodb('users')
    user = mongo.get_item({'user_id': user_id})
    if user == None:
        user_id = mongo.insert_item({
            "user_id": user_id,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "addresses": {},
            "nb_rides": 1
        })
    else:
        user["updated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user["nb_rides"] += 1
        mongo.update_item(user)
    
    
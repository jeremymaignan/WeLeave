from flask import Flask, Response, Blueprint, request
import json
from datetime import datetime
import logging
from urllib import parse
from bson import ObjectId
import ast

from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf
from entities.Rides import Rides
from utils.engine import get_fresh_estimation
from controllers.users import create_user

init_ride_route = Blueprint('init_ride', __name__)
stop_ride_route = Blueprint('stop_ride', __name__)
get_ride_route = Blueprint('get_ride', __name__)
extend_ride_route = Blueprint('extend_ride', __name__)

@init_ride_route.route("/rides",  methods=['POST'])
def init_ride():
    ride = Rides(json.loads(request.data)).get_ride()
    if None == ride:
        logging.error("Bad request. Cannot find coordinates from address")
        return Response(
            response=json.dumps({"details": "Cannot find coordinates from address"}),
            status=400,
            mimetype='application/json'
        )    
    if ride["seat_count"] <= 0 or ride["seat_count"] > 7:
        logging.error("Bad request. Number seat must be between 1 and 7")
        return Response(
            response=json.dumps({"details": "Number seat must be between 1 and 7"}),
            status=400,
            mimetype='application/json'
        )
    mongo = Mongodb('rides')
    ride_id = mongo.insert_item(ride)
    create_user(ride["user_id"])
    logging.info("Ride created. id: {}".format(ride_id))
    return Response(
        response=json.dumps({"id": str(ride_id)}),
        status=201,
        mimetype='application/json'
    )

@get_ride_route.route("/rides/<ride_id>",  methods=['GET'])
def get_ride(ride_id):
    # Parse query params:
    try:
        qs = parse.parse_qs(request.query_string.decode())
        size = int(qs["size"][0])
        update = ast.literal_eval(qs["update"][0].capitalize())
        apps = qs["apps"]
        if 1 == len(apps) and apps[0] == "*":
            apps = get_conf("apps")
        else:
            apps = apps[0].split(",")
        logging.info("Size: {} Update: {} Apps: {}".format(size, update, apps))
    except Exception as err:
        logging.error("Cannot parse query string params. Error: {}".format(err))
        return Response(status=400)

    # Update estimations
    if update:
        status = get_fresh_estimation(ride_id)
        if status == 404:
            logging.error("Not found. id: {}".format(ride_id))
            return Response(status=404)
        elif status == 500:
            logging.error("Internal Error. Cannot insert data in mongo. id: {}".format(ride_id))
            return Response(status=500)
        logging.info("Estimations updated. id: {}".format(ride_id))

    if 0 == size:
        return Response(status=200)
    
    # Get item and change id format
    mongo = Mongodb('rides')
    result = mongo.get_item({"_id": ObjectId(ride_id)})
    result["id"] = str(result["_id"])
    del result["_id"]

    # Keep only $SIZE items
    for app_name, app in result["prices"].copy().items():
        if app_name in apps:
            for mode_name in app.keys():
                app[mode_name] = app[mode_name][(size*-1):]
        else:
            del result["prices"][app_name]
            
    return Response(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

@extend_ride_route.route("/rides/<ride_id>",  methods=['PATCH'])
def extend_ride(ride_id):
    try:
        iteration = int(json.loads(request.data)["iteration"])
    except Exception as err:
        logging.error("Bad Request. Error: {}".format(err))
        return Response(status=400)
    mongo = Mongodb('rides')
    result = mongo.update_ride(ride_id, {"$inc": {'iteration.todo': iteration}})
    if not result:
        logging.error("Not found. id: {}".format(ride_id))
        return Response(status=404)
    logging.info("Increased number of iteration. id: {}".format(ride_id))
    return Response(status=200)

@stop_ride_route.route("/rides/<ride_id>",  methods=['DELETE'])
def stop_ride(ride_id):
    mongo = Mongodb('rides')
    result = mongo.update_ride(ride_id, {"$set": {"status": "stoped"}})
    if not result:
        logging.error("Not found. id: {}".format(ride_id))
        return Response(status=404)
    logging.info("Stoped ride. id: {}".format(ride_id))
    return Response(status=200)

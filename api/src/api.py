from flask import Flask, Response, Blueprint, request
import json
import logging

from utils.Mongodb import Mongodb
from entities.Rides import Rides
from utils.engine import get_fresh_estimation

init_ride_route = Blueprint('init_ride', __name__)
stop_ride_route = Blueprint('stop_ride', __name__)
get_ride_route = Blueprint('get_ride', __name__)
extend_ride_route = Blueprint('extend_ride', __name__)

@init_ride_route.route("/weleave",  methods=['POST'])
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
    mongo = Mongodb()
    ride_id = mongo.insert_item(ride)
    logging.info("Ride created. id: {}".format(ride_id))
    return Response(
        response=json.dumps({"id": str(ride_id)}),
        status=201,
        mimetype='application/json'
    )

@get_ride_route.route("/weleave/<ride_id>",  methods=['GET'])
def get_ride(ride_id):
    status, fresh_estimation = get_fresh_estimation(ride_id)
    if status == 404:
        logging.error("Not found. id: {}".format(ride_id))
        return Response(status=404)
    elif status == 500:
        logging.error("Internal Error. Cannot insert data in mongo. id: {}".format(ride_id))
        return Response(status=500)
    logging.info("Estimations updated. id: {}".format(ride_id))
    return Response(
        response=json.dumps(fresh_estimation),
        status=200,
        mimetype='application/json'
    )

@extend_ride_route.route("/weleave/<ride_id>",  methods=['PATCH'])
def extend_ride(ride_id):
    try:
        iteration = json.loads(request.data)["iteration"]
    except Exception as err:
        logging.error("Bad Request")
        return Response(status=400)
    mongo = Mongodb()
    result = mongo.update_ride(ride_id, {"$inc": {'iteration': {"todo": iteration}}})
    if not result:
        logging.error("Not found. id: {}".format(ride_id))
        return Response(status=404)
    logging.info("Increased number of iteration. id: {}".format(ride_id))
    return Response(status=200)

@stop_ride_route.route("/weleave/<ride_id>",  methods=['DELETE'])
def stop_ride(ride_id):
    mongo = Mongodb()
    result = mongo.update_ride(ride_id, {"$set": {"status": "stoped"}})
    if not result:
        logging.error("Not found. id: {}".format(ride_id))
        return Response(status=404)
    logging.info("Stoped ride. id: {}".format(ride_id))
    return Response(status=200)




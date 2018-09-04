from flask import Flask, Response, Blueprint, request
from datetime import datetime
import json

from utils.Geo import Geo
from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf

init_job_route = Blueprint('init_job', __name__)
stop_job_route = Blueprint('stop_job', __name__)
get_job_route = Blueprint('get_job', __name__)
extend_job_route = Blueprint('extend_job', __name__)

def build_item(data):
    geo = Geo()
    return {
        "user_id": data["user_id"],
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "from": {
            "address": data["from"],
            "coordinates": geo.get_geoloc(data["from"])
        },
        "to": {
            "address": data["to"],
            "coordinates": geo.get_geoloc(data["to"])
        },
        "iteration": {
            "todo": get_conf("number_of_iteration"),
            "done": 0
        },
        "status": "pending",
        "seat_count": data["number_seat"],
        "prices": {
        }
    }

@init_job_route.route("/uber",  methods=['POST'])
def init_job():
    item = build_item(json.loads(request.data))
    mongo = Mongodb()
    job_id = mongo.insert_item(item)
    return Response(
        response=json.dumps({"id": str(job_id)}),
        status=201,
        mimetype='application/json'
    )

@get_job_route.route("/uber/<job_id>",  methods=['GET'])
def get_job(job_id):
    print("[INFO] Get job {}".format(job_id))
    mongo = Mongodb()
    job = mongo.get_item(job_id)
    job["id"] = str(job["_id"])
    del job["_id"]
    if None == job:
        return Response(status=404)
    return Response(
        response=json.dumps(job),
        status=200,
        mimetype='application/json'
    )

@extend_job_route.route("/uber/<job_id>",  methods=['PATCH'])
def extend_job(job_id):
    try:
        iteration = json.loads(request.data)["iteration"]
    except Exception as err:
        return Response(status=404)
    mongo = Mongodb()
    result = mongo.update_job(job_id, {"$inc": {'iteration': {"todo": iteration}}})
    if not result:
        return Response(status=404)
    return Response(status=200)

@stop_job_route.route("/uber/<job_id>",  methods=['DELETE'])
def stop_job(job_id):
    mongo = Mongodb()
    result = mongo.update_job(job_id, {"$set": {"status": "stoped"}})
    if not result:
        return Response(status=404)
    return Response(status=200)
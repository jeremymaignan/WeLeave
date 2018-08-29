from flask import Flask, Response, Blueprint, request
from datetime import datetime
import json

from utils.Geo import Geo
from utils.Mongodb import Mongodb
from utils.ConfManager import get_conf

init_job_route = Blueprint('init_job', __name__)
stop_job_route = Blueprint('stop_job', __name__)
get_job_route = Blueprint('get_job', __name__)

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
        "iteration": get_conf("number_of_iteration"),
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
        response="{}".format({"id": str(job_id)}),
        status=201,
        mimetype='application/json'
    )

@get_job_route.route("/uber/<job_id>",  methods=['GET'])
def get_job(job_id):
    print("[INFO] Get job {}".format(job_id))
    mongo = Mongodb()
    job = mongo.get_item(job_id)
    print(job)
    if None == job:
        return Response(
            response="",
            status=404,
            mimetype='application/json'
        )
    return Response(
        response="{}".format(job),
        status=200,
        mimetype='application/json'
    )

@stop_job_route.route("/uber/<job_id>",  methods=['DELETE'])
def stop_job(job_id):
    mongo = Mongodb()
    result = mongo.update_item_status(job_id, {"status": "stoped"})
    if 1 == result:
        return Response(
            response="",
            status=201,
            mimetype='application/json'
        )
    return Response(
        response="",
        status=404,
        mimetype='application/json'
    )
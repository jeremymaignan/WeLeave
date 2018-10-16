from flask import Flask, Response, Blueprint, request, send_file
import json

from utils.ConfManager import get_conf

get_apps_picture_route = Blueprint('get_apps_picture', __name__)
get_apps_details_route = Blueprint('get_apps_details', __name__)

@get_apps_picture_route.route("/apps/pictures/<app_name>",  methods=['GET'])
def get_apps_picture(app_name):
    if app_name not in get_conf("apps"):
        return Response(status=404)
    return send_file("../assets/{}.jpg".format(app_name), mimetype='image/gif')

@get_apps_details_route.route("/apps",  methods=['GET'])
def get_apps_details():
    hostname = get_conf("api_hostname")
    return Response(
        response=json.dumps({
            "uber": {
                "picture_link": "{}/apps/pictures/uber".format(hostname),
                "deeplink": ""
            },
            "marcel": {
                "picture_link": "{}/apps/pictures/marcel".format(hostname),
                "deeplink": ""
            },
            "snapcar": {
                "picture_link": "{}/apps/pictures/snapcar".format(hostname),
                "deeplink": ""
            },
            "allocab": {
                "picture_link": "{}/apps/pictures/allocab".format(hostname),
                "deeplink": ""
            },
            "g7": {
                "picture_link": "{}/apps/pictures/g7".format(hostname),
                "deeplink": ""
            },
            "drive": {
                "picture_link": "{}/apps/pictures/drive".format(hostname),
                "deeplink": ""
            },
            "citybird": {
                "picture_link": "{}/apps/pictures/citybird".format(hostname),
                "deeplink": ""
            },
            "felix": {
                "picture_link": "{}/apps/pictures/felix".format(hostname),
                "deeplink": ""
            },
            "lecab": {
                "picture_link": "{}/apps/pictures/lecab".format(hostname),
                "deeplink": ""
            }
        }),
        status=200,
        mimetype='application/json'
    )

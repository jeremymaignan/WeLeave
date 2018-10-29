from flask import Flask, Response, Blueprint, request, send_file
import json
import logging
from urllib import parse

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
    try:
        qs = parse.parse_qs(request.query_string.decode())
        os = qs["os"][0]
    except:
        return Response(status=400)
    if os not in ["ios", "android"]:
        return Response(status=400)
    hostname = get_conf("api_hostname")
    if os == "android":
        return Response(
            response=json.dumps({
                "uber": {
                    "picture_link": "{}/apps/pictures/uber".format(hostname),
                    "deeplink": "",
                    "rating": "4.2"
                },
                "marcel": {
                    "picture_link": "{}/apps/pictures/marcel".format(hostname),
                    "deeplink": "",
                    "rating": "3.9"
                },
                "snapcar": {
                    "picture_link": "{}/apps/pictures/snapcar".format(hostname),
                    "deeplink": "",
                    "rating": "3.4"
                },
                "allocab": {
                    "picture_link": "{}/apps/pictures/allocab".format(hostname),
                    "deeplink": "",
                    "rating": "3.9"
                },
                "g7": {
                    "picture_link": "{}/apps/pictures/g7".format(hostname),
                    "deeplink": "",
                    "rating": "3.7"
                },
                "drive": {
                    "picture_link": "{}/apps/pictures/drive".format(hostname),
                    "deeplink": "",
                    "rating": ""
                },
                "citybird": {
                    "picture_link": "{}/apps/pictures/citybird".format(hostname),
                    "deeplink": "",
                    "rating": "4.3"
                },
                "felix": {
                    "picture_link": "{}/apps/pictures/felix".format(hostname),
                    "deeplink": "",
                    "rating": "3.2"
                },
                "lecab": {
                    "picture_link": "{}/apps/pictures/lecab".format(hostname),
                    "deeplink": "",
                    "rating": "3.7"
                },
                "taxify": {
                    "picture_link": "{}/apps/pictures/taxify".format(hostname),
                    "deeplink": "",
                    "rating": "4.2"
                },
                "talixo": {
                    "picture_link": "{}/apps/pictures/talixo".format(hostname),
                    "deeplink": "",
                    "rating": "3.9"
                }
            }),
            status=200,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({
            "uber": {
                "picture_link": "{}/apps/pictures/uber".format(hostname),
                "deeplink": "",
                "rating": "4.2"
            },
            "marcel": {
                "picture_link": "{}/apps/pictures/marcel".format(hostname),
                "deeplink": "",
                "rating": "3.1"
            },
            "snapcar": {
                "picture_link": "{}/apps/pictures/snapcar".format(hostname),
                "deeplink": "",
                "rating": "3.8"
            },
            "allocab": {
                "picture_link": "{}/apps/pictures/allocab".format(hostname),
                "deeplink": "",
                "rating": "4.7"
            },
            "g7": {
                "picture_link": "{}/apps/pictures/g7".format(hostname),
                "deeplink": "",
                "rating": "3.9"
            },
            "drive": {
                "picture_link": "{}/apps/pictures/drive".format(hostname),
                "deeplink": "",
                "rating": "4.9"
            },
            "citybird": {
                "picture_link": "{}/apps/pictures/citybird".format(hostname),
                "deeplink": "",
                "rating": "4.4"
            },
            "felix": {
                "picture_link": "{}/apps/pictures/felix".format(hostname),
                "deeplink": "",
                "rating": "3.5"
            },
            "lecab": {
                "picture_link": "{}/apps/pictures/lecab".format(hostname),
                "deeplink": "",
                "rating": "3.7"
            },
            "taxify": {
                "picture_link": "{}/apps/pictures/taxify".format(hostname),
                "deeplink": "",
                "rating": "4.8"
            },
            "talixo": {
                "picture_link": "{}/apps/pictures/talixo".format(hostname),
                "deeplink": "",
                "rating": "4.6"
            }
        }),
        status=200,
        mimetype='application/json'
    )

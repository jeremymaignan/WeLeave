from flask import Flask
import logging
import flask_monitoringdashboard as dashboard

from datetime import datetime
from utils.ConfManager import get_conf
import controllers.users as users
import controllers.rides as rides
import controllers.apps as apps

app = Flask(__name__)
dashboard.bind(app)
# Initial logger
if get_conf("log_in_file"):
    filename = '/logs/weleave_api_{}.log'.format(datetime.now().strftime('%Y-%m-%d'))
    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Redirect logs to {}".format(filename))
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Register routes
# Rides
app.register_blueprint(rides.init_ride_route)
app.register_blueprint(rides.stop_ride_route)
app.register_blueprint(rides.get_ride_route)
app.register_blueprint(rides.extend_ride_route)
# Apps
app.register_blueprint(apps.get_apps_picture_route)
app.register_blueprint(apps.get_apps_details_route)
# Users
app.register_blueprint(users.add_user_address_route)
app.register_blueprint(users.get_user_data_route)

# Run api
app.run(debug=True,  host='0.0.0.0', port=5000) # , ssl_context=('cert.pem', 'key.pem'))

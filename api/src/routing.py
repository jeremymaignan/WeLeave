from flask import Flask
import logging
import flask_monitoringdashboard as dashboard

from datetime import datetime
from utils.ConfManager import get_conf
import api

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
app.register_blueprint(api.init_ride_route)
app.register_blueprint(api.stop_ride_route)
app.register_blueprint(api.get_ride_route)
app.register_blueprint(api.extend_ride_route)
app.register_blueprint(api.get_apps_picture_route)
app.register_blueprint(api.get_apps_details_route)

# Run api
app.run(debug=True,  host='0.0.0.0', port=5000) # , ssl_context=('cert.pem', 'key.pem'))

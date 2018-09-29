from flask import Flask
import logging

import api

app = Flask(__name__)
# Initial logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Register routes
app.register_blueprint(api.init_ride_route)
app.register_blueprint(api.stop_ride_route)
app.register_blueprint(api.get_ride_route)
app.register_blueprint(api.extend_ride_route)
app.register_blueprint(api.get_pic_route)

# Run api
app.run(debug=True,  host='0.0.0.0', port=5000) # , ssl_context=('cert.pem', 'key.pem'))

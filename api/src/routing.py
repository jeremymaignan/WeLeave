from flask import Flask
import uber_analytics

app = Flask(__name__)
app.register_blueprint(uber_analytics.init_job_route)
app.register_blueprint(uber_analytics.stop_job_route)
app.register_blueprint(uber_analytics.get_job_route)
app.register_blueprint(uber_analytics.extend_job_route)
app.debug = True

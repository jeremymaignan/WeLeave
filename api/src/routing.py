from flask import Flask
import api

app = Flask(__name__)
app.register_blueprint(api.init_job_route)
app.register_blueprint(api.stop_job_route)
app.register_blueprint(api.get_job_route)
app.register_blueprint(api.extend_job_route)
app.debug = True

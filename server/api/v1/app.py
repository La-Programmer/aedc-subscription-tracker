#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from celery.schedules import crontab
from ..celery_config import celery_init_app

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
    ),
)
# app.config.from_prefixed_env()
# app.extensions["celery"] = celery_app
# app.config["CELERY_CONFIG"] = {
#     "broker_url": "redis://localhost:6379",
#     "result_backend": "redis://localhost:6379"
# }
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': 'AEDC Subscription Tracking Application',
    'uiversion': 3
}
celery_app = celery_init_app(app)
# celery_app.set_default()
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(error):
    """ Close storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

Swagger(app)

if __name__ == "__main__":
    """Main Function"""
    host = '0.0.0.0'
    port = '5000'
    app.run(debug=True, host=host, port=port, threaded=True)

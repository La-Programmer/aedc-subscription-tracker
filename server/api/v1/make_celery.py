#!/usr/bin/python3

from api.v1 import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

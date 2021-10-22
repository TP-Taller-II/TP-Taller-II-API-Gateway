"""Flask api."""
import logging

from flask import Flask
from flask_cors import CORS

from api_gateway.api import api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_app():
    """creates a new app instance"""
    new_app = Flask(__name__)
    new_app.config["ERROR_404_HELP"] = False
    api.init_app(new_app)
    CORS(new_app)
    return new_app

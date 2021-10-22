"""Flask api."""
import logging
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from api_gateway.api import api
from api_gateway.cfg import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_app():
    """creates a new app instance"""
    new_app = Flask(__name__)
    new_app.config["ERROR_404_HELP"] = False
    api.init_app(new_app)
    CORS(new_app)
    return new_app

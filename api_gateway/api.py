"""API module."""
import logging

import flask.scaffold

# monkeypatching this because it flask_restx has a bug
# pylint:disable=E1101
# pylint:disable=W0212
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restx import Api

from api_gateway import __version__
from api_gateway.namespaces import course_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api = Api(prefix="/api", version=__version__, validate=True)
api.add_namespace(course_namespace, path='/courses')

# Acordarse de mandar el x-header-user !!!!


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    logger.error('Unhandled Exception: %s - %s', str(type(error)), str(error))
    print(
        'Unhandled Exception: ', str(type(error)), str(error)
    )  # Todo: remove this print !!!!!

    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)

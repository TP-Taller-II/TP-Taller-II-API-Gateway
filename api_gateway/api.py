"""API module."""
import logging

import flask.scaffold

# monkeypatching this because it flask_restx has a bug
# pylint:disable=E1101
# pylint:disable=W0212
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restx import Api

from api_gateway import __version__
from api_gateway.namespaces import (
    course_namespace,
    payment_namespace,
    status_namespace,
    user_namespace,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api = Api(prefix="/api", version=__version__, validate=True)
api.add_namespace(course_namespace, path='/courses')
api.add_namespace(user_namespace, path='/auth-server')
api.add_namespace(status_namespace, path='/status')
api.add_namespace(payment_namespace, path='/payments')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    logger.error('Unhandled Exception: %s - %s', str(type(error)), str(error))

    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)

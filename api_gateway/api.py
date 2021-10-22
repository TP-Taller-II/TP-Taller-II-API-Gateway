"""API module."""
import logging

import flask.scaffold

# pylint:disable=W0212
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restx import Api

from api_gateway.namespaces.namespace import ns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="/v1", version="0.1", validate=True)
api.add_namespace(ns, path='/hello')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)

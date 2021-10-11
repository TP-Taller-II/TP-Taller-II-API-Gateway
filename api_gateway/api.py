"""API module."""
import logging

from flask_restx import Api

from api_gateway import __version__
from api_gateway.namespaces import default_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="/v1", version=__version__, validate=True)
api.add_namespace(default_namespace, path='/hello')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)

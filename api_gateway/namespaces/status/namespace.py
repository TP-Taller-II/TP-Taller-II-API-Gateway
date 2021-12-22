# pylint: disable=unused-argument
"""Course namespace module."""
from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, abort
from requests.exceptions import ConnectionError as NewConnectionError

from api_gateway.clients.auth_server_client import auth_server_client
from api_gateway.clients.course_client import course_client
from api_gateway.clients.payment_client import payment_client
from api_gateway.helpers.logger import logger

ns = Namespace("Status", description="Status operation")
starting_date = datetime.now()


def call_servers():
    logger.info('Status Call')

    if 'Authorization' not in request.headers:
        logger.error('Authorization token is required.')
        abort(401, 'Authorization token is required.')
    token = request.headers['Authorization']

    authentication_res_body, authentication_status_code = auth_server_client.call(
        'get', '/auth-server/v1/admin/users', None, token
    )
    if authentication_status_code != 200:
        return authentication_res_body, authentication_status_code

    status = {
        'api-gateway': {
            'status': 'Online',
            'creationDate': '0',
            'description': 'Microservicio de conexion con ' 'otros servidores.',
        }
    }

    try:
        status['auth-server'] = auth_server_client.call(
            'get', '/auth-server/v1/status', None, token
        )[0]
    except NewConnectionError:
        status['auth-server'] = {
            'status': 'Offline',
            'creationDate': '0',
            'description': '',
        }
    try:
        status['courses'] = course_client.call(
            'get', '/courses/v1/status', None, token, None
        )[0]
    except NewConnectionError:
        status['courses'] = {
            'status': 'Offline',
            'creationDate': '0',
            'description': '',
        }
    try:
        status['payments'] = payment_client.call(
            'get', '/payments/status', None, token
        )[0]
    except NewConnectionError:
        status['payments'] = {
            'status': 'Offline',
            'creationDate': '0',
            'description': '',
        }

    return status, 200


@ns.route('/')
@ns.header('Authorization', 'Authorization Token')
class StatusResource(Resource):
    @ns.doc('get_status')
    def get(self):
        """Get Courses Call"""
        return call_servers()

# pylint: disable=unused-argument
"""Course namespace module."""

from flask import request
from flask_restx import Namespace, Resource, abort

from api_gateway.clients.auth_server_client import auth_server_client
from api_gateway.clients.payment_client import payment_client
from api_gateway.helpers.logger import logger

ns = Namespace("Status", description="Status operation")


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

    status = {"payments": payment_client.call('get', 'payments/status', None, token)}

    return status, 200


@ns.route('/')
@ns.header('Authorization', 'Authorization Token')
class StatusResource(Resource):
    @ns.doc('get_status')
    def get(self):
        """Get Courses Call"""
        return call_servers()

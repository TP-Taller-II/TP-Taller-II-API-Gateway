# pylint: disable=unused-argument
"""Payment namespace module."""

from flask import request
from flask_restx import Namespace, Resource, abort

from api_gateway.clients.auth_server_client import auth_server_client
from api_gateway.clients.payment_client import payment_client
from api_gateway.helpers.logger import logger

ns = Namespace("Payment", description="Payments operations")


def call_payments(payload):
    logger.info('Payments Call')

    if 'Authorization' not in request.headers:
        logger.error('Authorization token is required.')
        abort(401, 'Authorization token is required.')
    token = request.headers['Authorization']

    authentication_res_body, authentication_status_code = auth_server_client.call(
        'get', '/auth-server/v1/users/me', None, token
    )
    if authentication_status_code != 200:
        return authentication_res_body, authentication_status_code

    path = request.path.split('/api')[1]
    method = request.method.lower()
    res_body, res_status_code = payment_client.call(
        method, path, payload, token
    )
    return res_body, res_status_code


@ns.route('/status/')
@ns.header('Authorization', 'Authorization Token')
class Payment1Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route('/<string:p1>/<string:p2>')
@ns.header('Authorization', 'Authorization Token')
class Payment2Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>')
@ns.header('Authorization', 'Authorization Token')
class Payment3Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>')
@ns.header('Authorization', 'Authorization Token')
class Payment4Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3, p4):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3, p4):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3, p4):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3, p4):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>')
@ns.header('Authorization', 'Authorization Token')
class Payment5Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3, p4, p5):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3, p4, p5):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3, p4, p5):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3, p4, p5):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>')
@ns.header('Authorization', 'Authorization Token')
class Payment6Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3, p4, p5, p6):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3, p4, p5, p6):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3, p4, p5, p6):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3, p4, p5, p6):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route(
    '/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>/<string:p7>'
)
@ns.header('Authorization', 'Authorization Token')
class Payment7Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3, p4, p5, p6, p7):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3, p4, p5, p6, p7):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3, p4, p5, p6, p7):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3, p4, p5, p6, p7):
        """Delete Payments Call"""
        return call_payments(ns.payload)


@ns.route(
    '/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>/<string:p7>/<string:p8>'
)
@ns.header('Authorization', 'Authorization Token')
class Payment8Resource(Resource):
    @ns.doc('get_call_payments')
    def get(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Get Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('post_call_payments')
    def post(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Post Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('patch_call_payments')
    def patch(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Patch Payments Call"""
        return call_payments(ns.payload)

    @ns.doc('delete_call_payments')
    def delete(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Delete Payments Call"""
        return call_payments(ns.payload)

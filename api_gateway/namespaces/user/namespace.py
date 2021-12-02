# pylint: disable=unused-argument
"""User namespace module."""

from flask import request
from flask_restx import Namespace, Resource, abort

from api_gateway.clients.auth_server_client import auth_server_client
from api_gateway.helpers.logger import logger

ns = Namespace("User", description="Users operations")


def call_users(payload):
    logger.info('Users Call')

    if 'Authorization' not in request.headers:
        logger.error('Authorization token is required.')
        abort(401, 'Authorization token is required.')
    token = request.headers['Authorization']
    path = request.path.split('/api')[1]
    method = request.method.lower()
    res_body, res_status_code = auth_server_client.call(method, path, payload, token)
    return res_body, res_status_code


@ns.route('/<string:p1>/<string:p2>')
@ns.header('Authorization', 'Authorization Token')
class User2Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>')
@ns.header('Authorization', 'Authorization Token')
class User3Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>')
@ns.header('Authorization', 'Authorization Token')
class User4Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3, p4):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3, p4):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3, p4):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3, p4):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>')
@ns.header('Authorization', 'Authorization Token')
class User5Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3, p4, p5):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3, p4, p5):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3, p4, p5):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3, p4, p5):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>')
@ns.header('Authorization', 'Authorization Token')
class User6Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3, p4, p5, p6):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3, p4, p5, p6):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3, p4, p5, p6):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3, p4, p5, p6):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route(
    '/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>/<string:p7>'
)
@ns.header('Authorization', 'Authorization Token')
class User7Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3, p4, p5, p6, p7):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3, p4, p5, p6, p7):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3, p4, p5, p6, p7):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3, p4, p5, p6, p7):
        """Delete Users Call"""
        return call_users(ns.payload)


@ns.route(
    '/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>/<string:p7>/<string:p8>'
)
@ns.header('Authorization', 'Authorization Token')
class User8Resource(Resource):
    @ns.doc('get_call_users')
    def get(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Get Users Call"""
        return call_users(ns.payload)

    @ns.doc('post_call_users')
    def post(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Post Users Call"""
        return call_users(ns.payload)

    @ns.doc('patch_call_users')
    def patch(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Patch Users Call"""
        return call_users(ns.payload)

    @ns.doc('delete_call_users')
    def delete(self, p1, p2, p3, p4, p5, p6, p7, p8):
        """Delete Users Call"""
        return call_users(ns.payload)

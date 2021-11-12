# pylint: disable=unused-argument
"""Course namespace module."""

from flask import request
from flask_restx import Namespace, Resource, abort

from api_gateway.clients.course_client import course_client
from api_gateway.helpers.logger import logger

ns = Namespace("Course", description="Courses operations")


def call_courses():
    logger.info('Courses Call')

    if 'Authorization' not in request.headers:
        logger.error('Authorization token is required.')
        abort(401, 'Authorization token is required.')
    token = request.headers['Authorization']
    path = request.path.split('/api')[1]
    method = request.method.lower()
    res_body, res_status_code = course_client.call(method, path, token, None)
    return res_body, res_status_code


@ns.route('/<string:p1>/<string:p2>')
@ns.header('Authorization', 'Authorization Token')
class Course2Resource(Resource):
    @ns.doc('get_call_courses')
    def get(self, p1, p2):
        """Get Courses Call"""
        return call_courses()

    @ns.doc('post_call_courses')
    def post(self, p1, p2):
        """Post Courses Call"""
        return call_courses()

    @ns.doc('patch_call_courses')
    def patch(self, p1, p2):
        """Patch Courses Call"""
        return call_courses()

    @ns.doc('delete_call_courses')
    def delete(self, p1, p2):
        """Delete Courses Call"""
        return call_courses()


@ns.route('/<string:p1>/<string:p2>/<string:p3>')
@ns.header('Authorization', 'Authorization Token')
class Course3Resource(Resource):
    @ns.doc('get_call_courses')
    def get(self, p1, p2, p3):
        """Get Courses Call"""
        return call_courses()

    @ns.doc('post_call_courses')
    def post(self, p1, p2, p3):
        """Post Courses Call"""
        return call_courses()

    @ns.doc('patch_call_courses')
    def patch(self, p1, p2, p3):
        """Patch Courses Call"""
        return call_courses()

    @ns.doc('delete_call_courses')
    def delete(self, p1, p2, p3):
        """Delete Courses Call"""
        return call_courses()


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>')
@ns.header('Authorization', 'Authorization Token')
class Course4Resource(Resource):
    @ns.doc('get_call_courses')
    def get(self, p1, p2, p3, p4):
        """Get Courses Call"""
        return call_courses()

    @ns.doc('post_call_courses')
    def post(self, p1, p2, p3, p4):
        """Post Courses Call"""
        return call_courses()

    @ns.doc('patch_call_courses')
    def patch(self, p1, p2, p3, p4):
        """Patch Courses Call"""
        return call_courses()

    @ns.doc('delete_call_courses')
    def delete(self, p1, p2, p3, p4):
        """Delete Courses Call"""
        return call_courses()


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>')
@ns.header('Authorization', 'Authorization Token')
class Course5Resource(Resource):
    @ns.doc('get_call_courses')
    def get(self, p1, p2, p3, p4, p5):
        """Get Courses Call"""
        return call_courses()

    @ns.doc('post_call_courses')
    def post(self, p1, p2, p3, p4, p5):
        """Post Courses Call"""
        return call_courses()

    @ns.doc('patch_call_courses')
    def patch(self, p1, p2, p3, p4, p5):
        """Patch Courses Call"""
        return call_courses()

    @ns.doc('delete_call_courses')
    def delete(self, p1, p2, p3, p4, p5):
        """Delete Courses Call"""
        return call_courses()


@ns.route('/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>/<string:p6>')
@ns.header('Authorization', 'Authorization Token')
class Course6Resource(Resource):
    @ns.doc('get_call_courses')
    def get(self, p1, p2, p3, p4, p5, p6):
        """Get Courses Call"""
        return call_courses()

    @ns.doc('post_call_courses')
    def post(self, p1, p2, p3, p4, p5, p6):
        """Post Courses Call"""
        return call_courses()

    @ns.doc('patch_call_courses')
    def patch(self, p1, p2, p3, p4, p5, p6):
        """Patch Courses Call"""
        return call_courses()

    @ns.doc('delete_call_courses')
    def delete(self, p1, p2, p3, p4, p5, p6):
        """Delete Courses Call"""
        return call_courses()

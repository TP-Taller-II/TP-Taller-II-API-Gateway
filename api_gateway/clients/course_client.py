import json
import os

import requests

from api_gateway.helpers.logger import logger


class CourseClient:
    def __init__(self):
        # !!!!
        self.url = os.environ.get(
            'FRUX_SC_URL', 'https://ubademy-g2-courses!!!!.herokuapp.com'
        )

    def _request(
        self, method, path, token, body,
    ):
        if not body:
            body = {}
        func = getattr(requests, method)
        try:
            r = func(f'{self.url}{path}', json=body, headers={'x-auth-token': token})
        except Exception as e:
            logger.error(
                'Error when making request path: "%s", token: "%s" to Courses. Error: %s',
                path,
                token,
                e,
            )
            raise e

        res_body = json.loads(r.content.decode())
        logger.info(
            'CourseClient method: %s, path: %s, status_code: %s, body: %s',
            method,
            path,
            r.status_code,
            res_body,
        )

        return res_body, r.status_code

    def call(self, method, path, token, body):
        return self._request(method, path, token, body)


course_client = CourseClient()
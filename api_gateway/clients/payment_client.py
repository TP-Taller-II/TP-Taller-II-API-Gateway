import json
import os

import requests

from api_gateway.helpers.logger import logger


class PaymentClient:
    def __init__(self):
        self.url = os.environ.get(
            'FRUX_SC_URL', 'https://ubademy-g2-payments.herokuapp.com'
        )

    def _request(self, method, path, body, token):
        if not body:
            body = {}
        func = getattr(requests, method)
        headers = {'x-auth-token': token}
        try:
            r = func(f'{self.url}{path}', json=body, headers=headers)
        except Exception as e:
            logger.error(
                'Error when making request path: "%s", token: "%s" to Courses. Error: %s',
                path,
                token,
                e,
            )
            raise e

        try:
            res_body = json.loads(r.content.decode())
        except Exception as e:
            logger.error(
                'Error when making request path: "%s", token: "%s" to Courses. Error: %s',
                path,
                token,
                e,
            )
            res_body = {}

        logger.info(
            'PaymentClient method: %s, path: %s, status_code: %s, body: %s',
            method,
            path,
            r.status_code,
            res_body,
        )

        return res_body, r.status_code

    def call(self, method, path, body, token):
        return self._request(method, path, body, token)


payment_client = PaymentClient()

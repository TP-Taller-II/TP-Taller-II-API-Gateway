"""Sample test suite."""

import json
import logging

# pylint:disable=redefined-outer-name,protected-access
import pytest

from api_gateway.app import create_app

# import requests
# from pytest_mock import mocker

logger = logging.getLogger(__name__)


class ResponseContentMock:
    def __init__(self, res_body):
        self.res_body = res_body

    def decode(self):
        return json.dumps(self.res_body)


class ResponseMock:
    def __init__(self, status_code, res_body):
        self.status_code = status_code
        self.content = ResponseContentMock(res_body)


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as test_client:
        test_client.environ_base['HTTP_AUTHORIZATION'] = 'token-1'
        yield test_client


def test_root(client):
    response = client.get("/")
    assert response._status_code == 200


def test_get_courses(client, mocker):
    mocker.patch('requests.get', return_value=ResponseMock(201, []))
    response = client.get("/api/courses/v1/courses")

    assert response._status_code == 201
    assert json.loads(response.data) == []

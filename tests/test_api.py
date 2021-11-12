"""Sample test suite."""

import json
import logging

# pylint:disable=redefined-outer-name,protected-access
import pytest

from api_gateway.app import create_app

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
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, ['course1', 'course2'])
    )

    response = client.get("/api/courses/v1/courses")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == ['course1', 'course2']


def test_post_courses(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post("/api/courses/v1/courses", json={'name': 'Fiesta'})

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_get_course(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.get("/api/courses/v1/courses/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_patch_course(client, mocker):
    mock_call = mocker.patch(
        'requests.patch', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.patch("/api/courses/v1/courses/1", json={'name': 'Fiesta'})

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_course(client, mocker):
    mock_call = mocker.patch(
        'requests.delete', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.delete("/api/courses/v1/courses/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_exams(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, [{'id': '1'}])
    )

    response = client.get("/api/courses/v1/courses/1/exams")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_exams(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post("/api/courses/v1/courses/1/exams", json={'name': 'Fiesta'})

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_get_exam(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.get("/api/courses/v1/courses/1/exams/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_patch_exam(client, mocker):
    mock_call = mocker.patch(
        'requests.patch', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.patch(
        "/api/courses/v1/courses/1/exams/1", json={'name': 'Fiesta'}
    )

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_exam(client, mocker):
    mock_call = mocker.patch(
        'requests.delete', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.delete("/api/courses/v1/courses/1/exams/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_students(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, [{'id': '1'}])
    )

    response = client.get("/api/courses/v1/courses/1/students")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_students(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post(
        "/api/courses/v1/courses/1/students", json={'name': 'Fiesta'}
    )

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_student(client, mocker):
    mock_call = mocker.patch(
        'requests.delete', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.delete("/api/courses/v1/courses/1/students/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_professors(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, [{'id': '1'}])
    )

    response = client.get("/api/courses/v1/courses/1/professors")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_professors(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post(
        "/api/courses/v1/courses/1/professors", json={'name': 'Fiesta'}
    )

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_professor(client, mocker):
    mock_call = mocker.patch(
        'requests.delete', return_value=ResponseMock(200, {'id': '1'})
    )

    response = client.delete("/api/courses/v1/courses/1/professors/1")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_exam_resolutions(client, mocker):
    mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, [{'id': '1'}])
    )

    response = client.get("/api/courses/v1/courses/1/exams/1/resolutions")

    mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_exam_resolutions(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post(
        "/api/courses/v1/courses/1/exams/1/resolutions", json={'name': 'Fiesta'}
    )

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_post_exam_resolutions_evaluate(client, mocker):
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(201, {'resource': {'id': '1'}})
    )

    response = client.post(
        "/api/courses/v1/courses/1/exams/1/resolutions/1/evaluate",
        json={'name': 'Fiesta'},
    )

    mock_call.assert_called_once_with(
        mocker.ANY, json={'name': 'Fiesta'}, headers=mocker.ANY
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}

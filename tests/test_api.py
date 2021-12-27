"""Sample test suite."""

import json
import logging

# pylint:disable=redefined-outer-name,protected-access
import pytest

from api_gateway.app import create_app

logger = logging.getLogger(__name__)

user_create_request_dto = {
    "name": "joe",
    "password": "joes super secret password",
    "surname": "Doe",
    "email": "joe_doeaassl@gmail.com",
    "birthDate": "2017-07-21T17:32:28Z",
    "profilePic": "https://a0.muscache.com/im/pictures/57acf111-9f94-4192-a7ae-7996fb31c1b1.jpg",
    "provider": "email",
}

user_response_dto = {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvZV9kb2VhYWxAZ21haWwuY29tIiwiX2lkIjoiNjFhNmVmMTA1MWU3MmEwMDEwMmU1MjIyIiwiY3JlYXRpb25EYXRlIjoiMjAyMS0xMi0wMVQwMzo0MjowOC42OTRaIiwiZXhwaXJhdGlvbkRhdGUiOiIyMDIxLTEyLTIxVDAzOjQyOjA4LjY5NFoiLCJpYXQiOjE2MzgzMzAxMjh9.aSyc1zkNIuecb1gpsMDgsIuIukg4SWlA44HrTnKfThk",
    "_id": "61a6ef1051e72a00102e5222",
    "name": "joe",
    "surname": "Doe",
    "email": "joe_doeaal@gmail.com",
    "birthDate": "2017-07-21T17:32:28.000Z",
    "profilePic": "https://a0.muscache.com/im/pictures/57acf111-9f94-4192-a7ae-7996fb31c1b1.jpg",
    "provider": "email",
    "createdAt": "2021-12-01T03:42:08.675Z",
    "updatedAt": "2021-12-01T03:42:08.675Z",
    "__v": 0,
}

valid_auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvZV9kb2VhYXNsQGdtYWlsLmNvbSIsIl9pZCI6IjYxYTZmMWY3ZjdiYzAyMDAxMGJhZTJiMyIsImNyZWF0aW9uRGF0ZSI6IjIwMjEtMTItMDFUMjM6MjE6MDEuNzczWiIsImV4cGlyYXRpb25EYXRlIjoiMjAyMS0xMi0yMVQyMzoyMTowMS43NzNaIiwiaWF0IjoxNjM4NDAwODYxfQ.8f-5uo56UZzM4l0b3LDB3qoCW5vwFamRUvrzEoQ-AJI'


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
        test_client.environ_base['HTTP_AUTHORIZATION'] = valid_auth_token
        yield test_client


def test_root(client):
    response = client.get("/")
    assert response._status_code == 200


def test_get_courses(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, ['course1', 'course2'])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == ['course1', 'course2']


def test_get_filtered_courses(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, ['course1', 'course2'])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses?category=Party&subscription=2")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses?category=Party&subscription=2',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == ['course1', 'course2']


def test_get_courses_but_authentication_returns_401(client, mocker):
    authentication_response = ResponseMock(401, {'message': 'Token expired'})
    get_mock_call = mocker.patch('requests.get', side_effect=[authentication_response])

    response = client.get("/api/courses/v1/courses")

    assert get_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    assert response._status_code == 401
    assert json.loads(response.data) == {'message': 'Token expired'}


def test_get_courses_but_authentication_returns_500(client, mocker):
    authentication_response = ResponseMock(500, {'message': 'Internal server error'})
    get_mock_call = mocker.patch('requests.get', side_effect=[authentication_response])

    response = client.get("/api/courses/v1/courses")

    assert get_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    assert response._status_code == 500
    assert json.loads(response.data) == {'message': 'Internal server error'}


def test_post_courses(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post("/api/courses/v1/courses", json={'name': 'Fiesta'})

    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_get_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_put_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    patch_mock_call = mocker.patch('requests.put', return_value=courses_response)

    response = client.put("/api/courses/v1/courses/1", json={'name': 'Fiesta'})

    assert get_mock_call.call_count == 1
    assert patch_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_patch_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    patch_mock_call = mocker.patch('requests.patch', return_value=courses_response)

    response = client.patch("/api/courses/v1/courses/1", json={'name': 'Fiesta'})

    assert get_mock_call.call_count == 1
    assert patch_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1")

    assert get_mock_call.call_count == 1
    assert delete_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_exams(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, [{'id': '1'}])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1/exams")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_exams(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post("/api/courses/v1/courses/1/exams", json={'name': 'Fiesta'})

    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_get_exam(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1/exams/1")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_put_exam(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    patch_mock_call = mocker.patch('requests.put', return_value=courses_response)

    response = client.put("/api/courses/v1/courses/1/exams/1", json={'name': 'Fiesta'})

    assert get_mock_call.call_count == 1
    assert patch_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_patch_exam(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    patch_mock_call = mocker.patch('requests.patch', return_value=courses_response)

    response = client.patch(
        "/api/courses/v1/courses/1/exams/1", json={'name': 'Fiesta'}
    )

    assert get_mock_call.call_count == 1
    assert patch_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_exam(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/exams/1")

    assert get_mock_call.call_count == 1
    assert delete_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_students(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, [{'id': '1'}])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1/students")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/students',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_students(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post(
        "/api/courses/v1/courses/1/students", json={'name': 'Fiesta'}
    )

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/students',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_student(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/students/1")

    assert get_mock_call.call_count == 1
    assert delete_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/students/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_professors(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, [{'id': '1'}])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1/professors")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/professors',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_professors(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post(
        "/api/courses/v1/courses/1/professors", json={'name': 'Fiesta'}
    )

    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/professors',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_professor(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/professors/1")

    assert get_mock_call.call_count == 1
    assert delete_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/professors/1',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_get_exam_resolutions(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, [{'id': '1'}])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses/1/exams/1/resolutions")

    assert get_mock_call.call_count == 2
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1/resolutions',
        json={},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_exam_resolutions(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post(
        "/api/courses/v1/courses/1/exams/1/resolutions", json={'name': 'Fiesta'}
    )

    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1/resolutions',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_post_exam_resolutions_evaluate(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post(
        "/api/courses/v1/courses/1/exams/1/resolutions/1/evaluate",
        json={'name': 'Fiesta'},
    )

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': valid_auth_token},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses.herokuapp.com/courses/v1/courses/1/exams/1/resolutions/1/evaluate',
        json={'name': 'Fiesta'},
        headers={
            'x-auth-token': valid_auth_token,
            'x-user-id': user_response_dto['_id'],
        },
    )
    assert get_mock_call.call_count == 1
    assert post_mock_call.call_count == 1
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_post_sign_up(client, mocker):
    request_dto = user_create_request_dto
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/users/signUp", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_sign_in(client, mocker):
    request_dto = {
        "email": "joe_doeaasl@gmail.com",
        "password": "joes super secret password",
    }
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/users/signIn", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_get_logged_user(client, mocker):
    forwarded_response = user_response_dto
    get_mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.get("/api/auth-server/v1/users/me")

    get_mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_patch_logged_user(client, mocker):
    request_dto = {"name": "Foo"}
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.patch', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.patch("/api/auth-server/v1/users/me", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_get_some_user(client, mocker):
    forwarded_response = user_response_dto
    get_mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.get("/api/auth-server/v1/users/someuserid")

    get_mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_sign_out(client, mocker):
    request_dto = {"message": "User sign out"}
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_sign_out_unauthorized(client, mocker):
    request_dto = {"message": "User sign out"}
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(401, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 401
    assert json.loads(response.data) == forwarded_response


def test_post_admin_sign_up(client, mocker):
    request_dto = {
        "email": "joe_doeaasl@gmail.com",
        "password": "joes super secret password",
    }
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/admin/signIn", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_admin_sign_in(client, mocker):
    forwarded_response = [user_response_dto]
    get_mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.get("/api/auth-server/v1/admin/users")

    get_mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_get_admin_get_some_user(client, mocker):
    forwarded_response = user_response_dto
    get_mock_call = mocker.patch(
        'requests.get', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.get("/api/auth-server/v1/admin/users/someuserid")

    get_mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_admin_sign_out(client, mocker):
    request_dto = {"message": "User sign out"}
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(200, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_post_admin_sign_out_unauthorized(client, mocker):
    request_dto = {"message": "User sign out"}
    forwarded_response = user_response_dto
    mock_call = mocker.patch(
        'requests.post', return_value=ResponseMock(401, forwarded_response)
    )

    response = client.post("/api/auth-server/v1/admin/signOut", json=request_dto)

    mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
    assert response._status_code == 401
    assert json.loads(response.data) == forwarded_response


def test_payments_get_subscription(client, mocker):
    forwarded_response = user_response_dto
    mocker.patch('requests.get', return_value=ResponseMock(200, forwarded_response))

    response = client.get("/api/payments/v1/getSubscription/60456ebb0190bf001f6bbee2")

    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_payments_get_contract(client, mocker):
    forwarded_response = user_response_dto
    mocker.patch('requests.get', return_value=ResponseMock(200, forwarded_response))

    response = client.get("/api/payments/v1/getContract")

    assert response._status_code == 200
    assert json.loads(response.data) == forwarded_response


def test_payments_pay_subscription_failed_auth(client, mocker):
    authentication_response = ResponseMock(401, user_response_dto)
    request_dto = {
        "user_id": "60456ebb0190bf001f6bbee2",
        "wallet_pass": "0x8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f",
        "tier": 1,
    }

    forwarded_response = user_response_dto
    mocker.patch('requests.get', return_value=authentication_response)
    mocker.patch('requests.post', return_value=ResponseMock(200, forwarded_response))

    response = client.post("/api/payments/v1/paySubscription", json=request_dto)

    assert response._status_code == 401
    assert json.loads(response.data) == forwarded_response


def test_payments_missing_authorization(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)

    del client.environ_base['HTTP_AUTHORIZATION']

    mocker.patch('requests.get', return_value=authentication_response)

    response = client.get("/api/auth-server/v1/admin/users")

    assert response._status_code == 401

    response = client.get("/api/courses/v1/courses")

    assert response._status_code == 401

    response = client.get("/api/payments/v1/getContract")

    assert response._status_code == 401

    response = client.get("/api/status/")

    assert response._status_code == 401


def test_status(client, mocker):
    forwarded_response = user_response_dto
    mocker.patch('requests.get', return_value=ResponseMock(200, forwarded_response))

    response = client.get("/api/status/")

    assert response._status_code == 200

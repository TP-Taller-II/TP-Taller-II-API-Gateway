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
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, ['course1', 'course2'])
    get_mock_call = mocker.patch(
        'requests.get', side_effect=[authentication_response, courses_response]
    )

    response = client.get("/api/courses/v1/courses")

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 200
    assert json.loads(response.data) == ['course1', 'course2']


def test_post_courses(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post("/api/courses/v1/courses", json={'name': 'Fiesta'})

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_patch_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    patch_mock_call = mocker.patch('requests.patch', return_value=courses_response)

    response = client.patch("/api/courses/v1/courses/1", json={'name': 'Fiesta'})

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_course(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1")

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 200
    assert json.loads(response.data) == [{'id': '1'}]


def test_post_exams(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(201, {'resource': {'id': '1'}})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    post_mock_call = mocker.patch('requests.post', return_value=courses_response)

    response = client.post("/api/courses/v1/courses/1/exams", json={'name': 'Fiesta'})

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    patch_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 200
    assert json.loads(response.data) == {'id': '1'}


def test_delete_exam(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/exams/1")

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/students',
        json={},
        headers={'x-auth-token': 'token-1'},
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
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/students',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_student(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/students/1")

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/students/1',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/professors',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/professors',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


def test_delete_professor(client, mocker):
    authentication_response = ResponseMock(200, user_response_dto)
    courses_response = ResponseMock(200, {'id': '1'})
    get_mock_call = mocker.patch('requests.get', return_value=authentication_response)
    delete_mock_call = mocker.patch('requests.delete', return_value=courses_response)

    response = client.delete("/api/courses/v1/courses/1/professors/1")

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    delete_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/professors/1',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    get_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1/resolutions',
        json={},
        headers={'x-auth-token': 'token-1'},
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

    get_mock_call.assert_any_call(
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1/resolutions',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
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
        'https://ubademy-g2-auth-server!!!!.herokuapp.com/auth-server/v1/users/me',
        json={},
        headers={'x-auth-token': 'token-1'},
    )
    post_mock_call.assert_any_call(
        'https://ubademy-g2-courses!!!!.herokuapp.com/courses/v1/courses/1/exams/1/resolutions/1/evaluate',
        json={'name': 'Fiesta'},
        headers={'x-auth-token': 'token-1'},
    )
    assert response._status_code == 201
    assert json.loads(response.data) == {'resource': {'id': '1'}}


# def test_post_sign_up(client, mocker):
#     request_dto = user_create_request_dto
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/users/signUp", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_sign_in(client, mocker):
#     request_dto = {
#         "email": "joe_doeaasl@gmail.com",
#         "password": "joes super secret password",
#     }
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/users/signIn", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_get_logged_user(client, mocker):
#     forwarded_response = user_response
#     get_mock_call = mocker.patch(
#         'requests.get', side_effect=[authentication_response, courses_response]ResponseMock(200, forwarded_response)
#     )
#
#     response = client.get("/api/auth-server/v1/users/me")
#
#     mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_patch_logged_user(client, mocker):
#     request_dto = {"name": "Foo"}
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.patch', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.patch("/api/auth-server/v1/users/me", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_get_some_user(client, mocker):
#     forwarded_response = user_response
#     get_mock_call = mocker.patch(
#         'requests.get', side_effect=[authentication_response, courses_response]ResponseMock(200, forwarded_response)
#     )
#
#     response = client.get("/api/auth-server/v1/users/someuserid")
#
#     mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_sign_out(client, mocker):
#     request_dto = {"message": "User sign out"}
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_sign_out_unauthorized(client, mocker):
#     request_dto = {"message": "User sign out"}
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(401, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 401
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_admin_sign_up(client, mocker):
#     request_dto = {
#         "email": "joe_doeaasl@gmail.com",
#         "password": "joes super secret password",
#     }
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/admin/signIn", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_admin_sign_in(client, mocker):
#     forwarded_response = [user_response]
#     get_mock_call = mocker.patch(
#         'requests.get', side_effect=[authentication_response, courses_response]ResponseMock(200, forwarded_response)
#     )
#
#     response = client.get("/api/auth-server/v1/admin/users")
#
#     mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_get_admin_get_some_user(client, mocker):
#     forwarded_response = user_response
#     get_mock_call = mocker.patch(
#         'requests.get', side_effect=[authentication_response, courses_response]ResponseMock(200, forwarded_response)
#     )
#
#     response = client.get("/api/auth-server/v1/admin/users/someuserid")
#
#     mock_call.assert_called_once_with(mocker.ANY, json={}, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_admin_sign_out(client, mocker):
#     request_dto = {"message": "User sign out"}
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(200, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/users/signOut", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 200
#     assert json.loads(response.data) == forwarded_response
#
#
# def test_post_admin_sign_out_unauthorized(client, mocker):
#     request_dto = {"message": "User sign out"}
#     forwarded_response = user_response
#     mock_call = mocker.patch(
#         'requests.post', return_value=ResponseMock(401, forwarded_response)
#     )
#
#     response = client.post("/api/auth-server/v1/admin/signOut", json=request_dto)
#
#     mock_call.assert_called_once_with(mocker.ANY, json=request_dto, headers=mocker.ANY)
#     assert response._status_code == 401
#     assert json.loads(response.data) == forwarded_response

"""Sample test suite."""

import json
import logging
import tempfile

# pylint:disable=redefined-outer-name,protected-access
import pytest

from api_gateway.app import create_app
from api_gateway.models import db

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as test_client:
        yield test_client


def test_root(client):
    response = client.get("/")
    assert response._status_code == 200
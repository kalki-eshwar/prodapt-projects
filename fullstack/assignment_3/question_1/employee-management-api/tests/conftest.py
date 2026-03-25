from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

os.environ.setdefault("APP_ENV", "test")

from app.core.dependencies import get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client["employee_management_test"]

    def override_get_db():
        return mock_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

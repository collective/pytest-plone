"""Base fixtures."""
import pytest


@pytest.fixture()
def app(integration):
    return integration["app"]


@pytest.fixture()
def portal(integration):
    return integration["portal"]


@pytest.fixture
def http_request(integration):
    return integration["request"]

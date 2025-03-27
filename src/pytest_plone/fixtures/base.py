"""Base fixtures."""

from OFS.Application import Application
from plone.testing.layer import Layer
from Products.CMFPlone.Portal import PloneSite
from ZPublisher.HTTPRequest import HTTPRequest

import pytest


@pytest.fixture()
def app(integration: Layer) -> Application:
    """Returns the root of a Zope application for an integration Layer.

    Example usage:
    ```python
    def test_app(self, app):
        assert app.title == "Zope"
    ```
    """
    return integration["app"]


@pytest.fixture()
def portal(integration: Layer) -> PloneSite:
    """Returns the default Plone Site for an integration Layer.

    Example usage:
    ```python
    def test_portal(self, portal):
        assert portal.title == "Plone site"
    ```
    """
    return integration["portal"]


@pytest.fixture
def http_request(integration: Layer) -> HTTPRequest:
    """Returns the current request object.

    Example usage:
    ```python
    def test_request(self, request):
        assert request.method == "GET"
    ```
    """
    return integration["request"]

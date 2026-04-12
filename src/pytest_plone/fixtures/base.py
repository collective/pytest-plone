"""Base fixtures."""

from .markers import apply_portal_marker
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
def portal(integration: Layer, request: pytest.FixtureRequest) -> PloneSite:
    """Returns the default Plone Site for an integration Layer.

    Supports ``@pytest.mark.portal`` to apply GenericSetup profiles,
    create content, and grant roles before the test runs.

    Example usage:
    ```python
    def test_portal(self, portal):
        assert portal.title == "Plone site"

    @pytest.mark.portal(
        profiles=["my.addon:testing"],
        content=[{"type": "Document", "id": "doc1", "title": "A document"}],
        roles=["Manager"],
    )
    def test_portal_with_marker(self, portal):
        assert "doc1" in portal
    ```
    """
    portal: PloneSite = integration["portal"]
    apply_portal_marker(portal, request)
    return portal


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

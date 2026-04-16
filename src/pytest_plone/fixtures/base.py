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


@pytest.fixture()
def functional_app(functional: Layer) -> Application:
    """Returns the root of a Zope application for a functional Layer.

    Mirrors :func:`app` but bound to the ``functional`` layer. Use this in
    REST API, browser, or other tests that require transaction-level
    isolation instead of the integration-layer stacked-DemoStorage.

    Example usage:
    ```python
    def test_functional_app(self, functional_app):
        assert functional_app.title == "Zope"
    ```
    """
    return functional["app"]


@pytest.fixture()
def functional_portal(functional: Layer, request: pytest.FixtureRequest) -> PloneSite:
    """Returns the default Plone Site for a functional Layer.

    Mirrors :func:`portal` but bound to the ``functional`` layer and also
    honors ``@pytest.mark.portal`` for GenericSetup profiles, pre-created
    content, and test-user roles.

    Example usage:
    ```python
    def test_functional_portal(self, functional_portal):
        assert functional_portal.title == "Plone site"
    ```
    """
    portal: PloneSite = functional["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture
def functional_http_request(functional: Layer) -> HTTPRequest:
    """Returns the current request object for a functional Layer.

    Mirrors :func:`http_request` but bound to the ``functional`` layer.

    Example usage:
    ```python
    def test_functional_request(self, functional_http_request):
        assert functional_http_request.method == "GET"
    ```
    """
    return functional["request"]

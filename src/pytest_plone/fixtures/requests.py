"""Request-builder fixtures for REST API / functional HTTP tests."""

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import _types as t
from urllib.parse import urljoin
from urllib.parse import urlparse

import pytest
import requests


_ROLE_AUTH: dict[str, tuple[str, str] | None] = {
    "Manager": (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
    "Anonymous": None,
}


class RelativeSession(requests.Session):
    """`requests.Session` that resolves relative URLs against a base URL.

    Minimal standalone equivalent of ``plone.restapi.testing.RelativeSession``
    — avoids pulling the full ``plone.restapi[test]`` import chain into
    pytest-plone's runtime.
    """

    def __init__(self, base_url: str) -> None:
        super().__init__()
        if not base_url.endswith("/"):
            base_url += "/"
        self._base_url = base_url

    def request(self, method: str, url: str, **kwargs):  # type: ignore[override]
        if urlparse(url).scheme not in ("http", "https"):
            url = urljoin(self._base_url, url.lstrip("/"))
        return super().request(method, url, **kwargs)


@pytest.fixture
def request_factory(
    functional_portal: PloneSite, request: pytest.FixtureRequest
) -> t.RequestFactory:
    """Builder fixture for HTTP request sessions against the functional portal.

    Returns a callable that produces a :class:`RelativeSession` bound to the
    portal URL. The session is closed automatically at the end of the test.

    Parameters accepted by the returned callable:

    - ``role`` — ``"Manager"`` or ``"Anonymous"`` (default). Maps to
      predefined test credentials. Unknown roles raise ``ValueError`` — use
      ``basic_auth`` for other identities.
    - ``basic_auth`` — ``(username, password)`` tuple; takes precedence over
      ``role`` when provided.
    - ``api`` — when ``True`` (default), the base URL is suffixed with
      ``++api++`` so relative requests hit the REST API traverser.

    Example usage:
    ```python
    def test_list_content(request_factory):
        session = request_factory(role="Manager")
        response = session.get("/")
        assert response.status_code == 200
    ```
    """

    def factory(
        *,
        role: str = "Anonymous",
        basic_auth: tuple[str, str] | None = None,
        api: bool = True,
    ) -> RelativeSession:
        base_url = functional_portal.absolute_url()
        if api:
            base_url = f"{base_url}/++api++"
        session = RelativeSession(base_url)
        session.headers.update({"Accept": "application/json"})
        if basic_auth is not None:
            session.auth = basic_auth
        elif role in _ROLE_AUTH:
            auth = _ROLE_AUTH[role]
            if auth is not None:
                session.auth = auth
        else:
            raise ValueError(
                f"Unknown role {role!r}. Pass role='Manager' or 'Anonymous', "
                "or use basic_auth=(username, password) for other identities."
            )
        request.addfinalizer(session.close)
        return session

    return factory


@pytest.fixture
def manager_request(request_factory: t.RequestFactory) -> RelativeSession:
    """A `RelativeSession` authenticated as the portal owner (Manager).

    Example usage:
    ```python
    def test_admin_endpoint(manager_request):
        response = manager_request.get("/@controlpanels")
        assert response.status_code == 200
    ```
    """
    return request_factory(role="Manager")


@pytest.fixture
def anon_request(request_factory: t.RequestFactory) -> RelativeSession:
    """A `RelativeSession` with no authentication (Anonymous).

    Example usage:
    ```python
    def test_public_endpoint(anon_request):
        response = anon_request.get("/")
        assert response.status_code == 200
    ```
    """
    return request_factory(role="Anonymous")

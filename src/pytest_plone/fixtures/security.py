"""Security fixtures."""

from pytest_plone import _types as t
from pytest_plone.fixtures import markers

import pytest


@pytest.fixture(scope="session")
def grant_roles() -> t.RolesGranter:
    """Grant local roles to the test user on the portal.

    Example usage:
    ```python
    def test_manager_action(portal, grant_roles):
        grant_roles(portal, ["Manager"])
        # test user now has Manager role on portal
    ```
    """

    def func(context: t.Context, roles: list[str]) -> None:
        markers.grant_roles(context, roles)

    return func

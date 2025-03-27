"""Fixtures used in add-on install / uninstall tests."""

from plone import api
from plone.base.utils import get_installer
from plone.browserlayer import utils
from Products.CMFPlone.controlpanel.browser.quickinstaller import InstallerView
from Products.CMFPlone.Portal import PloneSite
from Products.GenericSetup.tool import SetupTool
from pytest_plone import _types as t
from zope.interface.interface import InterfaceClass

import pytest


@pytest.fixture
def installer(portal: PloneSite) -> InstallerView:
    """Portal helper for managing add-ons using GenericSetup.

    Example usage:
    ```python
    PACKAGE_NAME = "collective.person"

    class TestSetupUninstall:
        @pytest.fixture(autouse=True)
        def uninstalled(self, installer):
            installer.uninstall_product(PACKAGE_NAME)
    ```
    """
    return get_installer(portal)


@pytest.fixture
def browser_layers(portal: PloneSite) -> list[InterfaceClass]:
    """List of browser layers registered in a portal.

    Example usage:
    ```python

    def test_browserlayer(self, browser_layers):
        from collective.person.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers
    ```
    """
    return utils.registered_layers()


@pytest.fixture
def controlpanel_actions(portal: PloneSite) -> list[str]:
    """List of identifiers (id) of control panel actions.

    Example usage:
    ```python

    def test_controlpanel_installed(self, controlpanel_actions):
        assert "MyControlPanel" in controlpanel_actions
    ```
    """
    controlpanel = portal.portal_controlpanel
    return [a.getAction(portal)["id"] for a in controlpanel.listActions()]


@pytest.fixture
def setup_tool(portal: PloneSite) -> SetupTool:
    """Return the portal_setup for the current portal.

    Example usage:
    ```python

    def test_profile_version(self, setup_tool):
        name = "profile-collective.person:default
        version = setup_tool.getLastVersionForProfile(name)
        return version[0] == "1000
    ```
    """
    return api.portal.get_tool("portal_setup")


@pytest.fixture
def profile_last_version(setup_tool: SetupTool) -> t.ProfileVersionGetter:
    """Provides a method to return the last version for a profile.

    Example usage:
    ```python
    PACKAGE_NAME = "collective.person"

    def test_latest_version(self, profile_last_version):
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1000"
    ```
    """

    def profile_last_version(profile: str) -> str:
        """Return the last version for a profile."""
        version = setup_tool.getLastVersionForProfile(profile)
        return version[0] if version else ""

    return profile_last_version

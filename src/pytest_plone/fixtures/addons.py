"""Fixtures used in add-on install / uninstall tests."""

from plone import api
from plone.base.utils import get_installer
from plone.browserlayer import utils
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture
def installer(portal: PloneSite):
    return get_installer(portal)


@pytest.fixture
def browser_layers(portal: PloneSite):
    return utils.registered_layers()


@pytest.fixture
def controlpanel_actions(portal: PloneSite) -> list:
    controlpanel = portal.portal_controlpanel
    return [a.getAction(portal)["id"] for a in controlpanel.listActions()]


@pytest.fixture
def setup_tool(integration):
    return api.portal.get_tool("portal_setup")


@pytest.fixture
def profile_last_version(setup_tool):
    def profile_last_version(name: str) -> str:
        version = setup_tool.getLastVersionForProfile(name)
        return version[0] if version else ""

    return profile_last_version

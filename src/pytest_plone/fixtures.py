from plone.base.utils import get_installer
from plone.browserlayer import utils

import pytest


@pytest.fixture()
def portal(integration):
    return integration["portal"]


@pytest.fixture
def http_request(integration):
    return integration["request"]


@pytest.fixture
def installer(portal):
    return get_installer(portal)


@pytest.fixture
def browser_layers(portal):
    return utils.registered_layers()


@pytest.fixture
def controlpanel_actions(portal):
    controlpanel = portal.portal_controlpanel
    return [a.getAction(portal)["id"] for a in controlpanel.listActions()]

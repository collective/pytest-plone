<h1 align="center">pytest-plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Status](https://img.shields.io/pypi/status/pytest-plone)](https://pypi.org/project/pytest-plone/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/pytest-plone)](https://pypi.org/project/pytest-plone/)

[![Code analysis checks](https://github.com/collective/pytest-plone/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/pytest-plone/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/pytest-plone/actions/workflows/tests.yml/badge.svg)](https://github.com/collective/pytest-plone/actions/workflows/tests.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/pytest-plone)](https://github.com/collective/pytest-plone)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/pytest-plone?style=social)](https://github.com/collective/pytest-plone)
</div>

**pytest-plone** is a [Pytest](https://docs.pytest.org) plugin providing fixtures and helpers to test [Plone](https://plone.org) add-ons.

This plugin is built on top of [gocept.pytestlayer](https://github.com/gocept/gocept.pytestlayer).

## Usage

In your top-level `conftest.py` import your testing layers, and also import `fixtures_factory` -- which will accept a iterator of tuples containing the testing layer and a prefix to be used to generate the needed pytest fixtures.

```python
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


globals().update(
    fixtures_factory(
        (
            (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
            (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
        )
    )
)
```

In the code above, the following pytest fixtures will be available to your tests:

| Fixture | Scope |
| --- | --- |
| functional_session | Session |
| functional_class | Class |
| functional | Function |
| integration_session | Session |
| integration_class | Class |
| integration | Function |


## Fixtures

### portal

|  |  |
| --- | --- |
| Description | Portal object |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_portal_title(portal):
    """Test portal title."""
    assert portal.title == "Plone Site"

```

### http_request

|  |  |
| --- | --- |
| Description | HTTP Request |
| Required Fixture | **integration** |
| Scope | **Function** |


```python
from plone import api


def test_myproduct_controlpanel_view(portal, http_request):
    """Test myproduct_controlpanel browser view is available."""
    view = api.content.get_view(
        "myproduct-controlpanel", portal, http_request
    )
    assert view is not None

```

### installer

|  |  |
| --- | --- |
| Description | Installer browser view. Used to install/uninstall/check for an add-on. |
| Required Fixture | **integration** |
| Scope | **Function** |


```python
import pytest


PACKAGE_NAME = "myproduct"


@pytest.fixture
def uninstall(installer):
    """Fixture to uninstall a package."""
    installer.uninstall_product(PACKAGE_NAME)


def test_product_installed(installer):
    """Test if myproduct is installed."""
    assert installer.is_product_installed(PACKAGE_NAME) is True

@pytest.mark.parametrize(
    "package",
    [
        "collective.casestudy",
        "pytest-plone",
    ]
)
def test_dependency_installed(installer, package):
    """Test if dependency is installed."""
    assert installer.is_product_installed(package) is True

```

### browser_layers

|  |  |
| --- | --- |
| Description | List of available browser layers. Used to test if a specific browser layer is registered. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_browserlayer(browser_layers):
    """Test that IMyProductLayer is registered."""
    from myproduct.interfaces import IMyProductLayer


    assert IMyProductLayer in browser_layers

```

### controlpanel_actions

|  |  |
| --- | --- |
| Description | List of control panel actions ids. Used to test if a specific control panel is installed or not. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_configlet_install(controlpanel_actions):
    """Test if control panel is installed."""
    assert "myproductcontrolpanel" in controlpanel_actions

```

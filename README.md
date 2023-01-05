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

**pytest-plone** is a [pytest](https://docs.pytest.org) plugin providing fixtures and helpers to test [Plone](https://plone.org) add-ons.


This package is built on top of [gocept.pytestlayer](https://github.com/gocept/gocept.pytestlayer).


## Reasoning

Despite the fact Plone, and Zope, have their codebases tested with `unittest`, over the years
`pytest` became the most popular choice for testing in Python.

`pytest` is more flexible and easier to use than `unittest` and has a rich ecosystem of plugins that you can use to extend its functionality.
## Warning

**THIS PACKAGE IS NOT CONSIDERED TO BE STABLE AND FIXTURES COULD CHANGE BEFORE A FINAL RELEASE**

## Usage

In your top-level `conftest.py` import your testing layers, and also import `fixtures_factory` -- which will accept a iterator of tuples containing the testing layer and a prefix to be used to generate the needed pytest fixtures.

```python
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


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

### app

|  |  |
| --- | --- |
| Description | Zope root |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_app(app):
    """Test portal title."""
    assert app.getPhysicalPath() == ("", )

```

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

### get_fti

|  |  |
| --- | --- |
| Description | Function to get the Factory Type Info (FTI) for a content type. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_get_fti(get_fti):
    """Test if Document fti is installed."""
    assert get_fti("Document") is not None

```

### get_behaviors

|  |  |
| --- | --- |
| Description | Function to list behaviors for a content type. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
import pytest


def test_block_in_document(get_behaviors):
    """Test if blocks behavior is installed for Document."""
    assert "volto.blocks" in get_behaviors("Document")


@pytest.mark.parametrize(
    "behavior",
    [
        "plone.dublincore",
        "plone.namefromtitle",
        "plone.shortname",
        "plone.excludefromnavigation",
        "plone.relateditems",
        "plone.versioning",
        "volto.blocks",
        "volto.navtitle",
        "volto.preview_image",
        "volto.head_title",
    ],
)
def test_has_behavior(self, get_behaviors, behavior):
    assert behavior in get_behaviors("Document")
```

### get_vocabulary

|  |  |
| --- | --- |
| Description | Function to get a named vocabulary. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
from zope.schema.vocabulary import SimpleVocabulary

VOCAB = "plone.app.vocabularies.AvailableContentLanguages"

def test_get_vocabulary(get_vocabulary):
    """Test plone.app.vocabularies.AvailableContentLanguages."""
    vocab = get_vocabulary(VOCAB)
    assert vocab is not None
    assert isinstance(vocab, SimpleVocabulary)

```

### setup_tool

|  |  |
| --- | --- |
| Description | Portal Setup tool. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_setup_tool(setup_tool):
    """Test setup_tool."""
    assert setup_tool is not None

```

### profile_last_version

|  |  |
| --- | --- |
| Description | Function to get the last version of a profile. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
PACKAGE_NAME = "collective.case_study"

def test_last_version(profile_last_version):
    """Test setup_tool."""
    profile = f"{PACKAGE_NAME}:default"
    version = profile_last_version(profile)
    assert version == "1000"

```
## Plugin Development

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.8 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```

To run tests for this package:

```bash
make test
```

By default we use the latest Plone version in the 6.x series.

## License

The project is licensed under the GPLv2.

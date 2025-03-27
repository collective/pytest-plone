from collections.abc import Iterable
from plone.testing.layer import Layer
from typing import Any

import zope.pytestlayer.fixture


def fixtures_factory(test_layers: Iterable[tuple[Layer, str]]) -> dict[str, Any]:
    """Create pytest fixtures for a group of plone.testing.layer.Layer.

    :param test_layer: Iterable (tuple or list) containing two-element tuple with the
                       Layer object and a string with the prefix to use for fixtures
                       created for that layer.

    ```python
        fixtures_factory(
            (
                (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
                (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
            )
        )
    ```
    """
    fixtures = {}
    for layer, prefix in test_layers:
        fixtures.update(
            zope.pytestlayer.fixture.create(
                layer,
                session_fixture_name=f"{prefix}_session",
                class_fixture_name=f"{prefix}_class",
                function_fixture_name=prefix,
            )
        )
    return fixtures

import pytest


pytest_plugins = ["pytester"]


@pytest.fixture
def testdir(pytester):
    # create a temporary conftest.py file
    pytester.makeconftest(
        """
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
            """
    )
    return pytester

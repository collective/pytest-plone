import pytest


pytest_plugins = ["pytester"]


@pytest.fixture
def testdir(pytester):
    # create a temporary conftest.py file
    pytester.makeconftest(
        """
        import gocept.pytestlayer.fixture
        from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING
        from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_INTEGRATION_TESTING


        _FIXTURES = (
            (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
            (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
        )


        def fixtures():
            fixtures = {}
            for item, prefix in _FIXTURES:
                fixtures.update(
                    gocept.pytestlayer.fixture.create(
                        item,
                        session_fixture_name=f"{prefix}_session",
                        class_fixture_name=f"{prefix}_class",
                        function_fixture_name=prefix,
                    )
                )
            return fixtures

        globals().update(fixtures())
    """
    )
    return pytester

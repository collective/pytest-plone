import pytest


@pytest.mark.no_cover
def test_fixture_exists(testdir, fixture_name: str):
    """Test pytest-plone fixtures exist."""

    pyfile = f"""

    def test_{fixture_name}_exists({fixture_name}):
        # Just pass the test, because if a fixture is not available,
        # it will raise an error
        assert True

    """
    testdir.makepyfile(pyfile)

    # run all tests with pytest
    result = testdir.runpytest_subprocess()

    # check that all tests passed
    result.assert_outcomes(passed=1)

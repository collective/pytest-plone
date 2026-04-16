"""Tests for the ``uninstalled`` fixture."""

import pytest


@pytest.mark.no_cover
class TestUninstalledFixture:
    """The ``uninstalled`` fixture uninstalls the configured add-on."""

    def test_uninstalled_removes_product(self, testdir):
        testdir.makepyfile(
            """
            import pytest


            PACKAGE_NAME = "plone.app.multilingual"


            @pytest.fixture
            def package_name() -> str:
                return PACKAGE_NAME


            @pytest.fixture(autouse=True)
            def ensure_installed(installer):
                if not installer.is_product_installed(PACKAGE_NAME):
                    installer.install_product(PACKAGE_NAME)


            class TestSetupUninstall:
                @pytest.fixture(autouse=True)
                def _uninstalled(self, uninstalled):
                    pass

                def test_product_uninstalled(self, installer):
                    assert installer.is_product_installed(PACKAGE_NAME) is False
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_uninstalled_without_package_name_errors(self, testdir):
        testdir.makepyfile(
            """
            def test_missing_package_name(uninstalled):
                pass
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*fixture 'package_name' not found*"])

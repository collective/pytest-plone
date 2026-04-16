"""Tests for request-builder fixtures."""

import pytest


@pytest.mark.no_cover
class TestRequestFactory:
    """``request_factory`` returns a configured RelativeSession."""

    def test_default_is_anonymous(self, testdir):
        testdir.makepyfile(
            """
            def test_anonymous(request_factory, functional_portal):
                session = request_factory()
                assert session.auth is None
                expected = f"{functional_portal.absolute_url()}/++api++/"
                assert session._base_url == expected
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_manager_role(self, testdir):
        testdir.makepyfile(
            """
            from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

            def test_manager(request_factory):
                session = request_factory(role="Manager")
                assert session.auth == (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_api_false_skips_api_prefix(self, testdir):
        testdir.makepyfile(
            """
            def test_no_api_prefix(request_factory, functional_portal):
                session = request_factory(api=False)
                expected = f"{functional_portal.absolute_url()}/"
                assert session._base_url == expected
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_basic_auth_overrides_role(self, testdir):
        testdir.makepyfile(
            """
            def test_explicit_credentials(request_factory):
                session = request_factory(
                    role="Manager", basic_auth=("alice", "s3cret")
                )
                assert session.auth == ("alice", "s3cret")
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_unknown_role_raises(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            def test_unknown_role(request_factory):
                with pytest.raises(ValueError, match="Unknown role"):
                    request_factory(role="Reviewer")
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_accept_header(self, testdir):
        testdir.makepyfile(
            """
            def test_accept_json(request_factory):
                session = request_factory()
                assert session.headers["Accept"] == "application/json"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestConvenienceFixtures:
    """``manager_request`` and ``anon_request`` wrap ``request_factory``."""

    def test_manager_request(self, testdir):
        testdir.makepyfile(
            """
            from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

            def test_manager(manager_request):
                assert manager_request.auth == (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_anon_request(self, testdir):
        testdir.makepyfile(
            """
            def test_anon(anon_request):
                assert anon_request.auth is None
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestRelativeSessionBehavior:
    """`RelativeSession` resolves relative URLs against the base URL."""

    def test_relative_url_resolution(self, testdir):
        testdir.makepyfile(
            """
            from pytest_plone.fixtures.requests import RelativeSession

            def test_prepends_base(monkeypatch):
                session = RelativeSession("http://example.com/api")
                seen = {}

                def fake_request(self, method, url, **kw):
                    seen["url"] = url
                    return None

                import requests
                monkeypatch.setattr(requests.Session, "request", fake_request)
                session.request("GET", "/@types")
                assert seen["url"] == "http://example.com/api/@types"

            def test_absolute_url_passthrough(monkeypatch):
                session = RelativeSession("http://example.com/api")
                seen = {}

                def fake_request(self, method, url, **kw):
                    seen["url"] = url
                    return None

                import requests
                monkeypatch.setattr(requests.Session, "request", fake_request)
                session.request("GET", "http://other.example/x")
                assert seen["url"] == "http://other.example/x"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

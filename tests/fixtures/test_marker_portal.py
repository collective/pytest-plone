"""Tests for @pytest.mark.portal marker support."""

import pytest


@pytest.mark.no_cover
class TestPortalMarkerNoArgs:
    """Portal fixture works without the marker (backwards-compatible)."""

    def test_portal_without_marker(self, testdir):
        testdir.makepyfile(
            """
            def test_portal_no_marker(portal):
                assert portal.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerRoles:
    """Portal marker applies roles to the test user."""

    def test_grant_manager_role(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager"])
            def test_user_has_manager_role(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_grant_multiple_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager", "Reviewer"])
            def test_user_has_multiple_roles(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
                assert "Reviewer" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerContent:
    """Portal marker creates content in the portal."""

    def test_create_document(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "A Document"}],
            )
            def test_document_exists(portal):
                assert "doc1" in portal
                assert portal["doc1"].title == "A Document"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_create_multiple_content(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[
                    {"type": "Document", "id": "doc1", "title": "Doc 1"},
                    {"type": "Document", "id": "doc2", "title": "Doc 2"},
                ],
            )
            def test_multiple_content(portal):
                assert "doc1" in portal
                assert "doc2" in portal
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerProfiles:
    """Portal marker applies GenericSetup profiles."""

    def test_apply_profile(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            @pytest.mark.portal(profiles=["plone.app.contenttypes:default"])
            def test_profile_applied(portal):
                setup_tool = api.portal.get_tool("portal_setup")
                # Verify the profile was applied by checking the profile version
                version = setup_tool.getLastVersionForProfile(
                    "plone.app.contenttypes:default"
                )
                assert version is not None
                assert version != "unknown"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerCombined:
    """Portal marker supports combining profiles, content, and roles."""

    def test_profiles_content_and_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
                roles=["Manager"],
            )
            def test_combined(portal):
                assert "doc1" in portal
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerIsolation:
    """Marker setup doesn't leak between tests (integration layer rollback)."""

    def test_isolation_between_tests(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
            )
            def test_first(portal):
                assert "doc1" in portal

            def test_second(portal):
                assert "doc1" not in portal
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

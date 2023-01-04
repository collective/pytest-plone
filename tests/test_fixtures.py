def test_all_fixtures(testdir):
    """Test installer fixture."""

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_http_request(http_request):
            assert http_request is not None

        def test_installer(installer):
            assert installer is not None

        def test_portal(portal):
            assert portal.portal_type == "Plone Site"

        def test_browser_layers(browser_layers):
            assert isinstance(browser_layers, list)

        def test_controlpanel_actions(controlpanel_actions):
            assert isinstance(controlpanel_actions, list)

    """
    )

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all tests passed
    result.assert_outcomes(passed=5)

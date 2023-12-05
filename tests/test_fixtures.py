def test_all_fixtures(testdir):
    """Test pytest-plone fixtures exist."""
    fixtures = [
        "app",
        "browser_layers",
        "controlpanel_actions",
        "generate_mo",
        "get_behaviors",
        "get_fti",
        "get_vocabulary",
        "http_request",
        "installer",
        "portal",
        "profile_last_version",
        "setup_tool",
    ]
    pyfile = ""
    for fixture in fixtures:
        pyfile = f"""
        {pyfile}

        def test_{fixture}_exists({fixture}):
            # Just pass the test, because if a fixture is not available,
            # it will raise an error
            assert True

        """

    testdir.makepyfile(pyfile)

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all tests passed
    result.assert_outcomes(passed=len(fixtures))

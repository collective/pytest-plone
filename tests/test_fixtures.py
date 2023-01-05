def test_all_fixtures(testdir):
    """Test pytest-plone fixtures exist."""

    fixtures = [
        "app",
        "browser_layers",
        "controlpanel_actions",
        "get_behaviors",
        "get_fti",
        "get_vocabulary",
        "http_request",
        "installer",
        "profile_last_version",
        "portal",
        "setup_tool",
    ]
    pyfile = ""
    for fixture in fixtures:
        pyfile = f"""
        {pyfile}

        def test_{fixture}({fixture}):
            assert {fixture} is not None

        """

    testdir.makepyfile(pyfile)

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all tests passed
    result.assert_outcomes(passed=len(fixtures))

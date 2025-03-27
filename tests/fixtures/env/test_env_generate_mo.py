TEST_FILES = {
    "test_generate_mo_result_no_env.py": """
    import os

    def test_generate_mo_result(generate_mo):
        assert os.getenv("zope_i18n_compile_mo_files") == "1"

    """,
    "test_generate_mo_result_with_env.py": """
    import pytest
    import os

    @pytest.fixture(scope="session", autouse=True)
    def set_i18n_var():
        os.environ["zope_i18n_compile_mo_files"] = "2"

    def test_generate_mo_result():
        assert os.getenv("zope_i18n_compile_mo_files") == "2"

    """,
}


def test_generate_mo(testdir):
    """Test generate_mo adds environment variable."""
    testdir.makepyfile(**TEST_FILES)
    # run all tests with pytest
    result = testdir.runpytest()
    # check that all tests passed
    result.assert_outcomes(passed=len(TEST_FILES))

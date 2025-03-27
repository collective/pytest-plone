"""Environment fixtures."""

from collections.abc import Generator

import os
import pytest


@pytest.fixture(scope="session")
def generate_mo() -> Generator[None]:
    """Compile available .po files and generate .mo files.

    This is a session fixture, as it needs to compile files just once.
    """
    # Set environment variable
    key = "zope_i18n_compile_mo_files"
    current_value = os.getenv(key, None)
    os.environ[key] = "1"
    try:
        yield
    finally:
        # Revert to previous state
        if current_value is None:
            os.environ.pop(key)
        else:
            os.environ[key] = current_value

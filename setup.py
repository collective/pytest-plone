"""Installer for the pytest-plone package."""
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""


description = "Pytest plugin to test Plone addons"

setup(
    name="pytest-plone",
    version="0.2.0",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
    keywords="Plone Pytest Testing",
    author="Plone",
    author_email="test@plone.org",
    url="http://pypi.python.org/pypi/pytest-plone",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Plone",
        "setuptools",
        "gocept.pytestlayer",
        "plone.app.testing",
        "plone.app.robotframework",
        "pytest",
    ],
    extras_require={},
    entry_points={"pytest11": ["plone = pytest_plone.fixtures"]},
)

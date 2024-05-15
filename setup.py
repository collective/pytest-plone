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
    version="0.5.0",
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
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
    keywords="Plone Pytest Testing",
    author="Plone",
    author_email="test@plone.org",
    url="http://pypi.python.org/pypi/pytest-plone",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/pytest-plone",
        "Source": "https://github.com/collective/pytest-plone",
        "Tracker": "https://github.com/collective/pytest-plone/issues",
    },
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "zope.pytestlayer",
        "plone.api",
        "plone.app.testing",
        "plone.base",
        "plone.browserlayer",
        "plone.dexterity",
        "Products.CMFPlone",
        "pytest<8.0.0",
        "setuptools",
        "zope.component",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "pytest-cov",
        ],
    },
    entry_points={"pytest11": ["plone = pytest_plone.fixtures"]},
)

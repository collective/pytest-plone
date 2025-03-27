# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0a1 (2025-03-27)


### Breaking changes:

- Drop support for Python 3.8 @ericof [#17](https://github.com/collective/pytest-plone/issues/17)
- Drop support for Python 3.9 @ericof [#18](https://github.com/collective/pytest-plone/issues/18)


### New features:

- Add support for Python 3.13 @ericof [#19](https://github.com/collective/pytest-plone/issues/19)
- Add support for Plone 6.1 @ericof [#20](https://github.com/collective/pytest-plone/issues/20)
- Add docstring for every fixture provided by pytest-plone @ericof [#24](https://github.com/collective/pytest-plone/issues/24)


### Internal:

- Move from `setuptools` to `hatchling` for package build. @ericof [#21](https://github.com/collective/pytest-plone/issues/21)
- Package metadata now lives in `pyproject.toml`. @ericof [#22](https://github.com/collective/pytest-plone/issues/22)
- Use UV to manage the development environment. @ericof [#23](https://github.com/collective/pytest-plone/issues/23)
- Add default `.vscode` configuration @ericof [#25](https://github.com/collective/pytest-plone/issues/25)
- Add type hints and check codebase with `mypy` [#27](https://github.com/collective/pytest-plone/issues/27)
- Don't reformat `.md` files. @stevepiercy [#28](https://github.com/collective/pytest-plone/issues/28)

## 0.5.0 (2024-05-15)


### New features:

- Add fixture `generate_mo` to compile translation files during tests [@ericof] #5
- Move from `gocept.pytestlayer` to `zope.pytestlayer` [@ericof] #11


### Internal:

- Implement plone/meta [@ericof] #6
- Clean up dependencies for pytest-plone [@thet], [@gforcada], [@ericof] #9
- Pin pytest version to be lower than 8.0 [@ericof] #12
- Update plone/meta [@ericof] #13

## 0.2.0 (2023-01-05)

- Add `app` fixture.
  [ericof]

- Add `setup_tool` and `profile_last_version` fixtures.
  [ericof]

- Add `get_fti` and `get_behaviors` fixtures.
  [ericof]

- Add `get_vocabulary` fixture.
  [ericof]


## 0.1.0 (2023-01-04)

- Fixtures `portal`, `http_request`, `installer`, `browser_layers`, `controlpanel_actions`
  [ericof]

- Initial release
  [ericof]

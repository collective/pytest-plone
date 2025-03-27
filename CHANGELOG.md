# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

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

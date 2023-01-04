import gocept.pytestlayer.fixture


def fixtures_factory(test_layers):
    fixtures = {}
    for item, prefix in test_layers:
        fixtures.update(
            gocept.pytestlayer.fixture.create(
                item,
                session_fixture_name=f"{prefix}_session",
                class_fixture_name=f"{prefix}_class",
                function_fixture_name=prefix,
            )
        )
    return fixtures

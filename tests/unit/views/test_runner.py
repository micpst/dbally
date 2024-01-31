from dbally.views.registry import ViewRegistry
from dbally.views.runner import Runner
from tests.unit.views.test_sqlalchemy_base import MockSqlAlchemyView


def test_runner() -> None:
    """
    Tests that the runner works correctly
    """
    registry = ViewRegistry()
    registry.register(MockSqlAlchemyView)
    runner = Runner("MockSqlAlchemyView", registry)
    runner.apply_filters("method_foo(1) and method_bar('London', 2020)")
    runner.apply_actions("action_baz()\naction_qux(5)")
    sql = runner.generate_sql().replace("\n", "")
    assert sql == "SELECT 'test' AS foo WHERE 1 AND 'hello London in 2020' ORDER BY foo LIMIT 5"
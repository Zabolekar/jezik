import pytest # type: ignore

def pytest_addoption(parser):
   parser.addoption("--quick", action="store_true", default=False,
                    help="skip time-consuming data validation")

def pytest_collection_modifyitems(config, items):
   for item in items:
      if "slow" in item.keywords and config.getoption("--quick"):
         item.add_marker(pytest.mark.skip(reason=
               "data validation is slow and only runs without --quick option"))

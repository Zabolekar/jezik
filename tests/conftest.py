def pytest_addoption(parser):
   parser.addoption("--quick", action="store_true", dest="quick",
                    default=False, help="skip time-consuming data validation")
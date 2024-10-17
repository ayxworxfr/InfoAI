import os

import pytest


@pytest.fixture()
def manual():
    if os.environ.get("MANUAL"):
        return True
    else:
        return False

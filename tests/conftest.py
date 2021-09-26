import pathlib
import sys

import pytest
from main import Item

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)


@pytest.fixture
def item():
    return Item(name='Banana', price=2.99, tax=0.25, description='One pound of banana')

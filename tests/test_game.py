import pytest

from game import Game
from config import Config


@pytest.mark.constructor
@pytest.mark.parametrize("path", ["somename", "idk"])
def test_get_wrong_image(path):
    some_config = Config((10, 10), 15, (800, 800), "custom")
    with pytest.raises(Exception):
        Game(some_config).get_image(path)


@pytest.mark.constructor
@pytest.mark.parametrize("path", ["stopwatch", "flags"])
def test_get_image(path):
    some_config = Config((10, 10), 15, (800, 800), "custom")
    assert Game(some_config).get_image(path).get_height() == 32 and Game(some_config).get_image(path).get_width() == 32

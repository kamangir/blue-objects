import pytest
import glob

from blue_objects.graphics.gif import generate_animated_gif
from blue_objects import objects

from abcli.plugins.testing import download_object


@pytest.mark.parametrize(
    ["object_name", "scale"],
    [
        ["void", 1],
        ["2024-05-07-18-45-13-31678", 2],
    ],
)
def test_graphics_generate_animated_gif(
    object_name: str,
    scale: int,
):
    assert download_object(object_name)

    list_of_images = list(glob.glob(objects.path_of("*.png", object_name)))
    if object_name != "void":
        assert list_of_images

    assert generate_animated_gif(
        list_of_images,
        objects.path_of("test.gif", object_name),
        scale=scale,
    )
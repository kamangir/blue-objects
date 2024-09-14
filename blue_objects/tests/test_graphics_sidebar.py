import pytest
import numpy as np

from blue_objects import file, objects
from blue_objects.graphics.sidebar import add_sidebar
from blue_objects.env import VANWATCH_TEST_OBJECT, DUMMY_TEXT


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_graphics_sidebar_add_side_bar(object_name: str):
    assert objects.download(object_name)

    success, image = file.load_image(
        objects.path_of(
            "Victoria41East.jpg",
            object_name,
        )
    )
    assert success

    output_image = add_sidebar(
        image,
        [DUMMY_TEXT for _ in range(5)],
        [np.zeros((100, 100, 3), dtype=np.uint8) for _ in range(3)],
    )
    assert isinstance(output_image, np.ndarray)

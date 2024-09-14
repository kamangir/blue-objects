import pytest
import numpy as np

from blue_objects import file, objects
from blue_objects.graphics.frame import add_frame
from blue_objects.env import VANWATCH_TEST_OBJECT


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_graphics_frame_add_frame(object_name: str):
    assert objects.download(object_name)

    success, matrix = file.load_image(
        objects.path_of(
            "Victoria41East.jpg",
            object_name,
        )
    )
    assert success

    assert isinstance(
        add_frame(matrix, width=12),
        np.ndarray,
    )

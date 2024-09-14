import pytest
import numpy as np

from blue_objects import file, objects
from blue_objects.graphics.text import add_label, render_text
from blue_objects.env import VANWATCH_TEST_OBJECT, DUMMY_TEXT


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_graphics_text_add_label(object_name: str):
    assert objects.download(object_name)

    success, image = file.load_image(
        objects.path_of(
            "Victoria41East.jpg",
            object_name,
        )
    )
    assert success

    assert isinstance(
        add_label(
            image=image,
            x=10,
            y=20,
            label=DUMMY_TEXT,
        ),
        np.ndarray,
    )


def test_graphics_text_render_text():
    assert isinstance(
        render_text(
            text=[DUMMY_TEXT for _ in range(10)],
        ),
        np.ndarray,
    )

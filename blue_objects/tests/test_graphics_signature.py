import pytest
import numpy as np

from blue_objects import file, objects
from blue_objects.graphics.signature import add_signature
from blue_objects.env import VANWATCH_TEST_OBJECT, DUMMY_TEXT


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_graphics_signature_add_signature(object_name: str):
    assert objects.download(object_name)

    success, image = file.load_image(
        objects.path_of(
            "Victoria41East.jpg",
            object_name,
        )
    )
    assert success

    output_image = add_signature(
        image,
        header=[DUMMY_TEXT],
        footer=[DUMMY_TEXT, DUMMY_TEXT],
    )

    assert isinstance(output_image, np.ndarray)

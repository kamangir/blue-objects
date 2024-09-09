import pytest
import numpy as np

from blue_objects import file, objects
from blue_objects.graphics.signature import add_signature
from blue_objects.env import VANWATCH_TEST_OBJECT


# https://www.randomtextgenerator.com/
dummy_text = "This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text."


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_add_signature(object_name):
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
        header=[dummy_text],
        footer=[dummy_text, dummy_text],
    )

    assert isinstance(output_image, np.ndarray)

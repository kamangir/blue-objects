import pytest
from typing import Callable

from blue_objects.file.load import (
    load_geodataframe,
    load_geojson,
    load_image,
    load_json,
    load_text,
)
from blue_objects import objects
from blue_objects.tests.test_objects import test_object


@pytest.mark.parametrize(
    ["func", "filename"],
    [
        [load_geodataframe, "vancouver.geojson"],
        [load_geojson, "vancouver.geojson"],
        [load_image, "Victoria41East.jpg"],
        [load_json, "vancouver.json"],
        [load_text, "vancouver.json"],
    ],
)
def test_file(
    test_object,
    func: Callable,
    filename: str,
):
    assert func(
        objects.path_of(
            object_name=test_object,
            filename=filename,
        )
    )

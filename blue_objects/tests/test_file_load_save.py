import pytest
from typing import Callable, Union, Tuple, List
import numpy as np

from blue_options import string

from blue_objects import file, objects, env
from blue_objects.file.load import (
    load_image,
    load_json,
    load_matrix,
    load_text,
)
from blue_objects.file.save import (
    save_image,
    save_json,
    save_matrix,
    save_text,
)
from blue_objects.tests.test_objects import test_object


@pytest.mark.parametrize(
    [
        "load_func",
        "filename",
        "save_func",
    ],
    [
        [
            load_image,
            "Victoria41East.jpg",
            save_image,
        ],
        [
            load_json,
            "vancouver.json",
            save_json,
        ],
        [
            load_text,
            "vancouver.json",
            save_text,
        ],
    ],
)
def test_file_load_save(
    test_object,
    load_func: Callable,
    filename: str,
    save_func: Union[Callable, None],
):
    success, thing = load_func(
        objects.path_of(
            object_name=test_object,
            filename=filename,
        )
    )
    assert success

    if not save_func is None:
        assert save_func(
            file.add_suffix(
                objects.path_of(
                    object_name=test_object,
                    filename=filename,
                ),
                string.random(),
            ),
            thing,
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    ["size", "dtype"],
    [
        [(10, 3), np.uint8],
        [(10, 3), np.float16],
        [(10, 20, 30), np.uint8],
        [(10, 30, 20), np.uint8],
        [(10, 30, 20), np.float32],
        [(10, 10, 10, 5), np.uint8],
    ],
)
def test_file_load_save_matrix(
    size: Tuple[int, ...],
    dtype: Union[np.dtype, type],
) -> None:
    object_name = objects.unique_object(test_file_load_save_matrix)

    test_matrix = (
        np.random.randint(0, 256, size=size, dtype=dtype)
        if dtype == np.uint8
        else np.array(np.random.random(size), dtype=dtype)
    )

    filename = objects.path_of("test.npy", object_name)

    assert save_matrix(filename, test_matrix)

    success, matrix_read = load_matrix(filename)
    assert success
    assert (matrix_read == test_matrix).all()
    assert matrix_read.dtype == dtype

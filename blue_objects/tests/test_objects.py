import pytest
from blue_objects import file, path, objects
from blue_objects.env import VANWATCH_TEST_OBJECT


@pytest.mark.parametrize(
    ["object_name"],
    [
        [VANWATCH_TEST_OBJECT],
    ],
)
def test_objects_download(object_name):
    assert objects.download(object_name)

    list_of_files = [
        file.name_and_extension(filename)
        for filename in objects.list_of_files(object_name=object_name)
    ]

    assert "vancouver.json" in list_of_files, objects.path_of(
        object_name=object_name,
        filename="vancouver.json",
    )

    assert file.exist(
        objects.path_of(
            object_name=object_name,
            filename="vancouver.json",
        )
    )


def test_object_path():
    object_name = objects.unique_object()
    object_path = objects.object_path(object_name, create=True)
    assert object_path
    assert path.exists(object_path)


def test_objects_unique_object():
    prefix = "prefix"
    object_name = objects.unique_object(prefix)
    assert object_name
    assert object_name.startswith(prefix)

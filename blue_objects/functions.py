import os

from blue_options import string

from blue_objects import file, path
from blue_objects.env import ABCLI_OBJECT_ROOT, abcli_object_name
from blue_objects.storage import instance as storage
from blue_objects.logger import logger


def list_of_files(
    object_name: str,
    cloud: bool = False,
    **kwargs,
):
    return (
        storage.list_of_objects(
            object_name,
            **kwargs,
        )
        if cloud
        else file.list_of(
            os.path.join(
                ABCLI_OBJECT_ROOT,
                object_name,
                "*",
            ),
            **kwargs,
        )
    )


def object_path(
    object_name=".",
    create=False,
):
    output = os.path.join(
        ABCLI_OBJECT_ROOT,
        abcli_object_name if object_name == "." else object_name,
    )

    if create:
        os.makedirs(output, exist_ok=True)

    return output


def path_of(
    filename,
    object_name=".",
    create=False,
):
    return os.path.join(
        object_path(object_name, create),
        filename,
    )


def signature(info=None, object_name="."):
    return [
        "{}{}".format(
            abcli_object_name if object_name == "." else object_name,
            "" if info is None else f"/{str(info)}",
        ),
        string.pretty_date(include_time=False),
        string.pretty_date(include_date=False, include_zone=True),
    ]


def unique_object(prefix=""):
    object_name = string.pretty_date(
        as_filename=True,
        unique=True,
    )
    if prefix:
        object_name = f"{prefix}-{object_name}"

    path.create(object_path(object_name))

    logger.info(f"📂 {object_name}")

    return object_name

from typing import Union
import os

from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)

HOME = os.getenv("HOME", "")

ABCLI_AWS_REGION = os.getenv(
    "ABCLI_AWS_REGION",
    "",
)

ABCLI_AWS_S3_BUCKET_NAME = os.getenv(
    "ABCLI_AWS_S3_BUCKET_NAME",
    "kamangir",
)

ABCLI_AWS_S3_PREFIX = os.getenv(
    "ABCLI_AWS_S3_PREFIX",
    "bolt",
)


ABCLI_OBJECT_PATH = os.getenv(
    "ABCLI_OBJECT_PATH",
    "",
)

ABCLI_PATH_STORAGE = os.getenv(
    "ABCLI_PATH_STORAGE",
    os.path.join(HOME, "storage"),
)

abcli_object_name = os.getenv(
    "abcli_object_name",
    "",
)


ABCLI_OBJECT_ROOT = os.getenv(
    "ABCLI_OBJECT_ROOT",
    os.path.join(ABCLI_PATH_STORAGE, "abcli"),
)

abcli_path_git = os.getenv(
    "abcli_path_git",
    os.path.join(HOME, "git"),
)


ABCLI_PATH_STATIC = os.getenv(
    "ABCLI_PATH_STATIC",
    "",
)


ABCLI_PUBLIC_PREFIX = os.getenv(
    "ABCLI_PUBLIC_PREFIX",
    "",
)

BLUE_OBJECTS_SECRET = os.getenv(
    "BLUE_OBJECTS_SECRET",
    "",
)

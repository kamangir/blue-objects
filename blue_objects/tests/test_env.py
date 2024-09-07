from abcli.tests import test_env
from blue_objects import env


def test_abcli_env():
    test_env.test_abcli_env()


def test_blue_objects_env():
    assert env.BLUE_OBJECTS_SECRET
    assert env.ABCLI_PUBLIC_PREFIX

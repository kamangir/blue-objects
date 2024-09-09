import os

from blueness import module
from blue_options.host.functions import (
    is_rpi,
    is_headless,
    is_mac,
    is_ec2,
    is_docker,
    is_github_workflow,
    is_jupyter,
    is_aws_batch,
)


from blue_objects import NAME
from blue_objects.host import shell
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


screen_width = None
screen_height = None

try:
    if is_rpi():
        if not is_headless():
            # https://stackoverflow.com/a/14124257
            screen = os.popen("xrandr -q -d :0").readlines()[0]
            screen_width = int(screen.split()[7])
            screen_height = int(screen.split()[9][:-1])
    elif is_mac():
        success, output = shell(
            "system_profiler SPDisplaysDataType |grep Resolution",
            clean_after=True,
            return_output=True,
        )
        output = [thing for thing in output if thing]
        if success and output:
            screen_width, screen_height = [
                int(thing) for thing in output[-1].split() if thing.isnumeric()
            ]

    elif (
        not is_ec2()
        and not is_docker()
        and not is_github_workflow()
        and not is_jupyter()
        and not is_aws_batch()
    ):
        from gi.repository import Gdk  # type: ignore

        screen = Gdk.Screen.get_default()
        geo = screen.get_monitor_geometry(screen.get_primary_monitor())
        screen_width = geo.width
        screen_height = geo.height
except Exception as e:
    logger.error(f"{NAME}: Failed: {e}.")

used_default = False
if screen_height is None or screen_width is None:
    used_default = True
    screen_height = 480
    screen_width = 640
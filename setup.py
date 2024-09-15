from blue_objects import NAME, VERSION, DESCRIPTION, REPO_NAME
from blueness.pypi import setup

setup(
    filename=__file__,
    repo_name=REPO_NAME,
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[
        NAME,
        f"{NAME}.cache",
        f"{NAME}.file",
        f"{NAME}.graphics",
        f"{NAME}.host",
        f"{NAME}.metadata",
        f"{NAME}.relations",
        f"{NAME}.storage",
        f"{NAME}.tags",
        f"{NAME}.tests",
    ],
    include_package_data=True,
    package_data={
        NAME: [
            "config.env",
            "sample.env",
            ".abcli/**/*.sh",
        ],
    },
)

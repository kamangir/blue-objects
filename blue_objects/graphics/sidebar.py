import cv2
import math
from typing import List
import numpy as np
from functools import reduce

from blueness import module
from blue_options import string

from blue_objects import NAME
from blue_objects.graphics.text import render_text
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


def add_sidebar(
    image: np.ndarray,
    lines: List[str],
    images: List[np.ndarray] = [],
    line_length: int = 28,
):
    logger.debug(
        "{}.add_sidebar({},{},{})".format(
            NAME,
            string.pretty_shape_of_matrix(image),
            "|".join(lines),
            len(images),
        )
    )

    if not image.shape or not lines:
        return image

    if line_length == -1:
        line_length = max([len(line) for line in lines])

    image_width = int(image.shape[1] / 7)

    sidebar = np.concatenate(
        [
            image_
            for _, image_ in sorted(
                zip(
                    lines,
                    [
                        render_text(
                            text=line.ljust(line_length),
                            color_depth=image.shape[2],
                            image_width=image_width,
                        )
                        for line in lines
                    ],
                )
            )
        ]
        + [
            cv2.resize(
                image_,
                (
                    image_width,
                    int(image_.shape[1] / image_.shape[0] * image_width),
                ),
            )
            for image_ in images
        ],
        axis=0,
    )

    if sidebar.shape[0] > image.shape[0]:
        sidebar = sidebar[: image.shape[0], :, :]
    elif sidebar.shape[0] < image.shape[0]:
        sidebar = np.concatenate(
            [
                np.zeros(
                    (
                        image.shape[0] - sidebar.shape[0],
                        sidebar.shape[1],
                        sidebar.shape[2],
                    ),
                    dtype=sidebar.dtype,
                ),
                sidebar,
            ],
            axis=0,
        )

    return np.concatenate([sidebar, image], axis=1)

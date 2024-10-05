import math
from typing import List
import numpy as np
from functools import reduce
import textwrap

from blueness import module

from blue_objects import NAME
from blue_objects.graphics.text import render_text

NAME = module.name(__file__, NAME)


def add_signature(
    image: np.ndarray,
    header: List[str],
    footer: List[str] = [],
    word_wrap: bool = True,
    line_width: int = 80,
) -> np.ndarray:
    if image is None or not image.shape:
        return image

    if word_wrap:
        justify_text = lambda text: reduce(
            lambda x, y: x + y,
            [textwrap.wrap(line, width=line_width) for line in text],
        )

        header = justify_text(header)
        footer = justify_text(footer)

    justify_line = lambda line: (
        line if len(line) >= line_width else line + (line_width - len(line)) * " "
    )

    return np.concatenate(
        [
            render_text(
                text=justify_line(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in header
        ]
        + [image]
        + [
            render_text(
                text=justify_line(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in footer
        ],
        axis=0,
    )

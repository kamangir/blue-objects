import numpy as np


def add_frame(
    image: np.ndarray,
    width: int,
) -> np.ndarray:
    output = np.zeros(
        (image.shape[0] + 2 * width, image.shape[1] + 2 * width, image.shape[2]),
        dtype=image.dtype,
    )

    output[width:-width, width:-width, :] = image[:, :, :]

    return output

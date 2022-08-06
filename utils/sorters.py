from pathlib import Path
from typing import List

from PIL import Image, ImageStat

from .data import exif_data


class OrderMethod:
    DATE = "date"
    COLOR = "color"


def sort_images(image_paths: List[Path], order_method: str):
    if order_method == OrderMethod.DATE:
        return date_sort(image_paths)
    elif order_method == OrderMethod.COLOR:
        return color_sort(image_paths)
    else:
        print("Not sorted.")


def date_sort(image_paths: List[Path]):
    image_dates = exif_data(image_paths, "datetime_original")
    if image_dates:
        return [
            image_data["path"]
            for image_data in sorted(image_dates, key=lambda x: x["datetime_original"], reverse=True)
        ]
    else:
        print(
            " * Couldn't sort images due to lack of *datetime_original* exif attribute."
        )
        return image_paths


def color_sort(image_paths: List[Path]):
    image_list = []
    for path in image_paths:
        H, _, _ = Image.open(path).convert("RGB").convert("HSV").split()
        image_list.append((path, ImageStat.Stat(H).mean))
    sorted_list = sorted(image_list, key=lambda x: x[1])
    return [image[0] for image in sorted_list]

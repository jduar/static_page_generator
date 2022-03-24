from pathlib import Path
from typing import List

from exif import Image


def exif_data(image_paths: List[Path], *args):
    images_data = []
    for path in image_paths:
        image_exif = {}
        image_exif["path"] = path
        with open(path, 'rb') as img_file:
            for arg in args:
                try:
                    image_exif[arg] = getattr(Image(img_file), arg)
                except (AttributeError, KeyError):
                    print(f" * This image doesn't have the exif info {arg}")
                    return
        images_data.append(image_exif)
    return images_data

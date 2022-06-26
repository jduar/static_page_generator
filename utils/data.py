from pathlib import Path
from typing import List

from exif import Image
from iptcinfo3 import IPTCInfo


def exif_data(image_paths: List[Path], *args):
    images_data = []
    for path in image_paths:
        image_exif = {}
        image_exif["path"] = path
        with open(path, "rb") as img_file:
            for arg in args:
                try:
                    image_exif[arg] = getattr(Image(img_file), arg)
                except (AttributeError, KeyError):
                    print(f" * This image doesn't have the exif info {arg}")
                    return
        images_data.append(image_exif)
    return images_data


def keywords_data(image_paths: List[Path]):
    return [image_keywords(path) for path in image_paths]


def image_keywords(path: Path):
    return {"path": path, "keywords": IPTCInfo(path).get("keywords", None)}

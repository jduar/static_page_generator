from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List

from exif import Image
from iptcinfo3 import IPTCInfo

import config

ImageData = namedtuple("ImageData", ["path", "keywords"])


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


def images_per_keyword(image_paths: List[Path]) -> Dict:
    keyword_images = defaultdict(list)
    for image in image_data(image_paths):
        for keyword in categories(image.keywords):
            keyword_images[keyword].append(image.path)
    return keyword_images


def categories(keywords: List[str]) -> List[str]:
    if not config.USE_CATEGORIES or not config.CATEGORIES:
        return keywords
    else:
        return [keyword for keyword in keywords if keyword in config.CATEGORIES]


def image_data(image_paths: List[Path]) -> List[ImageData]:
    return [
        ImageData(
            path, [keyword.decode("utf-8") for keyword in IPTCInfo(path)["keywords"]]
        )
        for path in image_paths
    ]

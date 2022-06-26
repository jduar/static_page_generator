from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List

from exif import Image
from iptcinfo3 import IPTCInfo

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


def image_by_keywords(image_paths: List[Path]) -> Dict:
    keywords_data = image_keywords(image_paths)
    keyword_images = defaultdict(list)
    for image_data in keywords_data:
        for keyword in image_data.keywords:
            keyword_images[keyword].append(image_data.path)
    return keyword_images


def image_keywords(image_paths: List[Path]) -> List[ImageData]:
    return [
        ImageData(
            path, [keyword.decode("utf-8") for keyword in IPTCInfo(path)["keywords"]]
        )
        for path in image_paths
    ]

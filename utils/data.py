import logging
from collections import OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from exif import Image
from iptcinfo3 import IPTCInfo
from PIL import Image as PILImage
from PIL import ImageOps

import settings

# Default logging level generates a bunch of IPTC warnings
iptcinfo_logger = logging.getLogger("iptcinfo")
iptcinfo_logger.setLevel(logging.ERROR)


class Photo:
    def __init__(self, path: Path):
        self.local_path = path  # local path
        self.path = Path("images") / path.name  # path inside container
        self.get_exif_data()
        self.get_image_size()

    def get_exif_data(self) -> None:
        image_data = Image(self.local_path)
        self.original_date = image_data.datetime_original
        self.aperture = image_data.get("aperture_value")
        self.focal_length = image_data.get("focal_length")
        self.keywords = [
            keyword.decode("utf-8") for keyword in IPTCInfo(self.local_path)["keywords"]
        ]
        self.orientation = image_data.get("orientation")

    def get_image_size(self) -> None:
        image = PILImage.open(self.local_path)
        # Some photos that had been exported straight from camera contained the orientation as
        # an exif tag and needed being transposed to appear correctly
        if self.orientation:
            image = ImageOps.exif_transpose(image)
        self.width, self.height = image.size

    def get_original_date(self) -> str:
        return datetime.strptime(self.original_date, "%Y:%m:%d %H:%M:%S").strftime(
            "%A, %b %d, %Y"
        )
        # 2021:10:14 21:44:43
        # Sunday, Jun 26, 2022

    def get_aperture(self) -> str:
        return f"f/{int(self.aperture)}"

    def get_focal_length(self) -> str:
        return f"{int(self.focal_length)} mm"

    def get_keywords(self) -> str:
        return ", ".join(self.keywords)


def photos_per_keyword(photos: List[Photo]) -> Dict[str, List[Photo]]:
    keyword_photos = defaultdict(list)
    for photo in photos:
        for keyword in categories(photo.keywords):
            keyword_photos[keyword].append(photo)
    return OrderedDict(sorted(keyword_photos.items()))


def categories(keywords: List[str]) -> List[str]:
    if not settings.USE_CATEGORIES or not settings.CATEGORIES:
        return keywords
    else:
        return [keyword for keyword in keywords if keyword in settings.CATEGORIES]

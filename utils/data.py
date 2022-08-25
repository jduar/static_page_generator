from collections import defaultdict
from typing import Dict, List

import settings
from exif import Image
from iptcinfo3 import IPTCInfo


class Photo:
    def __init__(self, path):
        self.path = path
        self.get_exif_data()

    def get_exif_data(self):
        image_data = Image(self.path)
        self.original_date = image_data.datetime_original
        self.aperture = image_data.get("aperture_value")
        self.focal_length = image_data.get("focal_length")
        self.keywords = [
            keyword.decode("utf-8") for keyword in IPTCInfo(self.path)["keywords"]
        ]


def photos_per_keyword(photos: List[Photo]) -> Dict:
    keyword_photos = defaultdict(list)
    for photo in photos:
        for keyword in categories(photo.keywords):
            keyword_photos[keyword].append(photo)
    return keyword_photos


def categories(keywords: List[str]) -> List[str]:
    if not settings.USE_CATEGORIES or not settings.CATEGORIES:
        return keywords
    else:
        return [keyword for keyword in keywords if keyword in settings.CATEGORIES]

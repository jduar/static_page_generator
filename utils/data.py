import logging
from collections import OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path

from exif import Image
from iptcinfo3 import IPTCInfo
from PIL import Image as PILImage
from yoga import image

import settings

# Default logging level generates a bunch of IPTC warnings
iptcinfo_logger = logging.getLogger("iptcinfo")
iptcinfo_logger.setLevel(logging.ERROR)

THUMBNAILS_DIRECTORY = "thumbnails"


class Photo:
    def __init__(self, path: Path):
        self.local_path = path  # local path
        self.path = Path("images") / path.name  # path inside container
        self.get_exif_data()
        self.get_image_size()
        self.thumbnail = (
            get_image_thumbnail(self.local_path)
            if Path.is_file(get_image_thumbnail(self.local_path))
            else None
        )

    def get_exif_data(self) -> None:
        image_data = Image(self.local_path)
        self.original_date = image_data.datetime_original
        self.aperture = image_data.get("aperture_value")
        self.focal_length = image_data.get("focal_length")
        self.title = image_data.get("title")
        self.keywords = [
            keyword.decode("utf-8") for keyword in IPTCInfo(self.local_path)["keywords"]
        ]

    def get_image_size(self) -> None:
        image = PILImage.open(self.local_path)
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


def get_image_thumbnail(local_path: Path) -> Path:
    """Returns Path for the image thumbnails, whether it exists or not."""
    return Path(THUMBNAILS_DIRECTORY) / f"{local_path.stem}_thumbnail{local_path.suffix}"


def optimize_images(images: list[Path], force: bool = False) -> None:
    print(" * Generating thumbnails...")
    for image_path in images:
        if Path.is_file(get_image_thumbnail(image_path)):
            return
        optimize_image(image_path)


def optimize_image(image_path: Path) -> None:
    print(f"   * Generating thumbnail for image {image.local_path.stem} ...")
    image.optimize(
        str(image_path),
        str(get_image_thumbnail(image_path)),
        options={
            "output_format": "orig",
            "resize": [512, 512],
            "jpeg_quality": 0.9,
        },
    )


def photos_per_keyword(photos: list[Photo]) -> dict[str, list[Photo]]:
    keyword_photos = defaultdict(list)
    for photo in photos:
        for keyword in categories(photo.keywords):
            keyword_photos[keyword].append(photo)
    return OrderedDict(sorted(keyword_photos.items()))


def categories(keywords: list[str]) -> list[str]:
    if not settings.USE_CATEGORIES or not settings.CATEGORIES:
        return keywords
    else:
        return [keyword for keyword in keywords if keyword in settings.CATEGORIES]

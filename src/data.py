import logging
from datetime import datetime
from pathlib import Path
from typing import Set

from exif import Image
from iptcinfo3 import IPTCInfo
from PIL import Image as PILImage
from yoga import image

import settings

# Default logging level generates a bunch of IPTC warnings
iptcinfo_logger = logging.getLogger("iptcinfo")
iptcinfo_logger.setLevel(logging.ERROR)

THUMBNAILS_PATH = Path("data/thumbnails")


class Photo:
    def __init__(self, path: Path, tag_organizer):
        self.tags: Set[str] = set()

        self.local_path = path  # local path
        self.path = Path("images") / path.name  # path inside container

        # get and set image data
        self.get_exif_data()
        self.get_tags(tag_organizer)
        self.get_image_size()
        self.thumbnail = (
            Path("thumbnails") / get_thumbnail_name(path)
            if Path.is_file(get_image_thumbnail(self.local_path))
            else None
        )

    def get_exif_data(self) -> None:
        image_data = Image(self.local_path)
        self.original_date = image_data.datetime_original
        self.aperture = image_data.get("aperture_value")
        self.focal_length = image_data.get("focal_length")
        self.description = image_data.get("image_description", "")

    def get_tags(self, tag_organizer) -> None:
        for keyword in IPTCInfo(self.local_path)["keywords"]:
            decoded_keyword = keyword.decode("utf-8")
            tag_organizer.create_or_update_tag(decoded_keyword, self)
            self.tags.add(decoded_keyword)

    def get_image_size(self) -> None:
        image = PILImage.open(self.local_path)
        self.width, self.height = image.size

    def get_original_date(self) -> str:
        return datetime.strptime(self.original_date, "%Y:%m:%d %H:%M:%S").strftime("%A, %b %d, %Y")
        # 2021:10:14 21:44:43
        # Sunday, Jun 26, 2022

    @property
    def render_aperture(self) -> str:
        return f"f/{int(self.aperture)}"

    @property
    def render_focal_length(self) -> str:
        return f"{int(self.focal_length)} mm"

    @property
    def render_keywords(self) -> str:
        return ", ".join(self.tags)


class TagOrganizer:
    def __init__(self):
        self.tags = {}

    def create_or_update_tag(self, keyword: str, photo: Photo):
        if keyword not in self.tags:
            self.tags[keyword] = Tag(keyword)
        self.tags[keyword].photos.add(photo)

    def get_render_tags(self) -> list[str]:
        if settings.TAGS_WHITELIST:
            whitelisted_tags = [tag for tag in settings.TAGS_WHITELIST if self.tags[tag]]
            if not settings.TAG_CUSTOM_ORDER:
                whitelisted_tags = sorted(whitelisted_tags)
            return whitelisted_tags
        return sorted([tag for tag in self.tags if tag not in settings.TAGS_BLACKLIST])


class Tag:
    def __init__(self, name: str):
        self.name = name
        self.photos: Set[Photo] = set()


def get_image_thumbnail(local_path: Path) -> Path:
    """Returns Path for the image thumbnails, whether it exists or not."""
    return THUMBNAILS_PATH / get_thumbnail_name(local_path)


def get_thumbnail_name(image_path: Path) -> str:
    return f"{image_path.stem}_thumbnail{image_path.suffix}"


def optimize_images(images: list[Path], force: bool = False) -> None:
    print(" * Generating thumbnails...")
    THUMBNAILS_PATH.mkdir(exist_ok=True, parents=True)
    for image_path in images:
        if not Path.is_file(get_image_thumbnail(image_path)) or force:
            optimize_image(image_path)


def optimize_image(image_path: Path) -> None:
    print(f"   * Generating thumbnail for image {image_path.stem} ...")
    image.optimize(
        str(image_path),
        str(get_image_thumbnail(image_path)),
        options={"output_format": "orig", "resize": [896, 896], "jpeg_quality": 0.9},
    )

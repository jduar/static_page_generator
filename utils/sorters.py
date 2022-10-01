from typing import List

from PIL import Image, ImageStat

from .data import Photo


class OrderMethod:
    DATE = "date"
    COLOR = "color"


def sort_photos(photos: List[Photo], order_method: str):
    sorting_map = {"date": date_sort,
                   "color": color_sort,
                   }
    try:
        return sorting_map[order_method](photos)

    except KeyError:
        print("Can't recognize sorting option, skipping it!")


def date_sort(photos: List[Photo]) -> List[Photo]:
    return sorted(photos, key=lambda x: x.original_date, reverse=True)


def color_sort(photos: List[Photo]) -> List[Photo]:
    photo_list = []
    for photo in photos:
        H, _, _ = Image.open(photo.path).convert("RGB").convert("HSV").split()
        photo_list.append((photo.path, ImageStat.Stat(H).mean))
    sorted_list = sorted(photo_list, key=lambda x: x[1])
    return [image[0] for image in sorted_list]

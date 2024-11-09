from PIL import Image, ImageStat

from data import Photo


class OrderMethod:
    DATE = "date"
    COLOR = "color"


def sort_photos(
    photos: list[Photo], order_method: str, reverse_order: bool = True
) -> list[Photo] | None:
    sorting_map = {
        "date": date_sort,
        "color": color_sort,
    }
    try:
        return sorting_map[order_method](photos, reverse_order)

    except KeyError:
        print("Can't recognize sorting option, skipping it!")


def date_sort(photos: list[Photo], reverse_order: bool) -> list[Photo]:
    return sorted(photos, key=lambda x: x.original_date, reverse=reverse_order)


def color_sort(photos: list[Photo], reverse_order: bool) -> list[Photo]:
    photo_list = []
    for photo in photos:
        H, _, _ = Image.open(photo.path).convert("RGB").convert("HSV").split()
        photo_list.append((photo, ImageStat.Stat(H).mean))
    sorted_list = sorted(photo_list, key=lambda x: x[1], reverse=reverse_order)
    return [image[0] for image in sorted_list]

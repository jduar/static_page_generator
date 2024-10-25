#!/usr/bin/env python3

import argparse
import shutil
from os import getenv
from pathlib import Path
from typing import Set

import markdown
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

import settings
from utils.data import Photo, TagOrganizer, optimize_images
from utils.sorters import OrderMethod, sort_photos

DESTINATION_DIR = "public"
IMAGES_PATH = Path("data/images")
PAGES_PATH = Path("data/pages")
FAVICON_PATH = Path("data/favicon.svg")


class SiteGenerator:
    def __init__(self):
        self.photos: Set[Photo] = set()
        self.tag_organizer = TagOrganizer()

        self.gather_photos()

        self.env = Environment(loader=FileSystemLoader("template"))

        self.site_title = settings.TITLE
        self.description = settings.DESCRIPTION
        self.text_paths = self.text_paths()
        self.text_page_names = [path.stem for path in self.text_paths if path.stem != "index"]

        self.render_content()
        self.cleanup()
        self.copy_content()
        print(" * Successfully generated site.")

    def cleanup(self) -> None:
        public = Path(DESTINATION_DIR)
        public.mkdir(parents=True, exist_ok=True)
        for path in public.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    def copy_content(self) -> None:
        dest_dir = Path(DESTINATION_DIR)
        shutil.copytree("template/css", dest_dir / "css")
        shutil.copytree("template/js", dest_dir / "js")
        shutil.copy(FAVICON_PATH, dest_dir / "favicon.svg")
        for path in Path(".src/public").iterdir():  # Deleting the dir itself causes issues with docker
            shutil.copy(path, Path(DESTINATION_DIR))

    def render_page(self, title: str, content: str) -> None:
        template = self.env.get_template("main_layout.html")

        link = f"{DESTINATION_DIR}/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(Path(".src") / link, "w+") as file:
            html = template.render(
                text_pages=self.text_page_names,
                photo_pages=self.tag_organizer.get_render_tags(),
                page=page,
                site_title=self.site_title,
                description=self.description,
            )
            file.write(html)

    def render_gallery(self, photos: list[Photo], sorting: str = None) -> None:
        if sorting:
            photos = sort_photos(photos, sorting)
        photo_context = []
        for photo in photos:
            self.render_photo_page(photo)
            photo_context.append(
                {
                    "photo": photo.path,
                    "thumbnail": photo.thumbnail if photo.thumbnail else photo.path,
                    "page": f"{photo.path.stem}.html",
                    "width": photo.width,
                    "height": photo.height,
                    "alt": photo.description,
                }
            )
        template = self.env.get_template("gallery.html")
        return template.render(photos=photo_context)

    def render_photo_page(self, photo: Photo) -> None:
        template = self.env.get_template("photo.html")
        with open(Path(".src/public") / f"{photo.path.stem}.html", "w+") as file:
            html = template.render(photo=photo)
            file.write(html)

    def render_content(self) -> None:
        generation_dir = Path(".src/public")
        generation_dir.mkdir(exist_ok=True, parents=True)
        for path in generation_dir.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

        self.render_page(
            title="index",
            content=self.render_gallery(self.photos, sorting=OrderMethod.DATE),
        )
        for path in self.text_paths:
            if path.stem == "index":
                continue
            else:
                with open(path, "r") as file:
                    content = file.read()
                html_content = markdown.markdown(content, output_format="html5")
                self.render_page(path.stem, html_content)

        for tag in self.tag_organizer.tags:
            self.render_page(
                title=tag,
                content=self.render_gallery(self.tag_organizer.tags[tag].photos, sorting=OrderMethod.DATE),
            )

    def text_paths(self) -> list[Path]:
        """Returns list of text page paths."""
        return list(PAGES_PATH.iterdir())

    def gather_photos(self):
        for image in IMAGES_PATH.iterdir():
            photo = Photo(image, tag_organizer=self.tag_organizer)
            self.photos.add(photo)


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    thumbnails = parser.add_argument_group("thumbnail generation")
    thumbnails.add_argument(
        "--generate-thumbnails",
        action="store_true",
        help="generate smaller image thumbnails for gallery - might take a while depending on the number of images",
    )
    thumbnails.add_argument(
        "--force",
        action="store_true",
        help="force regeneration of already existing thumbnails",
    )
    # TODO: Add future verbose functionality to prints.
    parser.add_argument("-v", "--verbose", action="store_true", help="currently does nothing")

    args = parser.parse_args()
    if args.generate_thumbnails:
        optimize_images(
            [image for image in Path(getenv("PICTURES_FOLDER")).iterdir()],
            force=args.force,
        )
    else:
        SiteGenerator()

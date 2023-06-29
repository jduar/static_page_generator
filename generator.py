#!/usr/bin/env python3

import argparse
import shutil
from os import getenv
from pathlib import Path

import markdown
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

import settings
from utils.data import Photo, optimize_images, photos_per_keyword
from utils.sorters import OrderMethod, sort_photos

DESTINATION_DIR = "public"


class SiteGenerator:
    def __init__(self):
        self.image_path = Path(getenv("PICTURES_FOLDER"))
        self.pages_path = Path(getenv("PAGES_FOLDER"))
        self.icon_path = Path(getenv("FAVICON"))
        self.env = Environment(loader=FileSystemLoader("template"))
        self.photos = self.gather_photos(self.image_path)
        self.photo_sections = photos_per_keyword(self.photos)
        self.site_title = settings.TITLE
        self.description = settings.DESCRIPTION
        self.text_paths = self.text_paths()
        self.text_page_names = [
            path.stem for path in self.text_paths if path.stem != "index"
        ]

        self.render_content()
        self.cleanup()
        self.copy_content()
        print(" * Successfully generated site.")

    def cleanup(self) -> None:
        public = Path(DESTINATION_DIR)
        for path in public.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    def copy_content(self) -> None:
        dest_dir = Path(DESTINATION_DIR)
        shutil.copytree("template/css", dest_dir / "css")
        shutil.copytree("template/js", dest_dir / "js")
        shutil.copy(self.icon_path, dest_dir / "favicon.svg")
        for path in Path(".src/public").iterdir():  # Deleting the dir itself causes issues with docker
            shutil.copy(path, Path(DESTINATION_DIR))

    def render_page(self, title: str, content: str) -> None:
        template = self.env.get_template("main_layout.html")

        link = f"{DESTINATION_DIR}/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(Path(".src") / link, "w+") as file:
            html = template.render(
                text_pages=self.text_page_names,
                photo_pages=self.photo_sections.keys(),
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

        for section in self.photo_sections:
            self.render_page(
                section,
                self.render_gallery(
                    self.photo_sections[section], sorting=OrderMethod.DATE
                ),
            )

    def text_paths(self) -> list[Path]:
        """Returns list of text page paths."""
        return list(self.pages_path.iterdir())

    def gather_photos(self, path: Path) -> list[Photo]:
        return [Photo(image) for image in path.iterdir()]

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-thumbnails", action="store_true")
    parser.add_argument("--force", action="store_true")
    # TODO: Add future verbose functionality to prints.
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.generate_thumbnails:
        optimize_images([image for image in Path(getenv("PICTURES_FOLDER")).iterdir()], force=args.force)
    else:
        SiteGenerator()

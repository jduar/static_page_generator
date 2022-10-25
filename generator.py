#!/usr/bin/env python3

import shutil
from pathlib import Path
from typing import List

import markdown
from jinja2 import Environment, FileSystemLoader

from utils.data import Photo, photos_per_keyword
from utils.sorters import OrderMethod, sort_photos

# FIXME: DEFAULT_IMAGE_PATH will currently break if changed. Fix this somehow.
DEFAULT_IMAGE_PATH = Path("images/pictures")  # path for directory containing images
DEFAULT_PAGES_PATH = Path("pages")  # path for directory containing the pages


class SiteGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("template"))
        self.cleanup()
        self.copy_static()

        self.photos = self.gather_photos(DEFAULT_IMAGE_PATH)
        self.photo_sections = photos_per_keyword(self.photos)

        self.text_paths = self.text_paths()
        self.text_page_names = [
            path.stem for path in self.text_paths if path.stem != "index"
        ]
        self.render_content()
        print(" * Successfully generated site.")

    def cleanup(self):
        public = Path("public")
        public.mkdir(exist_ok=True, parents=True)
        for path in public.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    def copy_static(self):
        shutil.copytree("template/static", "public/static")

    def render_page(self, title: str, content: str):
        template = self.env.get_template("main_layout.html")

        link = f"public/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(link, "w+") as file:
            html = template.render(
                text_pages=self.text_page_names,
                photo_pages=self.photo_sections.keys(),
                page=page,
            )
            file.write(html)

    def render_gallery(self, photos: List[Photo], sorting: str = None):
        if sorting:
            photos = sort_photos(photos, sorting)
        photo_context = []
        for photo in photos:
            self.render_photo_page(photo)
            photo_context.append(
                {"photo": photo.path, "page": f"{photo.path.stem}.html"}
            )
        template = self.env.get_template("gallery.html")
        return template.render(photos=photo_context)

    def render_photo_page(self, photo: Photo):
        template = self.env.get_template("photo.html")
        with open(f"public/{photo.path.stem}.html", "w+") as file:
            html = template.render(photo=photo)
            file.write(html)

    def render_content(self):
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
            self.render_page(section, self.render_gallery(self.photo_sections[section]))

    def text_paths(self) -> List[Path]:
        """Returns list of text page paths."""
        return list(DEFAULT_PAGES_PATH.iterdir())

    def gather_photos(self, path: Path) -> List[Photo]:
        return [Photo(image) for image in path.iterdir()]


if __name__ == "__main__":
    SiteGenerator()

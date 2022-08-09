#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import Dict, List

import markdown
from jinja2 import Environment, FileSystemLoader

from utils.data import images_per_keyword
from utils.sorters import OrderMethod, sort_images

DEFAULT_IMAGE_PATH = "images/pictures"


class SiteGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("template"))
        self.cleanup()
        self.copy_static()
        self.image_paths = [
            Path(DEFAULT_IMAGE_PATH, image) for image in os.listdir(DEFAULT_IMAGE_PATH)
        ]
        self.text_paths = self.text_paths()
        self.text_page_names = [path.stem for path in self.text_paths if path.stem != "index"]
        self.image_sections = images_per_keyword(self.image_paths)
        self.render_content()
        print(" * Successfully generated site.")

    def cleanup(self):
        public = Path("public")
        if public.is_dir():
            for path in public.glob("*"):
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        else:
            os.mkdir("./public")

    def copy_static(self):
        shutil.copytree("template/static", "public/static")

    def render_page(self, title: str, content: str):
        template = self.env.get_template("main_layout.html")

        link = f"public/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(link, "w+") as file:
            html = template.render(
                text_pages=self.text_page_names, image_pages=self.image_sections.keys(), page=page
            )
            file.write(html)

    def render_gallery(self, image_paths: List[str], sorting: str = None):
        if sorting:
            image_paths = sort_images(image_paths, sorting)
        # TODO: For each photo, render a photo page with the photo and details.
        template = self.env.get_template("gallery.html")
        return template.render(images=image_paths)

    def render_image_page(self):
        pass

    def render_content(self):
        for path in self.text_paths:
            if path.stem == "index":
                self.render_page(title="index", content=self.render_gallery(self.image_paths, sorting=OrderMethod.DATE))
            else:
                with open(path, "r") as file:
                    content = file.read()
                html_content = markdown.markdown(content, output_format="html5")
                self.render_page(path.stem, html_content)

        for section in self.image_sections:
            self.render_page(section, self.render_gallery(self.image_sections[section]))

    def text_paths(self) -> List[Path]:
        """Returns list of text page paths."""
        return [Path("pages") / path for path in next(os.walk("pages"))[2]]


if __name__ == "__main__":
    SiteGenerator()

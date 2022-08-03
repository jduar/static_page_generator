#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import Dict, List

import markdown
from jinja2 import Environment, FileSystemLoader
from utils.sorters import sort_images, OrderMethod
from utils.data import images_per_keyword


DEFAULT_IMAGE_PATH = "images/pictures"


class SiteGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("template"))
        self.cleanup()
        self.copy_static()
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

    def render_page(
        self, title: str, content: str, text_pages: List[Dict], image_pages: List[Dict]
    ):
        template = self.env.get_template("_layout.html")

        link = f"public/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(link, "w+") as file:
            html = template.render(
                text_pages=text_pages, image_pages=image_pages, page=page
            )
            file.write(html)

    def render_images(self, image_paths: List[str], sorting: str = None):
        if sorting:
            image_paths = sort_images(image_paths, sorting)
        template = self.env.get_template("images.html")
        return template.render(images=image_paths)

    def render_content(self):
        image_paths = [
            Path(DEFAULT_IMAGE_PATH, image) for image in os.listdir(DEFAULT_IMAGE_PATH)
        ]
        image_sections = images_per_keyword(image_paths)
        text_paths = self.text_paths()

        text_page_names = [path.stem for path in text_paths if path.stem != "index"]
        image_page_names = image_sections.keys()

        for path in text_paths:
            if path.stem == "index":
                self.render_page(
                    title="index",
                    content=self.render_images(image_paths, sorting=OrderMethod.DATE),
                    text_pages=text_page_names,
                    image_pages=image_page_names,
                )
            else:
                with open(path, "r") as file:
                    content = file.read()
                html_content = markdown.markdown(content, output_format="html5")
                self.render_page(
                    path.stem, html_content, text_page_names, image_page_names
                )

        for section in image_sections:
            self.render_page(
                section,
                self.render_images(image_sections[section]),
                text_page_names,
                image_page_names,
            )

    def text_paths(self) -> List[Path]:
        """Returns list of text page paths."""
        return [Path("pages") / path for path in next(os.walk("pages"))[2]]


if __name__ == "__main__":
    SiteGenerator()

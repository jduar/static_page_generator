#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import Dict, List

import markdown
from jinja2 import Environment, FileSystemLoader


class SiteGenerator():
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("template"))
        self.cleanup()
        self.copy_static()
        self.render_content()
        print(" * Successfully generated site.")

    def cleanup(self):
        shutil.rmtree("./public")
        os.mkdir("./public")

    def copy_static(self):
        shutil.copytree("template/static", "public/static")

    def render_page(self, page_title: str, page_content: str, pages: List[Dict]):
        template = self.env.get_template("_layout.html")

        page_link = f"public/{page_title}.html"
        page_content = {"title": page_title, "link": page_link, "text": page_content}

        with open(page_link, "w+") as file:
            html = template.render(pages=pages, page_content=page_content)
            file.write(html)

    def render_content(self):
        pagepaths: List[Path] = [Path("pages") / path for path in os.listdir("pages")]

        pages = [path.stem for path in pagepaths if path.stem != "index"]

        for path in pagepaths:
            with open(path, "r") as file:
                content = file.read()
            html_content = markdown.markdown(content, output_format="html5")
            self.render_page(path.stem, html_content, pages)


if __name__ == "__main__":
    SiteGenerator()

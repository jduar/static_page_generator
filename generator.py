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

    def render_page(self, title: str, content: str, pages: List[Dict], images: bool = False):
        template = self.env.get_template("_layout.html")

        link = f"public/{title}.html"
        page = {"title": title, "link": link, "content": content}

        with open(link, "w+") as file:
            html = template.render(pages=pages, page=page)
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

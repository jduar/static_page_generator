import shutil
from pathlib import Path
from typing import Iterable, Set

import markdown
from jinja2 import Environment, FileSystemLoader, Template

import settings
from data import Photo, TagOrganizer
from utils.sorters import OrderMethod, sort_photos

DESTINATION_DIR = "public"
IMAGES_PATH = Path("data/images")
PAGES_PATH = Path("data/pages")
FAVICON_PATH = Path("data/favicon.svg")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}


class SiteGenerator:
    def __init__(self):
        self.photos: Set[Photo] = set()
        self.tag_organizer = TagOrganizer()

        self.gather_photos()

        self.jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=True)

        self.text_paths = [page for page in PAGES_PATH.iterdir() if page.suffix.lower() == ".md"]
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
        shutil.copytree("static/css", dest_dir / "css")
        shutil.copytree("static/js", dest_dir / "js")
        shutil.copy(FAVICON_PATH, dest_dir / "favicon.svg")
        for path in Path(".src/public").iterdir():  # Deleting the dir itself causes issues with docker
            shutil.copy(path, Path(DESTINATION_DIR))

    def render_page(self, title: str, template_name: str, context: dict = {}) -> None:
        template: Template = self.jinja_env.get_template(template_name)

        with open(Path(".src") / f"{DESTINATION_DIR}/{title}.html", "w+") as file:
            html = template.render(
                text_pages=self.text_page_names,
                photo_sections=self.tag_organizer.get_render_tags(),
                # TODO: Order tags alphabetically
                photo_tags=self.tag_organizer.tags,
                site_title=settings.TITLE,
                description=settings.DESCRIPTION,
                show_tags_page=self.show_tags_page,
                **context,
            )
            file.write(html)

    def render_gallery(self, title: str, photos: Iterable[Photo], sorting: str | None = None) -> None:
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
        self.render_page(title, "gallery.html", {"photos": photo_context})

    def render_photo_page(self, photo: Photo) -> None:
        template = self.jinja_env.get_template("photo.html")
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

        self.render_gallery("index", self.photos, sorting=OrderMethod.DATE)
        for path in self.text_paths:
            if path.stem == "index":
                continue
            else:
                with open(path, "r") as file:
                    content = file.read()
                html_content = markdown.markdown(content, output_format="html")
                self.render_page(path.stem, "main_layout.html", {"content": html_content})

        for tag in self.tag_organizer.tags:
            self.render_gallery(tag, self.tag_organizer.tags[tag].photos, sorting=OrderMethod.DATE)

        if self.show_tags_page:
            self.render_page("tags", "tags_page.html")

    def gather_photos(self):
        for image in IMAGES_PATH.iterdir():
            if image.suffix.lower() in IMAGE_EXTENSIONS:
                photo = Photo(image, tag_organizer=self.tag_organizer)
                self.photos.add(photo)

    @property
    def show_tags_page(self) -> bool:
        return bool(settings.TAGS_WHITELIST or settings.TAGS_BLACKLIST)

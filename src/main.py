#!/usr/bin/env python3

import argparse

from dotenv import load_dotenv

from data import optimize_images
from generator import IMAGE_EXTENSIONS, IMAGES_PATH, SiteGenerator

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    thumbnails = parser.add_argument_group("thumbnail generation")
    thumbnails.add_argument(
        "--generate-thumbnails",
        action="store_true",
        help="generate smaller image thumbnails for gallery - might take a while depending on the number of images",
    )
    thumbnails.add_argument("--force", action="store_true", help="force regeneration of already existing thumbnails")
    # TODO: Add future verbose functionality to prints.
    parser.add_argument("-v", "--verbose", action="store_true", help="currently does nothing")

    args = parser.parse_args()
    if args.generate_thumbnails:
        optimize_images(
            [image for image in IMAGES_PATH.iterdir() if image.suffix.lower() in IMAGE_EXTENSIONS], force=args.force
        )
    else:
        SiteGenerator()

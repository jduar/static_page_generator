# static_page_generator

A static photo gallery generator for photographers. See it live at [jduarte.eu](https://jduarte.eu).

## Running

> [!WARNING]
> This is meant to be used with actual photo files that contain camera metadata - probably won't work well with random images.

Dump your favourite photos in `data/images/`. Add markdown files to `data/pages/` and those files are turned into sections in your gallery.

If you're unsure how these translate into the website layout, you can find example content in `example_content/`. Copy it with

```bash
$ cp example_content/* data/
```

Then run the server with

```bash
$ make run
```

Your gallery is now available at http://localhost:8080.

You can then replace the content over at `data` with your own.

Other commands that might come in handy:

```bash
$ make generate  # fully regenerates the website structure
$ make thumbnails  # generates thumbnails (smaller sized versions of your photos that show up on the index)
```

## Development

For development, you're going to need to install [uv](https://docs.astral.sh/uv/). Once you have that, install the virtual environment with

```bash
$ uv sync
```

Then running this for development should be as simple as

```bash
$ make dev
```

This regenerates the website structure whenever you tweak a template or style and serves it as you go.

Use

```bash
$ uv run python src/main.py -h
```

to see available commands.

## How it works

The generator has two generating behaviours: text pages and image galleries.

Text pages are HTML pages converted from Markdown documents. These should be stored inside the `data/pages` directory. See the `about.md` document for an example.

Photo galleries are generated from photos containing keyword data and camera metadata (shutter speed, aperture, etc). A section is generated for every keyword containing the pictures with that keyword. Your photos should be stored inside the `data/images` directory.

## History

This project started out with the intention of creating a simple website. Most of the tools I work with are overkill for a static website and I didn't feel like hand writing and copying HTML code a bunch of times.

I could have learned how to use one of the many available static website generating tools, but I felt like the concept itself seemed simple enough that I might as well do it myself.

Eventually, I forgot what I wanted to create a website for in the first place, so the project started leaning towards becoming more of a photo gallery generator out of necessity. *It is what it is.*

# static_page_generator

A static photo gallery generator for photographers. See it live at [jduarte.eu](https://jduarte.eu).

## How to

Run for the first time with

```
$ make first-run
```

This will spin up a basic page using example content at http://localhost:8080.

You can then replace the content over at `data` with your own (following the existent folder structure) and re-run with

```
$ make run
```

Running this for development should be as simple as

```
$ make dev
```

This regenerates the website structure whenever you tweak a template or style and serves it as you go.

## How it works

The generator currently has two generating behaviours: text pages and image galleries.

Text pages are HTML pages converted from Markdown documents. These should be stored inside the `data/pages` directory. See the `about.md` document for an example.

Photo galleries are generated from photos containing keyword data and camera metadata (shutter speed, aperture, etc). A section is generated for every keyword containing the pictures with that keyword. Your photos should be stored inside the `data/images` directory.

## History

This project started out with the intention of creating a simple website. Most of the tools I work with are overkill for a static website and I didn't feel like hand writing and copying HTML code a bunch of times.

I could have learned how to use one of the many available static website generating tools, but I felt like the concept itself seemed simple enough that I might as well do it myself.

Eventually, I forgot what I wanted to create a website for in the first place, so the project started leaning towards becoming more of a photo gallery generator out of necessity. *It is what it is.*
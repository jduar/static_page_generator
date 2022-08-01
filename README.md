# static_page_generator

This is a static page generator.

I initially only wanted to create a simple website. Most of the tools I work with are overkill for a static website and I didn't feel like hand writing and copying HTML code a bunch of times.

I could technically learn how to use one of the many available static website generating tools, but I felt like the concept itself seemed simple enough that I might aswell do it myself.

So here it is. By this point, I can't even remember exactly what I wanted to create a website for, but whatever it might be, this tool aims to help me do that.

[UPDATE AUGUST 2022]

By this point, this is less of a generic static page generator and more of static picture gallery website generator. It is what it is.

## Functionality

At this stage, the script has two generating behaviours for pages focused on text and pages which act as image galleries.

In order to have text sections, create a `pages` directory at the root directory. Any markdown document palced inside will be converted to HTML and its name will be used as a section name.

In order to have image gallery sections, create a `images` directory at the root directory. Any directory inside it with groups of images will be rendered into a section with an image gallery.

There is a base layout template and CSS styling inside `template`.

An example of the current result of this script can be found at www.jduarte.xyz.

I might make all of this structure less "mandatory" in the future. It could maybe just ask you on a first run: "Point me to your pages directory and your image directory" and use those.

We'll see.

You also currently need a `index.md` page aswell. That should probably be changed aswell.

Running the docker container than sets up an nginx server with the pages you've just generated.

## Development

If you want to try this, I recommend setting up a virtual environment. For example:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

And then running the `generator.py` script.

Eventually, I want this all to be done automatically when running the Docker container.

You can then run the container with:

```
$ docker-compose up --build
```

Et voilà!

You should be able to access your new ~~empire~~ website at localhost:80.

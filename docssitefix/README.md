# web

Web server setup to render the documentation.

## How it works

The goal of this is to take the documentation and convert it from Markup to HTML. A small web server can then just host the converted HTML files. The idea is that each part can be run and changed independantly with little trouble. Because of how simple this is (it just converts all `.md` files it finds into `.html`) this can actually be used for multiple different repositories.

One of the best ways to use this, is to add the script to cron and convert the files every few minutes.

### Header

The `header.html` file will be written to the beginning of each of the converted files.

### Footer

The `footer.html` file will be written to the end of each of the converted files.

### CSS

The `style.css` file will be copied to the base of the new directory.

## Requirments

The following software is required to make this work:

- [cmark](https://github.com/commonmark/cmark)
- [git](https://github.com/git/git)


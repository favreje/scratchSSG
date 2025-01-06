import utils


def main():
    utils.copy_content("static", "public")
    source = "content/index.md"
    template = "template.html"
    destination = "public/index.html"
    utils.generate_page(source, template, destination)


if __name__ == "__main__":
    main()

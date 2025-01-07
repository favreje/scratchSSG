import utils


def main():
    utils.copy_content("static", "public")
    utils.generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()

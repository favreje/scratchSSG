import os
from shutil import copy, rmtree
from markdown_to_html import extract_title


def copy_content(source, dest):
    """
    Copies a file tree structure (all files in the parent directory and subdirectories) from a
    source location to a destination location.

    For the purposes of this SSG project, it is used to copy the files from a static directory to a
    public directory to stage blog data for a website.

    Args:
        source (string): the path to the source directory
        dest (string): the path to the destination directory

    Returns:
        None: The function copies files from source to dest; nothing is returned
    """
    if os.path.exists(dest):
        rmtree(dest)
    os.mkdir(dest)
    rcopy(source, dest)


def rcopy(source, dest):
    """
    Used as a helper function in copy_content to recursively copy files and subdirectories

    Args:
        source (string): the path to the source directory
        dest (string): the path to the destination directory

    Returns:
        None: The function copies files from source to dest; nothing is returned
    """
    if not os.path.exists(dest):
        os.mkdir(dest)
    for object in os.listdir(source):
        source_path = f"{source}/{object}"
        dest_path = f"{dest}/{object}"
        if os.path.isfile(source_path):
            print(f"source file={source_path}", end=" --> ")
            print(f"dest file={dest_path}")
            copy(source_path, dest_path)
        else:
            rcopy(source_path, dest_path)


def extact_file_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def generate_page(from_path, template_path, dest_path):
    md_file = extact_file_data(from_path)
    template = extact_file_data(template_path)
    title = extract_title(md_file)
    dest_file = template.replace(" {{ Title }} ", str(title))
    return md_file, dest_file


if __name__ == "__main__":
    # source = "test-file-copy-source"
    # dest = "test-file-copy-dest"
    # copy_content(source, dest)

    source = "content/index.md"
    template = "template.html"
    raw_md_file, destination = generate_page(source, template, None)
    print(raw_md_file)
    print()
    print(destination)

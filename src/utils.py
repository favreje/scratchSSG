import os
from shutil import copy, rmtree
from markdown_to_html import extract_title, markdown_to_html_node


def copy_content(source, dest):
    """
    Removes existing content from 'dest' and recursively copies the file tree structure from
    'source' to 'dest'

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


def get_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def put_file(file_path, content):
    dir_path, _ = os.path.split(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_page(from_path, template_path, dest_path):
    md_file = get_file(from_path)
    template = get_file(template_path)
    title = extract_title(md_file)
    html_node = markdown_to_html_node(md_file)
    html = html_node.to_html()
    content = template.replace(" {{ Title }} ", str(title))
    content = content.replace(" {{ Content }}", html)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    put_file(dest_path, content)


def generate_pages_recursive(dir_path, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path)
    for object in dir_contents:
        full_path = os.path.join(dir_path, object)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(object)
            if ext == ".md":
                base_name, _ = os.path.splitext(object)
                dest_file = os.path.join(dest_dir_path, base_name + ".html")
                generate_page(full_path, template_path, dest_file)
            else:
                print(f"{object} is not markdown... copying file to {dest_dir_path}")
                copy(full_path, dest_dir_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, object)
            if not os.path.exists(new_dest_dir_path):
                os.makedirs(new_dest_dir_path)
            generate_pages_recursive(full_path, template_path, new_dest_dir_path)


if __name__ == "__main__":

    # html_file = generate_page(source, template, destination)
    generate_pages_recursive("content", "template.html", "test_dir")

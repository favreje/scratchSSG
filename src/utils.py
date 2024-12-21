import os
from shutil import copy, rmtree


def copy_content(source, dest):
    if os.path.exists(dest):
        rmtree(dest)
    os.mkdir(dest)
    rcopy(source, dest)


def rcopy(source, dest):
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


def main():
    source = "test-file-copy-source"
    dest = "test-file-copy-dest"
    copy_content(source, dest)


if __name__ == "__main__":
    main()

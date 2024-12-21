import utils


def main():
    print(f"\n{'-' * 99}\nHello, Main Module.\n")
    source = "static"
    dest = "public"
    utils.copy_content(source, dest)


if __name__ == "__main__":
    main()

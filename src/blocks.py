def markdown_to_blocks(markdown):
    raw_blocks = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in raw_blocks if block]

def is_full_width_block(block, page_width, threshold=0.72):
    c = block.get("coordinates")
    if not c:
        return True
    return (c["x2"] - c["x1"]) / page_width >= threshold


def split_blocks_by_layout(blocks):
    blocks_with_coords = [b for b in blocks if b.get("coordinates")]
    page_width = max(b["coordinates"]["x2"] for b in blocks_with_coords)

    full_width, column_blocks = [], []

    for b in blocks:
        if is_full_width_block(b, page_width):
            full_width.append(b)
        else:
            column_blocks.append(b)

    return full_width, column_blocks, page_width
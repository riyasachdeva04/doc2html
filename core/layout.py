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

def detect_num_columns(blocks, page_width):

    if not blocks:
        return 1

    widths = []

    for b in blocks:
        c = b.get("coordinates")
        if not c:
            continue

        width = c["x2"] - c["x1"]

        if width < 0.9 * page_width:
            widths.append(width)

    if not widths:
        return 1

    widths.sort()
    median_width = widths[len(widths) // 2]

    estimated_columns = round(page_width / median_width)

    return estimated_columns

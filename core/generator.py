from core.sources import PDFSources
from core.layout import split_blocks_by_layout
from core.renderer import BlockRenderer
from assets.css import CSS

class PDFToHTMLGenerator:
    def __init__(self, mode="scanned", dpi=225):
        self.mode = mode
        self.dpi = int(dpi)

    def generate_html(self, json_files, pdf_path, output_path):
        sources = PDFSources(self.mode, self.dpi)
        sources.prepare(pdf_path)

        renderer = BlockRenderer(
            self.mode, sources, pdf_path, self.dpi
        )

        html_out = f"""<!DOCTYPE html>
<html lang="gu">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
"""

        for page_data in json_files:
            page = page_data["data"]
            page_num = page["page_number"] - 1

            blocks = sorted(
                page["reading_order"]["sequence"],
                key=lambda b: b["reading_order"]
            )

            full_width, column_blocks, page_width = split_blocks_by_layout(blocks)

            has_columns = (
                column_blocks
                and any(b["coordinates"]["x1"] < page_width * 0.45 for b in column_blocks)
                and any(b["coordinates"]["x1"] > page_width * 0.55 for b in column_blocks)
            )

            html_out += "<div class='page-container'>\n"

            if not has_columns:
                for b in blocks:
                    html_out += renderer.render_block(page_num, b, 4)
                html_out += "</div>\n"
                continue

            mid = page_width / 2
            left = [b for b in column_blocks if b["coordinates"]["x1"] < mid]
            right = [b for b in column_blocks if b["coordinates"]["x1"] >= mid]

            for b in full_width:
                html_out += renderer.render_block(page_num, b, 4)

            html_out += "<div class='column-layout'>\n<div class='column'>\n"
            for b in left:
                html_out += renderer.render_block(page_num, b, 6)
            html_out += "</div>\n<div class='column'>\n"
            for b in right:
                html_out += renderer.render_block(page_num, b, 6)
            html_out += "</div>\n</div>\n</div>\n"

        html_out += "</body></html>"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_out)
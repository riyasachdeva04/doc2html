import html
import pdfplumber
from utils.image import image_to_base64


class BlockRenderer:
    def __init__(self, mode, sources, pdf_path, dpi):
        self.mode = mode
        self.sources = sources
        self.pdf_path = pdf_path
        self.dpi = dpi

    def render_figure(self, page_num, block):
        # Scanned PDF
        if self.mode == "scanned":
            coords = block.get("coordinates")
            if not coords:
                return ""

            img = self.sources.page_images[page_num]
            crop = img.crop((
                int(coords["x1"]),
                int(coords["y1"]),
                int(coords["x2"]),
                int(coords["y2"])
            ))

        # Digital PDF (spatial image order)
        else:
            images = self.sources.sorted_images_by_page.get(page_num)
            if not images:
                return ""

            img_obj = images.pop(0)

            with pdfplumber.open(self.pdf_path) as pdf:
                page = pdf.pages[page_num]
                crop = page.crop((
                    img_obj["x0"],
                    img_obj["top"],
                    img_obj["x1"],
                    img_obj["bottom"]
                )).to_image(resolution=self.dpi).original

        b64 = image_to_base64(crop)
        return f'<img src="data:image/png;base64,{b64}">'

    def render_block(self, page_num, block, indent):
        pad = " " * indent
        tag = block.get("layout_tag", "paragraph")
        text = html.escape(block.get("block_text", ""))

        if tag == "figure":
            img_html = self.render_figure(page_num, block)
            return f"""{pad}<div class="block figure">
{pad}  {img_html}
{pad}</div>\n"""

        if tag in ("title", "headline"):
            return f'{pad}<div class="block {tag}">{text}</div>\n'

        return f'{pad}<p class="block paragraph">{text}</p>\n'

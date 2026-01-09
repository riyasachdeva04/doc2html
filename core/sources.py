import pdfplumber


class PDFSources:
    def __init__(self, mode, dpi):
        self.mode = mode
        self.dpi = dpi

        # For scanned PDFs
        self.page_images = {}

        # For digital PDFs (IMPORTANT)
        self.sorted_images_by_page = {}

    def prepare(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):

                # Scanned PDF → full page image
                if self.mode == "scanned":
                    self.page_images[i] = page.to_image(
                        resolution=self.dpi
                    ).original

                # Digital PDF → spatially sorted images
                else:
                    images = page.images.copy()

                    # Sort images: top to bottom, left to right
                    images.sort(key=lambda img: (img["top"], img["x0"]))

                    self.sorted_images_by_page[i] = images

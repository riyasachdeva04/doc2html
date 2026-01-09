import pdfplumber
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PDF_PATH = "input.pdf"

# Example bbox: (x0, top, x1, bottom)
BBOX = (1070, 135, 1850, 1140)

def plot_bbox_on_pdf(pdf_path, bbox):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            img = page.to_image(resolution=150)
            fig, ax = plt.subplots(figsize=(6, 8))
            ax.imshow(img.original)

            x0, top, x1, bottom = bbox
            width = x1 - x0
            height = bottom - top

            rect = patches.Rectangle(
                (x0, top),
                width,
                height,
                linewidth=2,
                edgecolor="red",
                facecolor="none"
            )

            ax.add_patch(rect)
            ax.set_title(f"Page {page_num}")
            ax.axis("off")
            plt.show()
            break

plot_bbox_on_pdf("input/Kumar/kumar.pdf", BBOX)

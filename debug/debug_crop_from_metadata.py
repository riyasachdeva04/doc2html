import cv2
import numpy as np
import pdfplumber
from pathlib import Path
from PIL import Image


def extract_images_from_scanned_pdf(
    pdf_path,
    out_dir="scanned_images",
    dpi=300,
    min_area_ratio=0.02
):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            page_img = page.to_image(resolution=dpi).original
            img = np.array(page_img)

            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            # ---- 1. Suppress text using adaptive threshold
            thresh = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                35, 15
            )

            # ---- 2. Morphology to merge image regions
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
            merged = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            # ---- 3. Find connected components
            contours, _ = cv2.findContours(
                merged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            page_area = img.shape[0] * img.shape[1]
            img_count = 0

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w * h

                # ---- 4. Filter small (text) regions
                if area < page_area * min_area_ratio:
                    continue

                # ---- 5. Crop and save
                crop = img[y:y+h, x:x+w]
                pil_crop = Image.fromarray(crop)

                out_file = out_dir / f"page_{page_idx+1:03d}_img_{img_count}.png"
                pil_crop.save(out_file)

                img_count += 1

            print(f"✓ Page {page_idx+1}: {img_count} images extracted")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_file")
    parser.add_argument("--out", default="scanned_images")
    args = parser.parse_args()

    extract_images_from_scanned_pdf(args.pdf_file, args.out)

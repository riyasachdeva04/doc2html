import pdfplumber
import matplotlib.pyplot as plt
import numpy as np

points = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((int(event.xdata), int(event.ydata)))
        print(f"Clicked: {points[-1]}")
        if len(points) == 2:
            plt.close()

def mark_bbox(pdf_path, page_number=0):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        img = page.to_image(resolution=300).original

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("Click TOP-LEFT, then BOTTOM-RIGHT of image")
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    if len(points) != 2:
        raise RuntimeError("You must click exactly two points")

    (x1, y1), (x2, y2) = points
    bbox = {
        "x1": min(x1, x2),
        "y1": min(y1, y2),
        "x2": max(x1, x2),
        "y2": max(y1, y2),
    }

    return bbox


if __name__ == "__main__":
    bbox = mark_bbox("input/Kumar/kumar.pdf", page_number=0)
    print("\nBounding box:")
    print(bbox)

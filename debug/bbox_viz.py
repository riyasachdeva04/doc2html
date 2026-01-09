import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import fitz  # PyMuPDF

def draw_bounding_boxes(pdf_path, json_dir, output_dir, dpi=150):

    pdf_path = Path(pdf_path)
    json_dir = Path(json_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    
    colors = {
        "figure": "red",
        "table": "blue",
        "text": "green",
        "title": "purple",
        "list": "orange",
        "caption": "cyan",
    }
    
    json_files = sorted(json_dir.glob("page_*_reading_order.json"))
    
    if not json_files:
        print(f"No JSON files found in {json_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        page_num = data.get("page_number", 0)
        
        if page_num >= len(doc):
            print(f"Page {page_num} out of range (PDF has {len(doc)} pages)")
            continue
        
        page = doc[page_num]
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
        
        # Draw bounding boxes
        blocks = data.get("reading_order", {}).get("sequence", [])
        
        print(f"\nProcessing page {page_num} ({json_file.name}):")
        print(f"  Image dimensions: {img.width}x{img.height}")
        print(f"  Found {len(blocks)} blocks")
        
        for block in blocks:
            coords = block.get("coordinates")
            if not coords:
                continue
            
            block_id = block.get("block_id", "unknown")
            layout_tag = block.get("layout_tag", "unknown")
            reading_order = block.get("reading_order", "?")
            
            # Get color for this layout tag
            color = colors.get(layout_tag, "yellow")
            
            # Draw rectangle
            x1, y1 = int(coords["x1"]), int(coords["y1"])
            x2, y2 = int(coords["x2"]), int(coords["y2"])
            
            # Check if coordinates are within image bounds
            if x1 < 0 or y1 < 0 or x2 > img.width or y2 > img.height:
                print(f"  WARNING: {block_id} coordinates out of bounds!")
                print(f"    Coords: ({x1}, {y1}) to ({x2}, {y2})")
                print(f"    Image size: {img.width}x{img.height}")
            
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw label
            label = f"{reading_order}: {layout_tag}\n{block_id}"
            
            # Draw label background
            bbox = draw.textbbox((x1, y1 - 45), label, font=font)
            draw.rectangle(bbox, fill=color)
            draw.text((x1, y1 - 45), label, fill="white", font=font)
        
        # Save annotated image
        output_path = output_dir / f"page_{page_num}_annotated.png"
        img.save(output_path)
        print(f"  Saved to {output_path}")
    
    doc.close()
    print(f"\n✓ All annotated images saved to {output_dir}")


def analyze_single_block(pdf_path, page_num, block_coords, dpi=150):
    """
    Analyze a single block and show the cropped region.
    
    Args:
        pdf_path: Path to the PDF file
        page_num: Page number (0-indexed)
        block_coords: Dictionary with x1, y1, x2, y2 keys
        dpi: DPI for rendering PDF pages (default 150)
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    
    # Render page
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    print(f"Page {page_num} dimensions: {img.width}x{img.height}")
    print(f"Crop coordinates: ({block_coords['x1']}, {block_coords['y1']}) to ({block_coords['x2']}, {block_coords['y2']})")
    
    # Crop
    crop = img.crop((
        int(block_coords["x1"]),
        int(block_coords["y1"]),
        int(block_coords["x2"]),
        int(block_coords["y2"])
    ))
    
    print(f"Cropped image dimensions: {crop.width}x{crop.height}")
    
    doc.close()
    return img, crop


# Example usage:
if __name__ == "__main__":
    # Configuration
    PDF_PATH = "input/Kumar/kumar.pdf"
    JSON_DIR = "input/Kumar/Kumar_Output" 
    OUTPUT_DIR = "annotated_pages"
    DPI = 150 
    
    draw_bounding_boxes(PDF_PATH, JSON_DIR, OUTPUT_DIR, dpi=DPI)
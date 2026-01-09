# PDF → HTML (Deterministic Layout Reconstruction)

This project converts PDFs into structured HTML using page-wise layout JSONs
(reading order, labels, and coordinates).

## Approach

1. **Input**
   - PDF document
   - Page-wise JSONs with layout tags, reading order, and bounding boxes

2. **PDF Handling**
   - **Scanned PDFs**: pages are rasterized, figures are cropped using block coordinates
   - **Digital PDFs**: images are extracted and spatially sorted (top → bottom, left → right)

3. **Layout Reconstruction**
   - Reading order from JSON is treated as authoritative
   - Blocks are classified geometrically into:
     - **Full-width blocks** (titles, wide figures)
     - **Column blocks** (multi-column text)
   - Columns are inferred using x-position relative to page width

4. **Rendering**
   - One A4-sized HTML container per page
   - Full-width blocks rendered before columns
   - Column content rendered left-to-right
   - Figures rendered as page-level elements to avoid layout breakage

## Notes

- For **scanned PDFs**, figures are extracted by cropping the rasterized page using
  bounding boxes from the layout JSONs. Since these bounding boxes are derived from
  scanned content rather than embedded digital objects, image crops may occasionally
  include extra surrounding regions.

## Outputs

- Generated HTML files for both documents:
  - [CVRaman_Digital_output.html](CVRaman_Digital_output.html)
  - [Kumar_Scanned_output.html](Kumar_Scanned_output.html)

## Usage

```bash
pip install -r requirements.txt
python main.py --pdf input.pdf --json json_dir --output output.html --mode scanned|digital

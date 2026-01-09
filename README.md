# PDF → HTML (Deterministic Layout Reconstruction)

This project converts PDFs into structured HTML using page-wise layout JSONs
(reading order, labels, and coordinates).

## Approach

1. **Input**
   - PDF document
   - Page-wise JSONs with layout tags, reading order, and bounding boxes

2. **Layout Reconstruction**
   - Reading order from JSON is treated as authoritative
   - Blocks are classified geometrically into:
     - **Full-width blocks** (titles, wide figures)
     - **Column blocks** (multi-column text)
   - Columns are inferred using x-position relative to page width

3. **Rendering**
   - One A4-sized HTML container per page
   - Full-width blocks rendered before columns
   - Column content rendered left-to-right
   - Figures rendered as page-level elements to avoid layout breakage

## Outputs

- Generated HTML files for both documents:
  - [CVRaman_output.html](CVRaman_output.html)
  - [Kumar_output.html](Kumar_output.html)

## Usage

```bash
pip install -r requirements.txt
python main.py --pdf input.pdf --json json_dir --output output.html --dpi res

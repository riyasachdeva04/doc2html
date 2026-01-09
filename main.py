import json
from pathlib import Path
from core.generator import PDFToHTMLGenerator

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode", choices=["scanned", "digital"], required=True)
    args = parser.parse_args()

    json_files = []
    for f in Path(args.json).glob("*.json"):
        json_files.append({
            "data": json.loads(f.read_text(encoding="utf-8"))
        })

    json_files.sort(key=lambda x: x["data"]["page_number"])

    gen = PDFToHTMLGenerator(mode=args.mode)
    gen.generate_html(json_files, args.pdf, args.output)

    print("✓ HTML generated:", args.output)

if __name__ == "__main__":
    main()
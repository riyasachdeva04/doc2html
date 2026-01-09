CSS = """
* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: 'Noto Sans Gujarati','Noto Sans',Arial,sans-serif;
  background:#f5f5f5;
  padding:20px;
}

.page-container {
  width:210mm;
  min-height:297mm;
  background:white;
  margin:0 auto 20px;
  padding:20mm;
  box-shadow:0 2px 10px rgba(0,0,0,0.1);
  page-break-after:always;
}

.block { margin-bottom:1em; break-inside:avoid; }

.paragraph {
  font-size:14pt;
  line-height:1.8;
  text-align:justify;
}

.title {
  font-size:28pt;
  font-weight:bold;
  text-align:center;
  margin:2em 0 1em;
}

.headline {
  font-size:24pt;
  font-weight:bold;
  text-align:center;
}

.figure { text-align:center; margin:1.5em 0; }
.figure img { max-width:100%; border:1px solid #ddd; }

.column-layout {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:20px;
}

.column { break-inside:avoid; }
"""
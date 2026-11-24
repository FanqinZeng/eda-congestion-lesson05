"""Build only generated/example.py and generated/reference.html."""
from pathlib import Path
from html import escape

root = Path(__file__).resolve().parent
out = root / "generated"
out.mkdir(exist_ok=True)
source = (root / "reference.py").read_bytes()
(out / "example.py").write_bytes(source)
page = ('<!doctype html><meta charset="utf-8"><title>Python · Mini Placement</title>'
        '<h1>Python · Mini Placement</h1><pre>' + escape(source.decode()) + '</pre>')
(out / "reference.html").write_text(page, encoding="utf-8")

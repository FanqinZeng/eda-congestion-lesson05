import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path

from reference import geometry

root = Path(__file__).resolve().parent
cases = [
    [["2.35", "1.02"], ["4", "2"]],
    [["2.45", "1.02"], ["4", "2"]],
    [["2.85", "1.02"], ["4", "2"]],
    [["1", "0"], ["1.9999999995", "0"]],
    [["1", "0"], ["2", "0"]],
    [["1", "0"], ["2.0000000005", "0"]],
    [["0", "0"], ["0", "1.999999999999999999999"]],
    [["-0.0000000005", "0"], ["7", "4"]],
    [["0", "0"], ["0", "0"]],
]
js = """const m=require('./model.js'); const cells=JSON.parse(process.argv[1]);
console.log(JSON.stringify(cells.map(pair=>m.geometry(...pair.map(([x,y])=>({x,y}))))));"""
results = json.loads(subprocess.check_output(["node","-e",js,json.dumps(cases)],cwd=root))
for (a, b), result in zip(cases, results):
    area, cells = geometry(a, b)
    assert Fraction(result["area"]) == area
    assert result["cells"] == cells and result["overlap"] == (area > 0)
print(len(cases), "exact JS/Python comparisons OK")


class Reading(HTMLParser):
    inside = False
    text = ""
    def handle_starttag(self, tag, attrs):
        if tag == "pre": self.inside = True
    def handle_endtag(self, tag):
        if tag == "pre": self.inside = False
    def handle_data(self, text):
        if self.inside: self.text += text


def hashes(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp) / "checkout"
    shutil.copytree(root,project,ignore=shutil.ignore_patterns("generated","__pycache__",".git"))
    before = hashes(project)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for _ in range(2):
        subprocess.run([sys.executable,"-I",project/"generate.py"],cwd=tmp,env=env,check=True)
        after=hashes(project)
        assert {k:v for k,v in after.items() if k in before}==before
        assert after.keys()-before.keys()=={"generated/example.py","generated/reference.html"}
        assert after==hashes(root)
    reader=Reading()
    reader.feed((project/"generated/reference.html").read_text())
    assert reader.text==(project/"reference.py").read_text()==(project/"generated/example.py").read_text()
    subprocess.run([sys.executable,"-I",project/"generated/example.py"],cwd=tmp,check=True)
print("Isolated regeneration twice, source hashes, reference HTML and runnable example OK")

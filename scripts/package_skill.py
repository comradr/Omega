#!/usr/bin/env python3
from __future__ import annotations
import hashlib, subprocess, sys, zipfile
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(65536),b""): h.update(b)
    return h.hexdigest()

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    validator=root/"scripts"/"validate_skill.py"
    subprocess.run([sys.executable,str(validator),str(root)],check=True)
    for ext in ("zip","skill"):
        out=root.parent/f"{root.name}.{ext}"
        with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
            for p in root.rglob("*"):
                if p.is_file() and "__pycache__" not in p.parts:
                    z.write(p,Path(root.name)/p.relative_to(root))
        print(f"{out} sha256={sha256(out)}")
if __name__=="__main__": main()

#!/usr/bin/env python3
from __future__ import annotations
import ast, re, sys
from pathlib import Path

NAME_RE=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    errors=[]
    skill=root/"SKILL.md"
    if not skill.is_file():
        errors.append("Missing SKILL.md")
    else:
        text=skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("Invalid frontmatter")
        else:
            raw=text[4:text.find("\n---\n",4)]
            fields={}
            for line in raw.splitlines():
                if ":" in line:
                    k,v=line.split(":",1); fields[k.strip()]=v.strip()
            extra=set(fields)-{"name","description"}
            if extra: errors.append(f"Unsupported frontmatter fields: {sorted(extra)}")
            name=fields.get("name","")
            if not NAME_RE.fullmatch(name) or len(name)>64: errors.append("Invalid skill name")
            if root.name!=name: errors.append(f"Folder name '{root.name}' must match skill name '{name}'")
            if len(fields.get("description",""))<40: errors.append("Description is too short")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
            if not target.startswith(("http://","https://","#")):
                p=target.split("#",1)[0]
                if p and not (root/p).exists(): errors.append(f"Broken local link: {target}")
    for p in root.rglob("*.py"):
        try: ast.parse(p.read_text(encoding="utf-8"),filename=str(p))
        except Exception as e: errors.append(f"Python syntax error in {p}: {e}")
    if errors:
        for e in errors: print("ERROR:",e)
        return 1
    print("VALID: 0 warning(s)")
    return 0
if __name__=="__main__": raise SystemExit(main())

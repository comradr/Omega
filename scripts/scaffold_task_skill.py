#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
NAME_RE=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("name"); p.add_argument("--path",default=".")
    p.add_argument("--description",required=True); p.add_argument("--display-name")
    p.add_argument("--with-references",action="store_true"); p.add_argument("--with-scripts",action="store_true")
    a=p.parse_args()
    if len(a.name)>64 or not NAME_RE.fullmatch(a.name): raise SystemExit("Invalid skill name")
    root=Path(a.path)/a.name
    if root.exists() and any(root.iterdir()): raise SystemExit(f"Refusing to overwrite {root}")
    (root/"agents").mkdir(parents=True,exist_ok=True)
    if a.with_references: (root/"references").mkdir()
    if a.with_scripts: (root/"scripts").mkdir()
    display=a.display_name or a.name.replace("-"," ").title()
    (root/"SKILL.md").write_text(f"---\nname: {a.name}\ndescription: {json.dumps(a.description,ensure_ascii=False)}\n---\n\n# {display}\n\n## Objective\n\nDefine the durable task-specific workflow and invariants here.\n\n## Workflow\n\n1. Inspect the source of truth.\n2. Execute the task-specific procedure.\n3. Verify observable completion criteria.\n",encoding="utf-8")
    default="Use this task-specific workflow to execute the request according to its project rules and verification requirements."
    (root/"agents"/"openai.yaml").write_text("interface:\n"+f"  display_name: {json.dumps(display)}\n  short_description: \"Task-specific execution workflow\"\n  default_prompt: {json.dumps(default)}\npolicy:\n  allow_implicit_invocation: true\n",encoding="utf-8")
    print(root)
if __name__=="__main__": main()

#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    skill=(root/"SKILL.md").read_text(encoding="utf-8").lower()
    refs="\n".join(p.read_text(encoding="utf-8").lower() for p in (root/"references").glob("*.md"))
    errors=[]
    required={
      "routing":"overhead-and-routing.md",
      "runtime":"runtime-adaptation.md",
      "trust":"trust-boundaries.md",
      "behavior":"behavior-mining.md",
      "evidence":"prompting-evidence.md",
      "empirical":"empirical-evaluation.md"
    }
    for label,name in required.items():
        if not (root/"references"/name).is_file(): errors.append(f"missing {label}: {name}")
    for f in ("trigger-evals.json","behavior-evals.json"):
        try:
            data=json.loads((root/"evals"/f).read_text(encoding="utf-8"))
            if not data.get("cases"): errors.append(f"{f}: no cases")
        except Exception as e: errors.append(f"{f}: {e}")
    anchors=["architectural overhead","runtime","trust","behavior","empirical"]
    combined=skill+"\n"+refs
    for a in anchors:
        if a not in combined: errors.append(f"missing concept anchor: {a}")
    if errors:
        print("\n".join("ERROR: "+x for x in errors)); return 1
    print("STATIC-EVALS: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())

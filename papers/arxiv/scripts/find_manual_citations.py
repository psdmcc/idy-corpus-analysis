#!/usr/bin/env python3

import re
import sys

texfile = sys.argv[1] if len(sys.argv) > 1 else "main.tex"

pattern = re.compile(r"\[\[([^\]]+)\]\]")

with open(texfile, encoding="utf-8") as f:
    for lineno, line in enumerate(f, start=1):
        for match in pattern.finditer(line):
            print(f"{lineno}: [[{match.group(1)}]]")

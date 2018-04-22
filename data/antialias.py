#!/usr/bin/python
from __future__ import print_function
import json
import sys
import re

aliases = json.load(open("aliases.json","r"))
regexes = {}
for line in sys.stdin:
    for entry in aliases:
        for alias in aliases[entry]:
            if alias not in regexes:
                regexes[alias] = re.compile(re.escape(alias), re.IGNORECASE)
            line = regexes[alias].sub(entry, line)
    sys.stdout.write(line)
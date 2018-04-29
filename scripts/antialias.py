#!/usr/bin/python

# replaces all instances of the aliases in a file with their standardized form
# read from stdin and write to stdout
from __future__ import print_function
import json
import sys
import re

# file where aliases are stored
aliases = json.load(open("aliases.json","r"))
regexes = {}
for line in sys.stdin:
    for entry in aliases:
        for alias in aliases[entry]:
            # cache compiled regexes for performance
            if alias not in regexes:
                regexes[alias] = re.compile(re.escape(alias), re.IGNORECASE)
            line = regexes[alias].sub(entry, line)
    sys.stdout.write(line)
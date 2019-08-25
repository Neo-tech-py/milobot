import sys
from os import listdir
from os.path import join

from pylint.lint import Run

THRESHOLD = 9.75

cogs = [join("cogs", c) for c in listdir("cogs") if c.endswith(".py")]


results = Run(["main.py", *cogs], do_exit=False)

score = results.linter.stats["global_note"]
if score <= THRESHOLD:
    sys.exit(1)

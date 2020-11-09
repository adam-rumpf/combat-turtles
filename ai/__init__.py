"""Automatically imports all AI submodules.

The AI directory may contain various user-defined modules. This initialization
script imports all submodules, defined as .py files whose names do not begin
with an underscore (_).

In the main driver, specific AI classes will be referred to using the format
'tc.ai.<submodule>.CombatTurtle', where '<submodule>' is the name of the .py
file. This script loads all valid submodule names into this module's __all__
attribute.
"""

import os.path
import glob

# Gather all .py files
files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

# Define __all__ as a filtered list of those files
__all__ = []
for f in files:
    # Ignore non-files
    if os.path.isfile(f) == False:
        continue
    # Ignore files beginning with an underscore
    if os.path.basename(f).startswith("_"):
        continue
    # Take the file name minus the ".py" extension
    __all__.append(os.path.splitext(os.path.basename(f))[0])

del files

# Import attributes
from . import *

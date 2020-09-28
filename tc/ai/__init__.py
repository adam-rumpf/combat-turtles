# Automatically import all AI submodules, defined as .py files whose names do
# not begin with an underscore (_).

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

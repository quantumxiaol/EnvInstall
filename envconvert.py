
"""
python convertenv.py requirements.txt >> pyproject.toml
"""

import sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, ver = line.split("==", 1)
        print(f'"{name}=={ver}",')
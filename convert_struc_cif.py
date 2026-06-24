#!/usr/bin/env python3
"""
Convert structure files to CIF format.

Accepts POSCAR, CIF, or any other format pymatgen can read. Output basename
matches the input with a ``.cif`` suffix. If that file already exists, writes
``*_conv.cif`` instead.

Usage:
    convert_struc_cif.py FILE [FILE ...]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from struc_utils import convert_structures, parse_args


def main() -> None:
    convert_structures(parse_args(), fmt="cif", suffix=".cif", tag="conv")


if __name__ == "__main__":
    main()

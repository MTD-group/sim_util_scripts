#!/usr/bin/env python3
"""
Reduce a structure to its primitive cell and write CIF format.

Uses pymatgen's ``SpacegroupAnalyzer`` with symprec=1e-4 and angle_tolerance=0.1
(VASP defaults). Output basename matches the input with a ``.cif`` suffix. If
that file already exists, writes ``*_prim.cif`` instead.

Usage:
    convert_struc_prim_cif.py FILE [FILE ...]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from struc_utils import convert_structures, parse_args


def main() -> None:
    convert_structures(
        parse_args(),
        fmt="cif",
        suffix=".cif",
        tag="prim",
        primitive=True,
    )


if __name__ == "__main__":
    main()

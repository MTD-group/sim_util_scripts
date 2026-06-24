#!/usr/bin/env python3
"""
Reduce a structure to its primitive cell and write CIF format.

Uses pymatgen's ``SpacegroupAnalyzer`` (default symprec=1e-4, angle_tolerance=0.1).
Output basename matches the input with a ``.cif`` suffix. If that file already exists,
writes ``*_prim.cif`` instead.

Usage:
    convert_struc_prim_cif.py [--symprec SYMPREC] [--angle-tol DEG] FILE [FILE ...]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from struc_utils import convert_structures, parse_prim_args


def main() -> None:
    file_names, symprec, angle_tol = parse_prim_args()
    convert_structures(
        file_names,
        fmt="cif",
        suffix=".cif",
        tag="prim",
        primitive=True,
        symprec=symprec,
        angle_tolerance=angle_tol,
    )


if __name__ == "__main__":
    main()

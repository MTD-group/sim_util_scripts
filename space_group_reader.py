#!/usr/bin/env python3
"""
Report space-group symbol and number at several symmetry tolerances.

By default, prints a table of (symprec, angle_tolerance) pairs and the space group
pymatgen assigns at each setting. Pass ``--symprec`` and/or ``--angle-tol`` to report
a single tolerance pair instead.

Usage:
    space_group_reader.py [--symprec SYMPREC] [--angle-tol DEG] FILE [FILE ...]
"""

from __future__ import annotations

import argparse

from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

DEFAULT_SYMPREC = 1e-4
DEFAULT_ANGLE_TOL = 0.1

# (symprec, angle_tolerance) pairs from tight to loose matching.
# Tighter tolerances reveal symmetry broken by small distortions; looser ones
# recover higher symmetry when atoms are nearly equivalent.
TOLERANCE_GRID: list[tuple[float, float]] = [
    (1e-6, 0.01),
    (1e-5, 0.1),
    (1e-4, 0.1),
    (1e-4, 1.0),
    (1e-3, 2.0),
    (1e-2, 5.0),
    (1e-1, 5.0),
    (1.0, 5.0),
]


def parse_args() -> tuple[list[str], list[tuple[float, float]]]:
    parser = argparse.ArgumentParser(
        description="Report space-group assignment at one or more tolerance settings.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="structure files to analyze",
    )
    parser.add_argument(
        "--symprec",
        type=float,
        help=(
            f"symmetry tolerance in Angstrom (default: sweep preset grid, "
            f"or {DEFAULT_SYMPREC:g} with --angle-tol)"
        ),
    )
    parser.add_argument(
        "--angle-tol",
        "--angle-tolerance",
        type=float,
        dest="angle_tol",
        help=(
            f"angle tolerance in degrees (default: sweep preset grid, "
            f"or {DEFAULT_ANGLE_TOL:g} with --symprec)"
        ),
    )
    args = parser.parse_args()

    if args.symprec is None and args.angle_tol is None:
        tolerances = TOLERANCE_GRID
    else:
        symprec = DEFAULT_SYMPREC if args.symprec is None else args.symprec
        angle_tol = DEFAULT_ANGLE_TOL if args.angle_tol is None else args.angle_tol
        tolerances = [(symprec, angle_tol)]

    return args.files, tolerances


def report_space_groups(
    file_path: str, tolerances: list[tuple[float, float]]
) -> None:
    """Print a tolerance table for one structure file."""
    structure = Structure.from_file(file_path)
    print(f"\n{file_path}")
    print(f"{'symprec':>10}  {'angle_tol':>10}  {'symbol':<12}  number")
    print("-" * 48)

    for symprec, angle_tol in tolerances:
        analyzer = SpacegroupAnalyzer(
            structure, symprec=symprec, angle_tolerance=angle_tol
        )
        symbol = analyzer.get_space_group_symbol()
        number = analyzer.get_space_group_number()
        print(f"{symprec:>10g}  {angle_tol:>10g}  {symbol:<12}  {number}")


def main() -> None:
    file_paths, tolerances = parse_args()
    for file_path in file_paths:
        report_space_groups(file_path, tolerances)


if __name__ == "__main__":
    main()

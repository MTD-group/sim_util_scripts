#!/usr/bin/env python3
"""
Report space-group symbol and number at several symmetry tolerances.

For each input structure, prints a table of (symprec, angle_tolerance) pairs
and the space group pymatgen assigns at each setting. Comparing rows helps judge
how sensitive the assigned symmetry is to small distortions or numerical noise.

Usage:
    space_group_reader.py FILE [FILE ...]
"""

from __future__ import annotations

import sys
from pathlib import Path

from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

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


def parse_args() -> list[str]:
    if len(sys.argv) < 2:
        print(f"Usage: {Path(sys.argv[0]).name} FILE [FILE ...]", file=sys.stderr)
        sys.exit(1)
    return sys.argv[1:]


def report_space_groups(file_path: str) -> None:
    """Print a tolerance sweep table for one structure file."""
    structure = Structure.from_file(file_path)
    print(f"\n{file_path}")
    print(f"{'symprec':>10}  {'angle_tol':>10}  {'symbol':<12}  number")
    print("-" * 48)

    for symprec, angle_tol in TOLERANCE_GRID:
        analyzer = SpacegroupAnalyzer(
            structure, symprec=symprec, angle_tolerance=angle_tol
        )
        symbol = analyzer.get_space_group_symbol()
        number = analyzer.get_space_group_number()
        print(f"{symprec:>10g}  {angle_tol:>10g}  {symbol:<12}  {number}")


def main() -> None:
    for file_path in parse_args():
        report_space_groups(file_path)


if __name__ == "__main__":
    main()

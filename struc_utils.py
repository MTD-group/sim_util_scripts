"""Shared helpers used by multiple conversion scripts."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# VASP-style symmetry tolerances used by the primitive-cell scripts.
DEFAULT_SYMPREC = 1e-4
DEFAULT_ANGLE_TOL = 0.1

# Extensions stripped when building an output basename.
_STRIP_SUFFIXES = (".VASP", ".vasp", ".cif", ".POSCAR", ".poscar", ".CIF")


def parse_args() -> list[str]:
    """Return input filenames from the command line, or exit with usage."""
    if len(sys.argv) < 2:
        print(f"Usage: {Path(sys.argv[0]).name} FILE [FILE ...]", file=sys.stderr)
        sys.exit(1)
    return sys.argv[1:]


def parse_prim_args() -> tuple[list[str], float, float]:
    """Return input files and symmetry tolerances for primitive-cell scripts."""
    parser = argparse.ArgumentParser(
        description="Reduce structures to the primitive cell.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="structure files to convert",
    )
    parser.add_argument(
        "--symprec",
        type=float,
        default=DEFAULT_SYMPREC,
        help=f"symmetry tolerance in Angstrom (default: {DEFAULT_SYMPREC:g})",
    )
    parser.add_argument(
        "--angle-tol",
        "--angle-tolerance",
        type=float,
        default=DEFAULT_ANGLE_TOL,
        dest="angle_tol",
        help=f"angle tolerance in degrees (default: {DEFAULT_ANGLE_TOL:g})",
    )
    args = parser.parse_args()
    return args.files, args.symprec, args.angle_tol


def convert_structures(
    file_names: list[str],
    fmt: str,
    suffix: str,
    tag: str,
    *,
    primitive: bool = False,
    symprec: float = DEFAULT_SYMPREC,
    angle_tolerance: float = DEFAULT_ANGLE_TOL,
) -> None:
    """Read each input file and write it in ``fmt`` format."""
    for file_name in file_names:
        structure = Structure.from_file(file_name)

        if primitive:
            analyzer = SpacegroupAnalyzer(
                structure, symprec=symprec, angle_tolerance=angle_tolerance
            )
            structure = analyzer.get_primitive_standard_structure()

        base = file_name
        for ext in _STRIP_SUFFIXES:
            if base.endswith(ext):
                base = base[: -len(ext)]
                break

        out_file_name = base + suffix
        if os.path.exists(out_file_name):
            out_file_name = out_file_name.replace(suffix, f"_{tag}{suffix}")

        print(f"{file_name}  ==>  {out_file_name}")
        structure.to(fmt=fmt, filename=out_file_name)

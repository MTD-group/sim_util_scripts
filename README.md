# Simulation Utility Scripts

Command-line helpers for common first-principles structure tasks:

- Convert between CIF and POSCAR
- Reduce structures to the primitive cell
- Sweep symmetry tolerances to see how space-group assignment changes

All scripts use [pymatgen](https://pymatgen.org/) for structure I/O and symmetry analysis.

## Requirements

- Python 3.9+
- pymatgen

```bash
pip install -r requirements.txt
```

## Setup

Clone the repo and add it to your `PATH` so the scripts are callable from anywhere.
Because the conversion scripts import shared code from `struc_utils.py`, keep the
repository layout intact (do not copy individual scripts elsewhere).

```bash
git clone https://github.com/<your-org>/sim_util_scripts.git
export PATH="/path/to/sim_util_scripts:$PATH"
```

Alternatively, run a script directly:

```bash
python /path/to/sim_util_scripts/convert_struc_cif.py structure.vasp
```

Make scripts executable if you prefer:

```bash
chmod +x /path/to/sim_util_scripts/*.py
```

## Scripts

### `convert_struc_cif.py`

Convert one or more structure files to CIF.

```bash
convert_struc_cif.py POSCAR Si.vasp
# POSCAR  ==>  POSCAR.cif
# Si.vasp  ==>  Si.cif
```

If the output file already exists, writes `*_conv.cif` instead.

### `convert_struc_poscar.py`

Convert one or more structure files to POSCAR (`.vasp`).

```bash
convert_struc_poscar.py structure.cif
# structure.cif  ==>  structure.vasp
```

If the output file already exists, writes `*_conv.vasp` instead.

### `convert_struc_prim_cif.py`

Find the standardized primitive cell (symprec=`1e-4`, angle tolerance=`0.1`) and write CIF.

```bash
convert_struc_prim_cif.py supercell.vasp
# supercell.vasp  ==>  supercell.cif
```

If the output file already exists, writes `*_prim.cif` instead.

### `convert_struc_prim_poscar.py`

Same primitive-cell reduction, written as POSCAR (`.vasp`).

```bash
convert_struc_prim_poscar.py structure.cif
# structure.cif  ==>  structure.vasp
```

If the output file already exists, writes `*_prim.vasp` instead.

### `space_group_reader.py`

Print space-group symbol and international number at several `(symprec, angle_tolerance)` pairs.
Use this to see whether a slightly distorted structure is classified as lower symmetry at
tight tolerances and recovers a higher-symmetry group when tolerances are relaxed.

```bash
space_group_reader.py distorted.cif
```

Example output:

```
distorted.cif
   symprec   angle_tol  symbol        number
------------------------------------------------
     1e-06        0.01  P1            1
     1e-05         0.1  Pm            6
     0.0001         0.1  Pm            6
     ...
```

## Notes

- Input formats: any structure format pymatgen supports (CIF, POSCAR/CONTCAR, XYZ, etc.).
- Output naming: extensions `.vasp`, `.cif`, `.POSCAR`, and `.poscar` are stripped from the
  input basename before the output suffix is appended.
- Primitive-cell scripts use VASP-style defaults (`symprec=1e-4`, `angle_tolerance=0.1`).
  Edit `DEFAULT_SYMPREC` and `DEFAULT_ANGLE_TOL` at the top of `struc_utils.py` to change them
  for both primitive scripts.

## License

See [LICENSE](LICENSE).

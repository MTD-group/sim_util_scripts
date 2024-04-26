"""
@author: Kyle Miller
Usage: python convert_struc_prim_poscar.py struc1 struc2
"""

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.core.structure import Structure
import sys
import os

def main():
    SYMPREC = 1e-4
    ANGLE_TOL = 0.1

    file_names = sys.argv[1:]
    for file_name in file_names:
        target_suffix = '.vasp'

        ### Parse structure
        struc = Structure.from_file(file_name)

        ### Get primitive structure
        sga = SpacegroupAnalyzer(struc, symprec=SYMPREC, angle_tolerance=ANGLE_TOL)
        struc = sga.get_primitive_standard_structure()

        ### Assign output name, tweak to avoid overwrite
        out_file_name = file_name.replace('.vasp','').replace('.cif','') + target_suffix
        if os.path.exists(out_file_name): 
            out_file_name = out_file_name.replace(target_suffix, f'_prim.{target_suffix}')
        print(f'{file_name}  ==>  {out_file_name}')

        ### Write structure to file
        struc.to(fmt='poscar', filename=out_file_name)
            
if __name__ == "__main__":
    main()



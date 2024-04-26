"""
@author: Kyle Miller
Usage: python convert_struc_cif.py struc1 struc2
"""

from pymatgen.core.structure import Structure
import sys
import os

def main():
    file_names = sys.argv[1:]
    for file_name in file_names:
        target_suffix = '.cif'

        ### Parse structure
        struc = Structure.from_file(file_name)

        ### Assign output name, tweak to avoid overwrite
        out_file_name = file_name.replace('.vasp','').replace('.cif','') + target_suffix
        if os.path.exists(out_file_name): 
            out_file_name = out_file_name.replace(target_suffix, f'_conv.{target_suffix}')
        print(f'{file_name}  ==>  {out_file_name}')

        ### Write structure to file
        struc.to(fmt='cif', filename=out_file_name)
            
if __name__ == "__main__":
    main()

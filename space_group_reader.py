from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.core.structure import Structure
import sys

"""
Usage: python space_group_reader.py struc1.cif struc2.vasp ...
"""

def main():
    files = sys.argv[1:]
    for file in files:
    
        struc = Structure.from_file(file)

        print("Prec \tAngle_tol \tSG Sym\tSG Num")
        for tol, angle_tol in [(0.000001, 0.01), (0.00001, 0.1), (0.0001, 0.1), (0.0001, 1), (0.001, 2), (0.01, 5), (0.1, 5), (1,5)]:
            sga = SpacegroupAnalyzer(struc, symprec=tol, angle_tolerance=angle_tol)
            sgSym = sga.get_space_group_symbol()
            sgNum = sga.get_space_group_number()
            print("{}\t{}\t{}\t{}".format(str(tol), str(angle_tol), sgSym, str(sgNum)))

if __name__ == "__main__":
    main()

# https://biopython.org/docs/1.75/api/Bio.SeqIO.html
# https://ena-docs.readthedocs.io/en/latest/submit/fileprep/flat-file-example.html
# https://github.com/biopython/biopython/blob/master/Bio/GenBank/Scanner.py#L1024
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1897316/
# https://learnbyexample.github.io/py_regular_expressions/regex-module.html

# Run me like so:
#   $ python dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl

import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

# infile = "data/Dfam.embl"
# outfile = "data/Dfam_corrected.embl"

def process_id_line(line):
    nb = line.count(";")

    # 2, 3 or 6 is correct according to
    # https://github.com/biopython/biopython/blob/master/Bio/GenBank/Scanner.py#L1024
    if nb in (2, 3, 6):
        return line

    # in the latest embl file format, the ID line must have 6 semicolons
    # convert 5 semicolons to 6
    if nb == 5:
        strfind = "^ID   (.*); (circular|linear|unspecified); (.*); (.*); (.*); ([0-9]+) BP\.$"
        x = re.search(strfind, line)
        if x is None:
            raise ValueError(f"ID line format is incorrect. Expected is \"{strfind}\", but encontered: {line}")
        
        return re.sub(strfind, "ID   \g<1>; SV 1; \g<2>; \g<3>; \g<4>; \g<5>; \g<6> BP.", line)
    
    raise ValueError(f"Number of semicolon(;) is incorrect. Expected is 2, 3, 5 or 6, but encontered: {nb}")

print("Starting.\nConverting EMBL file downloaded from DFAM to CORRECT EMBL file format.")
print("infile=", infile)
print("outfile=", outfile)

reader = open(infile, "r")
writer = open(outfile, "w")

for line in reader:
    if line[:2] == "ID":
        line = process_id_line(line)

    writer.write(line)

reader.close()
writer.close()

print("Finished.")
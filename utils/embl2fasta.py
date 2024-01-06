# from Bio import SeqIO

# records = SeqIO.parse("data/Dfam.embl", "embl")
# count = SeqIO.write(records, "data/Dfam.embl.fasta", "fasta")
# print("Converted %i records" % count)

from Bio import SeqIO
import sys

# Run me like so:
#   $ python utils/embl2fasta.py data/Dfam_corrected.embl embl data/Dfam.embl.fasta fasta

infile = sys.argv[1]
intype = sys.argv[2]
outfile = sys.argv[3]
outtype = sys.argv[4]

SeqIO.convert(infile, intype, outfile, outtype)
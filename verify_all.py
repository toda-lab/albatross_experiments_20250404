import sys
import os

# Usage: find log/1/albatross+zalbatross -name "stdout" | python verify_all.py

SCRIPTDIR="." # directory in which python script files are put.
CNFDIR="./data" # directory in which CNF files are put.

for line in sys.stdin:
    li = line.strip("\n").split("/")
    if li[-1] != "stdout":
        raise Exception
    if li[-2][-1] != "f" or\
        li[-2][-2] != "n" or\
        li[-2][-3] != "c" or\
        li[-2][-4] != ".":
        raise Exception
    cnf   = li[-2]
    proof = line.strip("\n")
    cmd   = f"python {SCRIPTDIR}/verifier.py {CNFDIR}/{cnf} {proof} "
    os.system(cmd)

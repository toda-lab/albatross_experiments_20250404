from argparse import ArgumentParser

from pysat.formula import CNF
from pysat.solvers import Solver

from hit import HitMgr

# Usage: python verifier.py cnf-file proof-file
# proof-file is a file consisting of clauses derived by complementary encoding.

parser = ArgumentParser()
parser.add_argument("arg1", help="dimacs cnf file")
parser.add_argument("arg2", help="proof file")
cnffile   = parser.parse_args().arg1
prooffile = parser.parse_args().arg2

assign  = []
derived = []
with open(prooffile) as f:
    for line in f.readlines():
        if line[0] == "s":
            li = line.strip("\n").split(" ")
            assert len(li) == 2, f"{line}"
            if li[1] != "UNSATISFIABLE":
                print("[warning] skipped because of satisfiable instance")
                exit()
        if line[0] != "c":
            continue
        li = line.strip("\n").split(":")
        if len(li) != 2:
            continue
        h = li[0].split(" ")
        b = li[1].split(" ")
        h = [x for x in h if x!=""]
        b = [x for x in b if x!=""]
        if len(h) == 2 and h[1] == "assign":
            assign.append(tuple(map(int,b)))
        if len(h) == 2 and h[1] == "derived":
            derived.append(tuple(map(int,b)))
L = len(assign)
assert L > 0
assert len(derived) == L

N = 0
M = 0
T = 0
F = []
with open(cnffile) as f:
    for line in f.readlines():
        if line[0] != "c":
            continue
        li = line.strip("\n").split(":")
        if len(li) != 2:
            continue
        h = li[0].split(" ")
        h = [x for x in h if x!=""]
        b = li[1].split(" ")
        b = [x for x in b if x!=""]
        if len(h) == 2 and h[1] == "n":
            N = int(b[0])
        if len(h) == 2 and h[1] == "m":
            M = int(b[0])
        if len(h) == 2 and h[1] == "t":
            T = int(b[0])
        if len(h) == 2 and h[1] == "edge":
            F.append(tuple(map(int,b)))
M = len(F)
assert N > 0
assert M > 0
assert T > 0

mgr = HitMgr(CECD_DISABLE=False,N=N,M=M,F=F,T=T)

# Verification of each R-derived clause
print(f"Verifying {cnffile} {prooffile}")
count = 0
for i in range(L):
    tset = set([mgr.dec(abs(j))[1] for j in derived[i]])
    fset = set([mgr.dec(abs(j))[1] for j in assign[i] if j > 0 and mgr.dec(abs(j))[0]=="f"])
    if len(fset) < T:
        print(f"[failed] {i}: packing size {len(fset)} < {T}")
        count += 1
    for j in fset:
        for k in fset:
            if j >= k:
                continue
            if (set(F[j])-tset) & (set(F[k])-tset) != set():
                print(f"[failed] {i}: packing condition broken\n"+\
                    f"{j}-th edge: {F[j]}\n"+\
                    f"{k}-th edge: {F[k]}\n"+\
                    f"certificate: {tset}")
                count +=1
    if count > 0:
        print(f"[failed] {i}: {' '.join(map(str,derived[i]))}")
        break
if count > 0:
    print(f"[failed] the 1st-stage verification")
else:
    print(f"[passed] the 1st-stage verification")


# Verification of the conjunction of all clauses in the precondition part,
# postcondition part, and all R-derived clauses.
clause_list = derived + [tup for tup in mgr.clause_list\
    if mgr.enc("y") not in tup] + [(mgr.enc("y"),)]
with Solver(bootstrap_with=CNF(from_clauses=clause_list)) as solver:
    if solver.solve():
        print(f"[failed] the 2nd-stage verification")
    else:
        print(f"[passed] the 2nd-stage verification")

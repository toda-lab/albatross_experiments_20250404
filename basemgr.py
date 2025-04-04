from typing import Iterable

class BaseMgr:
    """Manager for encoding/decoding in DIMACS CNF"""
    def __init__(self):
        self.index_dic = {}
        """dictionary to lookup variable index"""
        self.rev_list  = []
        """list for reverse lookup"""
        self.clause_list = []
        """list of clauses"""

    def tostr(self,lit):
        def tostr_main(sig, args):
            if len(args) == 0:
                return sig
            else:
                return f"{sig}(" +\
                    str(args).translate(str.maketrans({'(':'',')':'',' ':''}))\
                    + ")"
        v = abs(lit)
        key = self.dec(v)
        return tostr_main(key[0],key[1:]) if lit > 0\
                    else "~" + tostr_main(key[0],key[1:])

    def newvar(self, *args):
        """underscore is preserved to designate anonymous variables."""
        return self.enc("_", *args)

    def enc(self, *args):
        key = tuple(args)
        if key not in self.index_dic:
            self.rev_list.append(key)
            self.index_dic[key] = len(self.rev_list)
        return self.index_dic[key]

    def dec(self, v):
        if v <= 0:
            raise ValueError
        return self.rev_list[v-1]

    def add_clause(self, li):
        assert(len(li)>0)
        assert(0 not in li)
        self.clause_list.append(tuple(li))

    def print_cnf(self):
        print(f"p cnf {len(self.rev_list)} {len(self.clause_list)}")
        for tup in self.clause_list:
            print(" ".join(["c"] + [self.tostr(x) for x in tup]))
            print(" ".join(map(str,tup)) +" 0")

    def at_most_r_sinz(self, x: Iterable[int], r: int):
        """Computes at-most-r constraint of Sinz.

        See also TAOCP Vol.4, Fascicle 6, p.8.
        """
        if len(x) == 0:
            raise Exception
        x = (0,) + tuple(x)
        n = len(x)-1
        if r >= n or r <= 0:
            raise Exception
        key = len(self.rev_list)
        """NOTE:used to avoid collision of variables over multiple calls of
        this method"""

        def s(k: int, i: int) -> int:
            if k in range(n,2*n) and i ==1:
                assert(0 != k-n+1)
                return x[k-n+1]
            return self.newvar(k,i,key) # key added to avoid collision
        
        res = []
        for j in range(1,n-r):
            for k in range(1,r+1):
                li = []
                if k != 0:
                    li.append(-s(k,j))
                li.append(s(k,j+1))
                res.append(li)
        for j in range(1,n-r+1):
            for k in range(0,r+1):
                li = [-x[j+k]]
                if k != 0:
                    li.append(-s(k,j))
                if k != r:
                    li.append(s(k+1,j))
                res.append(li)
        assert(len(res) == (n-r-1)*r+(n-r)*(r+1))
        return res

    def at_most_r_bailleux_boufkhad(self, x: Iterable[int], r: int):
        """Computes at-most-r constraint of O.Bailleux and Y.Boufkhad.

        See also TAOCP Vol.4, Fascicle 6, p.8.
        """
        if len(x) == 0:
            raise Exception
        x = (0,) + tuple(x)
        n = len(x)-1
        if r >= n:
            return []
        if r <= 0:
            return [[-v] for v in x[1:]]
        key = len(self.rev_list)
        """NOTE:used to avoid collision of variables over multiple calls of
        this method"""

        def b(k: int, i: int) -> int:
            assert(i != 0)
            assert(i != r+1)
            if k in range(n,2*n) and i ==1:
                assert(0 != k-n+1)
                return x[k-n+1]
            return self.newvar(k,i,key) # key added to avoid collision

        t = [0]*(2*n)
        for k in range(n,2*n):
            t[k] = 1
        for k in range(n-1,0,-1):
            t[k] = min(r,t[2*k]+t[2*k+1])
        res = []
        for k in range(2,n):
            for i in range(t[2*k]+1):
                for j in range(t[2*k+1]+1):
                    if not 1 <= i+j <= t[k]+1:
                        continue
                    li = []
                    if i != 0:
                        li.append(-b(2*k,i))
                    if j != 0:
                        li.append(-b(2*k+1,j))
                    if i+j != r+1:
                        li.append(b(k,i+j))
                    res.append(li)
        for i in range(t[2]+1):
            for j in range(t[3]+1):
                if i+j != r+1:
                    continue
                li = []
                if i != 0:
                    li.append(-b(2,i))
                if j != 0:
                    li.append(-b(3,j))
                res.append(li)
        return res

    def at_least_r_sinz(self, x: Iterable[int], r: int):
        return self.at_most_r_sinz([-v for v in x],len(x)-r)

    def at_least_r_bailleux_boufkhad(self, x: Iterable[int], r: int):
        return self.at_most_r_bailleux_boufkhad([-v for v in x],len(x)-r)


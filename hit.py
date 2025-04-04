from basemgr import BaseMgr

class HitMgr(BaseMgr):
    def __init__(self,CECD_DISABLE,N,M,F,T):
        super().__init__()
        self.CECD_DISABLE = CECD_DISABLE
        self.N = N
        self.M = M
        self.F = F
        self.T = T
        for i in range(self.N):
            li = [i for j in range(self.M) if i in self.F[j]]
            if len(li) == 0:
                raise Exception("isolated vertex found!")
        self._make_cnf()
        if self.CECD_DISABLE:
            self.add_clause([self.ency()])

    def _make_cnf(self):
        # precondition
        for j in range(self.M):
            li = [self.encx(i) for i  in self.F[j]]
            self.add_clause(li)
        #for i in range(self.N):
        #    li = [-self.encx(i)] +\
        #        [self.encx(i,j) for j in range(self.M) if i in self.F[j]]
        #    assert len(li) > 0 # assume no isolated vertex exists.
        #    self.add_clause(li)
        #for i in range(self.N):
        #    for k in range(i+1,self.N):
        #        for j in range(self.M):
        #            if (i not in self.F[j]) or (k not in self.F[j]):
        #                continue
        #            li = [-self.encx(i),-self.encx(k),-self.encx(i,j),-self.encx(k,j)]
        #            self.add_clause(li)
        # postcondition
        #for li in self.at_most_r_sinz(\
        for li in self.at_most_r_bailleux_boufkhad(\
            [self.encx(i) for i in range(self.N)], self.T-1):
            self.add_clause([-self.ency()]+li)
        # complement
        #for li in self.at_least_r_sinz(\
        for li in self.at_least_r_bailleux_boufkhad(\
            [self.encf(j) for j in range(self.M)], self.T):
            self.add_clause([self.ency()]+li)
        for i in range(self.N):
            li = [self.ency(),-self.enct(i),-self.encx(i)]
            self.add_clause(li)
        for i in range(self.N):
            for j in range(self.M):
                for k in range(j+1,self.M):
                    if (i not in self.F[j]) or (i not in self.F[k]):
                        continue
                    li = [self.ency(),self.enct(i),-self.encf(j),-self.encf(k)]
                    self.add_clause(li)
        for i in range(self.N):
            li = [self.ency(),-self.enct(i)] +\
                [self.encw(i,j,k) for j in range(self.M)\
                                    for k in range(j+1,self.M)\
                                        if i in self.F[j] and i in self.F[k]] 
            self.add_clause(li)
            for j in range(self.M):
                for k in range(j+1,self.M):
                    if (i not in self.F[j]) or (i not in self.F[k]):
                        continue
                    li = [self.ency(),-self.enct(i)] +\
                        [-self.encw(i,j,k),self.encf(j)]
                    self.add_clause(li)
                    li = [self.ency(),-self.enct(i)] +\
                        [-self.encw(i,j,k),self.encf(k)]
                    self.add_clause(li)

    def encx(self, *args):
        assert 1 <= len(args) <= 2
        assert 0 <= args[0] < self.N, f"args[0]"
        if len(args)==2:
            assert 0 <= args[1] < self.M, f"args[1]"
        return self.enc("x",*args)

    def ency(self):
        return self.enc("y")

    def encf(self,*args):
        assert len(args)==1, f"{args}"
        assert 0 <= args[0] < self.M, f"args[0]"
        return self.enc("f",*args)

    def enct(self,*args):
        assert len(args)==1, f"{args}"
        assert 0 <= args[0] < self.N, f"args[0]"
        return self.enc("t",*args)

    def encw(self,*args):
        assert len(args)==3, f"{args}"
        assert 0 <= args[0] < self.N, f"args[0]"
        assert 0 <= args[1] < self.M, f"args[1]"
        assert 0 <= args[2] < self.M, f"args[2]"
        assert args[1] < args[2], f"args"
        return self.enc("w",*args)

    def print_cnf(self):
        for v in self.index_dic.values():
            key = self.dec(v)
            if key[0] == "x":
                print(f"c IVAR {v} 0 {self.tostr(v)}")
            elif key[0] == "y":
                print(f"c OVAR {v} 0 {self.tostr(v)}")
            elif key[0] in ["t", "f"]:
                print(f"c WVAR {v} 0 {self.tostr(v)}")
        super().print_cnf()

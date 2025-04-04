from basemgr import BaseMgr

import random
from pyunigen import Sampler

def test_at_most_r_bailleux_boufkhad():
    mgr = BaseMgr()
    nof_samples = 100
    n = 10
    r = random.randint(0,n)

    c = Sampler()
    for li in mgr.at_most_r_bailleux_boufkhad(\
        [mgr.enc("x",i) for i in range(n)], r):
        c.add_clause(li)
    cells, hashes, samples = c.sample(num=nof_samples,\
        sampling_set=[mgr.enc("x",i) for i in range(n)])
    for sol in samples:
        count = 0
        for x in sol:
           if x > 0:
                count = count+1
        assert count <= r

def test_at_least_r_bailleux_boufkhad():
    mgr = BaseMgr()
    nof_samples = 10
    n = 10
    r = random.randint(0,n)

    c = Sampler()
    for li in mgr.at_least_r_bailleux_boufkhad(\
        [mgr.enc("x",i) for i in range(n)], r):
        c.add_clause(li)
    cells, hashes, samples = c.sample(num=nof_samples,\
        sampling_set=[mgr.enc("x",i) for i in range(n)])
    for sol in samples:
        count = 0
        for x in sol:
           if x > 0:
                count = count+1
        assert count >= r

def test_exact_r_bailleux_boufkhad():
    mgr = BaseMgr()
    nof_samples = 10
    n = 10
    r = random.randint(0,n)

    c = Sampler()
    for li in mgr.at_least_r_bailleux_boufkhad(\
        [mgr.enc("x",i) for i in range(n)], r):
        c.add_clause(li)
    for li in mgr.at_most_r_bailleux_boufkhad(\
        [mgr.enc("x",i) for i in range(n)], r):
        c.add_clause(li)
    cells, hashes, samples = c.sample(num=nof_samples,\
        sampling_set=[mgr.enc("x",i) for i in range(n)])
    for sol in samples:
        count = 0
        for x in sol:
           if x > 0:
                count = count+1
        assert count == r


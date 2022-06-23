import time
from functools import lru_cache
import numpy as np


@lru_cache
def rand_array(nbytes):
    return np.random.rand(nbytes // 8)


def stat_ts(ts):
    t = np.array(ts)
    return {
        "mean(s)": float(t.mean()),
        "std(s)": float(t.std()),
        "time points(s)": ts
    }


def timeit(f, n=10):
    ts = []
    for i in range(n):
        t0 = time.perf_counter()
        f()
        ts.append(time.perf_counter() - t0)
    return stat_ts(ts)

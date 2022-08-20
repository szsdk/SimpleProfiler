import time
from functools import lru_cache
import numpy as np
import string
import random


def rand_str(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


@lru_cache
def rand_array(nbytes):
    return np.random.rand(nbytes // 8)


def stat_ts(ts):
    t = np.array(ts)
    return {
        "mean (s)": float(t.mean()),
        "std (s)": float(t.std()),
        "time points (s)": ts
    }


def timeit(f, n=10, time_points=False):
    ts = []
    for i in range(n):
        t0 = time.perf_counter()
        f()
        ts.append(time.perf_counter() - t0)
    ans = stat_ts(ts)
    if not time_points:
        ans.pop("time points (s)")
    return ans

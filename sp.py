import platform
import cpuinfo
import numpy as np
import toml
from utils import timeit, rand_array


def system_info():
    uname = platform.uname()
    return {
        "System": uname.system,
        "Node Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor,
    }


def np_copy(nbytes):
    a = rand_array(nbytes)
    b = a.copy()
    info = timeit(lambda: np.copyto(b, a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info['mean(s)']
    info.pop("time points(s)")
    return info


def np_float_sum(nbytes):
    a = rand_array(nbytes)
    info = timeit(lambda: np.sum(a), n=7)
    info["array size"] = len(a)
    info["sum speed (element/s)"] = len(a) / info['mean(s)']
    info.pop("time points(s)")
    return info


result = dict()
result["system"] = system_info()
result["cpu"] = cpuinfo.get_cpu_info()
result["numpy copy (small)"] = np_copy(1 << 18)
result["numpy copy (large)"] = np_copy(1 << 27)
result["numpy float sum (small)"] = np_float_sum(1 << 18)
result["numpy float sum (large)"] = np_float_sum(1 << 27)
print(toml.dumps(result))

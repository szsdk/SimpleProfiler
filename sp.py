from pathlib import Path
import tempfile
import platform
import cpuinfo
import numpy as np
import toml
import utils
import h5py


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
    a = utils.rand_array(nbytes)
    b = a.copy()
    info = utils.timeit(lambda: np.copyto(b, a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info['mean(s)']
    info.pop("time points(s)")
    return info


def np_float_sum(nbytes):
    a = utils.rand_array(nbytes)
    info = utils.timeit(lambda: np.sum(a), n=7)
    info["array size"] = len(a)
    info["sum speed (G element/s)"] = len(a) * 1e-9 / info['mean(s)']
    info.pop("time points(s)")
    return info


def h5_IO(nbytes):
    a = utils.rand_array(nbytes)
    result = {
        "array size (MB)": nbytes * 1e-6
    }
    with tempfile.NamedTemporaryFile(dir=Path(), suffix=".h5") as f:
        with h5py.File(f.name, "w") as fp:
            info = utils.timeit(lambda: fp.create_dataset(utils.rand_str(), data=a), n=10)
            info.pop("time points(s)")
        result["writing speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
        with h5py.File(f.name, "r") as fp:
            keys = iter(fp.keys())
            info = utils.timeit(lambda: fp[next(keys)][...], n=10)
            info.pop("time points(s)")
        result["reading speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
    return result



result = dict()
result["system"] = system_info()
result["cpu"] = cpuinfo.get_cpu_info()
result["numpy copy (small)"] = np_copy(1 << 18)
result["numpy copy (large)"] = np_copy(1 << 27)
result["numpy float sum (small)"] = np_float_sum(1 << 18)
result["numpy float sum (large)"] = np_float_sum(1 << 27)
result["HDF5 IO (small)"] = h5_IO(1 << 18)
result["HDF5 IO (large)"] = h5_IO(1 << 27)
print(toml.dumps(result))

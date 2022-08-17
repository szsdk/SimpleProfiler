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
    return info


def np_float_sum(nbytes):
    a = utils.rand_array(nbytes)
    info = utils.timeit(lambda: np.sum(a), n=7)
    info["array size"] = len(a)
    info["sum speed (G element/s)"] = len(a) * 1e-9 / info['mean(s)']
    return info


def h5_IO(nbytes):
    a = utils.rand_array(nbytes)
    result = {"array size (MB)": nbytes * 1e-6}
    with tempfile.NamedTemporaryFile(dir=Path(), suffix=".h5") as f:
        with h5py.File(f.name, "w") as fp:
            info = utils.timeit(
                lambda: fp.create_dataset(utils.rand_str(), data=a), n=10)
        result["writing speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
        with h5py.File(f.name, "r") as fp:
            keys = iter(fp.keys())
            info = utils.timeit(lambda: fp[next(keys)][...], n=10)
        result["reading speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
    return result


def prime_benchmark(nb_primes, method: str):
    if method == "pybind11":
        from sci_benchmark.pybind11_func import primes
    elif method == "cython":
        from sci_benchmark.cython_func import primes
    elif method == "numba":
        from sci_benchmark.numba_func import primes
        primes(20)  # warmup

    info = utils.timeit(lambda: primes(nb_primes))
    info["number of primes"] = nb_primes
    info["method"] = method
    return info


result = dict()
result["system"] = system_info()
result["cpu"] = cpuinfo.get_cpu_info()
result["numpy copy (small)"] = np_copy(1 << 18)
result["numpy copy (large)"] = np_copy(1 << 27)
result["numpy float sum (small)"] = np_float_sum(1 << 18)
result["numpy float sum (large)"] = np_float_sum(1 << 27)
result["HDF5 IO (small)"] = h5_IO(1 << 18)
result["HDF5 IO (large)"] = h5_IO(1 << 27)
result["pybind11 primes"] = prime_benchmark(300000, "pybind11")
result["cython primes"] = prime_benchmark(300000, "cython")
result["numba primes"] = prime_benchmark(300000, "numba")
print(toml.dumps(result))

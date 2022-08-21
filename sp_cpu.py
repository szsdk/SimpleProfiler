from pathlib import Path
import tempfile
import logging

import numpy as np

import utils

def cpu_info():
    try:
        import cpuinfo
    except ImportError:
        logging.warning("Cannot import cpuinfo.")
        return
    return cpuinfo.get_cpu_info()


def system_info():
    import platform
    from datetime import datetime
    uname = platform.uname()
    return {
        "time": datetime.now(),
        "system": uname.system,
        "node Name": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
    }


def np_copy(nbytes):
    a = utils.rand_array(nbytes)
    b = a.copy()
    info = utils.timeit(lambda: np.copyto(b, a), n=7)
    info["memory size (MB)"] = a.nbytes / (1 << 20)
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean (s)"]
    return info


def np_float_sum(nbytes):
    a = utils.rand_array(nbytes)
    info = utils.timeit(lambda: np.sum(a), n=7)
    info["array size"] = len(a)
    info["sum speed (G element/s)"] = len(a) * 1e-9 / info["mean (s)"]
    return info


def h5_IO(nbytes):
    try:
        import h5py
    except ImportError:
        logging.warning("Cannot import h5py")
        return
    a = utils.rand_array(nbytes)
    result = {"array size (MB)": nbytes * 1e-6}
    with tempfile.NamedTemporaryFile(dir=Path(), suffix=".h5") as f:
        with h5py.File(f.name, "w") as fp:
            info = utils.timeit(
                lambda: fp.create_dataset(utils.rand_str(), data=a), n=10)
        result["writing speed (GB/s)"] = nbytes * 1e-9 / info["mean (s)"]
        with h5py.File(f.name, "r") as fp:
            keys = iter(fp.keys())
            info = utils.timeit(lambda: fp[next(keys)][...], n=10)
        result["reading speed (GB/s)"] = nbytes * 1e-9 / info["mean (s)"]
    return result


def prime_benchmark(nb_primes, method: str):
    try:
        if method == "pybind11":
            from sci_benchmark.pybind11_func import primes
        elif method == "cython":
            from sci_benchmark.cython_func import primes
        elif method == "numba":
            from sci_benchmark.numba_func import primes

            primes(20)  # warmup
    except ImportError:
        logging.warning(f"Cannot import sci_benchmark {method}")
        return

    info = utils.timeit(lambda: primes(nb_primes))
    info["number of primes"] = nb_primes
    info["method"] = method
    return info

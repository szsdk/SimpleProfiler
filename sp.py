import logging
from rich.logging import RichHandler
from rich.progress import Progress
from pathlib import Path
import tempfile
import platform
import numpy as np
import toml
import utils


FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

def cpu_info():
    try:
        import cpuinfo
    except ImportError:
        logging.warning("Cannot import cpuinfo.")
    return cpuinfo.get_cpu_info()


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
        result["writing speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
        with h5py.File(f.name, "r") as fp:
            keys = iter(fp.keys())
            info = utils.timeit(lambda: fp[next(keys)][...], n=10)
        result["reading speed (GB/s)"] = nbytes * 1e-9 / info['mean(s)']
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


result = dict()
with Progress() as progress:
    task1 = progress.add_task("", total=None)
    progress.update(task1, advance=1, description="system info")
    result["system"] = system_info()
    progress.update(task1, advance=1, description="cpu info")
    result["cpu"] = cpu_info()
    progress.update(task1, advance=1, description="numpy copy (small)")
    result["numpy copy (small)"] = np_copy(1 << 18)
    progress.update(task1, advance=1, description="numpy copy (large)")
    result["numpy copy (large)"] = np_copy(1 << 27)
    progress.update(task1, advance=1, description="numpy float sum (small)")
    result["numpy float sum (small)"] = np_float_sum(1 << 18)
    progress.update(task1, advance=1, description="numpy float sum (large)")
    result["numpy float sum (large)"] = np_float_sum(1 << 27)
    progress.update(task1, advance=1, description="HDF5 IO (small)")
    result["HDF5 IO (small)"] = h5_IO(1 << 18)
    progress.update(task1, advance=1, description="HDF5 IO (large)")
    result["HDF5 IO (large)"] = h5_IO(1 << 27)
    progress.update(task1, advance=1, description="pybind11 primes")
    result["pybind11 primes"] = prime_benchmark(300000, "pybind11")
    progress.update(task1, advance=1, description="cython primes")
    result["cython primes"] = prime_benchmark(300000, "cython")
    progress.update(task1, advance=1, description="numba primes")
    result["numba primes"] = prime_benchmark(300000, "numba")
print(toml.dumps(result))

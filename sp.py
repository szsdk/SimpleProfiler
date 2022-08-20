from pathlib import Path
import tempfile
import logging
from datetime import datetime

from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
import platform
import numpy as np
import toml
import click

import utils

logging.basicConfig(
    level="INFO", format= "%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

def cpu_info():
    try:
        import cpuinfo
    except ImportError:
        logging.warning("Cannot import cpuinfo.")
        return
    return cpuinfo.get_cpu_info()


def system_info():
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
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean(s)"]
    return info


def np_float_sum(nbytes):
    a = utils.rand_array(nbytes)
    info = utils.timeit(lambda: np.sum(a), n=7)
    info["array size"] = len(a)
    info["sum speed (G element/s)"] = len(a) * 1e-9 / info["mean(s)"]
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
                lambda: fp.create_dataset(utils.rand_str(), data=a), n=10
            )
        result["writing speed (GB/s)"] = nbytes * 1e-9 / info["mean(s)"]
        with h5py.File(f.name, "r") as fp:
            keys = iter(fp.keys())
            info = utils.timeit(lambda: fp[next(keys)][...], n=10)
        result["reading speed (GB/s)"] = nbytes * 1e-9 / info["mean(s)"]
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


@click.command()
@click.option("--no-log", is_flag=True, default=True)
def main(no_log):
    if not no_log:
        logging.disable()
    result = dict()
    result["system"] = system_info()
    logging.info("system information")
    result["cpu"] = cpu_info()
    logging.info("cpu information")
    logging.info("numpy array (small) in memory copy")
    result["numpy copy (small)"] = np_copy(1 << 18)
    logging.info("numpy array (large) in memory copy")
    result["numpy copy (large)"] = np_copy(1 << 27)
    logging.info("sum of a samll numpy float array")
    result["numpy float sum (small)"] = np_float_sum(1 << 18)
    logging.info("sum of a large numpy float array")
    result["numpy float sum (large)"] = np_float_sum(1 << 27)
    logging.info("HDF5 IO (small)")
    result["HDF5 IO (small)"] = h5_IO(1 << 18)
    logging.info("HDF5 IO (large)")
    result["HDF5 IO (large)"] = h5_IO(1 << 27)
    logging.info("primes (pybind11)")
    result["pybind11 primes"] = prime_benchmark(300000, "pybind11")
    logging.info("primes (cython)")
    result["cython primes"] = prime_benchmark(300000, "cython")
    logging.info("primes (numba)")
    result["numba primes"] = prime_benchmark(300000, "numba")

    console = Console()
    syntax = Syntax(toml.dumps(result), "toml", background_color="default")
    console.print(syntax)

if __name__ == "__main__":
    main()

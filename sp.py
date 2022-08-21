import logging
import math

from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from rich.style import Style
from rich.table import Table


import toml
import click



logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

_to_super = dict(zip("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))


def pretty_float(f: float) -> str:
    """
    Parameters
    ----------
    f : float
        The input float number.

    Returns
    -------
    s : str
        A string in the form of `f"{m:.4f} × 10{s_exp}"` for a too large or too small `f`.
    """
    if f == 0:
        return "0"
    exponet = int(math.floor(math.log10(f)))
    if -2 < exponet <= 3:
        return f"{f:.4f}"
    m = f * 10 ** (-exponet)
    s_exp = "".join([_to_super[i] for i in str(exponet)])
    return f"{m:.4f} × 10{s_exp}"


def cuda_benchmark():
    try:
        import cupy as cp
    except ImportError:
        logging.warning("Cupy is not installed")
        return {}
    try:
        cp.cuda.runtime.getDeviceCount()
    except cp.cuda.runtime.CUDARuntimeError:
        logging.warning("No CUDA-capable device detected")
        return {}

    import sp_cuda as scu

    info = dict()
    logging.info("cuda runtime")
    info["cuda runtime"] = scu.get_cuda_runtime()
    logging.info("copy to a GPU device (cupy)")
    info["cupy copy to a device"] = scu.cp_copy_to_device(1 << 28)
    logging.info("copy from a GPU device (cupy)")
    info["cupy copy from a device"] = scu.cp_copy_from_device(1 << 28)
    logging.info("copy in a GPU device (cupy)")
    info["cupy copy in a device"] = scu.cp_copy_in_device(1 << 28)
    if cp.cuda.runtime.getDeviceCount() >= 2:
        logging.info("copy between devices (cupy)")
        info["cupy copy between devices"] = scu.cp_copy_between_device(1 << 28)
    logging.info("sum (cupy)")
    info["cupy sum (small)"] = scu.cp_sum(1 << 16)
    info["cupy sum (large)"] = scu.cp_sum(1 << 28)
    logging.info("SVD (cupy)")
    info["cupy svd (small)"] = scu.cp_svd(16)
    info["cupy svd (large)"] = scu.cp_svd(512)
    return info


def cpu_benchmark():
    import sp_cpu as scp

    info = dict()
    info["system"] = scp.system_info()
    logging.info("system information")
    info["cpu"] = scp.cpu_info()
    logging.info("cpu information")
    logging.info("numpy array (small) in memory copy")
    info["numpy copy (small)"] = scp.np_copy(1 << 18)
    logging.info("numpy array (large) in memory copy")
    info["numpy copy (large)"] = scp.np_copy(1 << 27)
    logging.info("sum of a samll numpy float array")
    info["numpy float sum (small)"] = scp.np_float_sum(1 << 18)
    logging.info("sum of a large numpy float array")
    info["numpy float sum (large)"] = scp.np_float_sum(1 << 27)
    logging.info("HDF5 IO (small)")
    info["HDF5 IO (small)"] = scp.h5_IO(1 << 18)
    logging.info("HDF5 IO (large)")
    info["HDF5 IO (large)"] = scp.h5_IO(1 << 27)
    logging.info("primes (pybind11)")
    info["pybind11 primes"] = scp.prime_benchmark(300000, "pybind11")
    logging.info("primes (cython)")
    info["cython primes"] = scp.prime_benchmark(300000, "cython")
    logging.info("primes (numba)")
    info["numba primes"] = scp.prime_benchmark(300000, "numba")
    return info


def concat_dict(ds):
    ans = {k: [] for k in ds[0].keys()}
    for d in ds:
        for k, v in ans.items():
            v.append(d[k])
    return ans


def sort_stat(nodes, stat, sort_by=None):
    info = dict()
    table = {}
    for k, v in stat.items():
        if len(set(v)) == 1:
            info[k] = v[0]
        else:
            table[k] = v
    if sort_by is None:
        table["node"] = nodes
    else:
        sb = table[sort_by]
        table["node"] = [i for _, i in sorted(zip(sb, nodes))]
        for k, v in table.items():
            table[k] = [i for _, i in sorted(zip(sb, v))]
    return info, table


@click.command()
@click.argument("results", nargs=-1)
@click.option("--highlight", default="_NONE_")
def stat(results, highlight):
    rs = [toml.load(r) for r in results]
    no_stats = {"cpu", "system", "cuda runtime"}
    keys = set(sum([list(r.keys()) for r in rs], []))
    keys -= no_stats

    # output_str = toml.dumps(result)
    console = Console()
    for k in sorted(keys):
        nodes = [r["system"]["node Name"] for r in rs if k in r]
        stat = concat_dict([r[k] for r in rs if k in r])

        sort_by = "mean (s)" if "mean (s)" in stat else None
        info, table = sort_stat(
            nodes, stat, sort_by=sort_by
        )
        console.print(
            Syntax(toml.dumps({k: info}), "toml", background_color="default"), end=""
        )

        tab = Table()
        for k in table.keys():
            # if k == "node":
            #     width = None
            # else:
            #     width = max(len(k), 4)
            width = None
            tab.add_column(k, width=width)
        for l in zip(*list(table.values())):
            if  highlight in l[-1]:
                style = Style(color="rgb(240,0,0)")
            else:
                style = Style.null()
            tab.add_row(*[pretty_float(i) if isinstance(i, float) else str(i) for i in l], style=style)
        console.print(tab)

@click.command()
@click.option("--no-log", is_flag=True, default=True)
@click.option("--output", "-O", type=str, default="")
def main(no_log, output):
    if not no_log:
        logging.disable()

    result = dict()
    result.update(cpu_benchmark())
    result.update(cuda_benchmark())

    output_str = toml.dumps(result)
    console = Console()
    syntax = Syntax(output_str, "toml", background_color="default")
    console.print(syntax)

    if output != "":
        with open(output, "w") as fp:
            print(output_str, file=fp, end="")


if __name__ == "__main__":
    stat()
    # main()

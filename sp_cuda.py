import time
import cupy as cp
import cupyx
from utils import timeit, rand_array


def get_cuda_runtime():
    info = dict()
    for line in str(cupyx.get_runtime_info()).splitlines():
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        info[k] = v
    return info


def cp_copy_to_device(nbytes):
    a = rand_array(nbytes)
    cp.array(a[:2])  # warm-up run
    info = timeit(lambda: cp.array(a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean (s)"]
    return info


def cp_copy_from_device(nbytes):
    a = cp.array(rand_array(nbytes))
    cp.asnumpy(a[:2])  # warm-up run
    info = timeit(lambda: cp.asnumpy(a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean (s)"]
    return info


def gpu_copy(dst, src):
    end_gpu = cp.cuda.Event()
    cp.copyto(dst, src)
    end_gpu.record()
    end_gpu.synchronize()


def cp_copy_in_device(nbytes):
    a = cp.array(rand_array(nbytes))
    b = cp.empty_like(a)
    info = timeit(lambda: gpu_copy(b, a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean (s)"]
    return info


def cp_copy_between_device(nbytes):
    with cp.cuda.Device(0):
        a = cp.array(rand_array(nbytes))
    with cp.cuda.Device(1):
        b = cp.empty_like(a)
    info = timeit(lambda: gpu_copy(b, a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean (s)"]
    return info


def cp_timeit(f, n=10, time_points=False):
    def _f():
        event = cp.cuda.stream.Event()
        event.record()
        event.synchronize()
        f()
        event = cp.cuda.stream.Event()
        event.record()
        event.synchronize()

    return timeit(_f, n, time_points=time_points)


def cp_svd(n, n_times=7):
    a = cp.random.rand(2, 2)
    cp.linalg.svd(a)
    a = cp.random.rand(n, n)
    info = {"array size": n}
    info.update(cp_timeit(lambda: cp.linalg.svd(a), n_times))
    return info


def cp_sum(nbytes, n_times=7):
    cp.sum(cp.empty(2))
    a = cp.array(rand_array(nbytes))
    size_GB = a.nbytes / (1 << 30)
    info = {"array size (GB)": size_GB}
    info.update(cp_timeit(lambda: cp.sum(a), n_times))
    info["speed (GB/s)"] = size_GB / info["mean (s)"]
    return info

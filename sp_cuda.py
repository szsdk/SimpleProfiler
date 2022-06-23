import cupy as cp
import cupyx
import toml
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
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean(s)"]
    info.pop("time points(s)")
    return info


def cp_copy_from_device(nbytes):
    a = cp.array(rand_array(nbytes))
    cp.asnumpy(a[:2])  # warm-up run
    info = timeit(lambda: cp.asnumpy(a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean(s)"]
    info.pop("time points(s)")
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
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean(s)"]
    info.pop("time points(s)")
    return info


def cp_copy_between_device(nbytes):
    with cp.cuda.Device(0):
        a = cp.array(rand_array(nbytes))
    with cp.cuda.Device(1):
        b = cp.empty_like(a)
    info = timeit(lambda: gpu_copy(b, a), n=7)
    info["memory size"] = f"{a.nbytes / (1 << 20)} MB"
    info["copy speed (GB/s)"] = a.nbytes / (1 << 30) / info["mean(s)"]
    info.pop("time points(s)")
    return info


info = dict()
info["cuda runtime"] = get_cuda_runtime()
info["cupy copy to devices"] = cp_copy_to_device(1 << 28)
info["cupy copy from devices"] = cp_copy_from_device(1 << 28)
info["cupy copy in devices"] = cp_copy_in_device(1 << 28)
info["cupy copy between devices"] = cp_copy_between_device(1 << 28)
print(toml.dumps(info))

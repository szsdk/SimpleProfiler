import cupyx
import toml

def get_cuda_runtime():
    info = dict()
    for line in str(cupyx.get_runtime_info()).splitlines():
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        info[k] = v
    return info

info = dict()
info["cuda runtime"] = get_cuda_runtime()
print(toml.dumps(info))

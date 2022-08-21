[system]
time = 2022-08-21T12:06:07.928275
system = "Linux"
"node Name" = "max-cssb017.desy.de"
release = "3.10.0-1160.71.1.el7.x86_64"
version = "#1 SMP Tue Jun 28 15:37:28 UTC 2022"
machine = "x86_64"
processor = "x86_64"

[cpu]
python_version = "3.8.13.final.0 (64 bit)"
cpuinfo_version = [ 8, 0, 0,]
cpuinfo_version_string = "8.0.0"
arch = "X86_64"
bits = 64
count = 48
arch_string_raw = "x86_64"
vendor_id_raw = "GenuineIntel"
brand_raw = "Intel(R) Xeon(R) Gold 6126 CPU @ 2.60GHz"
hz_advertised_friendly = "2.6000 GHz"
hz_actual_friendly = "3.2998 GHz"
hz_advertised = [ 2600000000, 0,]
hz_actual = [ 3299829000, 0,]
stepping = 4
model = 85
family = 6
flags = [ "3dnowprefetch", "abm", "acpi", "adx", "aes", "aperfmperf", "apic", "arat", "arch_capabilities", "arch_perfmon", "art", "avx", "avx2", "avx512bw", "avx512cd", "avx512dq", "avx512f", "avx512vl", "bmi1", "bmi2", "bts", "cat_l3", "cdp_l3", "clflush", "clflushopt", "clwb", "cmov", "constant_tsc", "cqm", "cqm_llc", "cqm_mbm_local", "cqm_mbm_total", "cqm_occup_llc", "cx16", "cx8", "dca", "de", "ds_cpl", "dtes64", "dtherm", "dts", "eagerfpu", "epb", "ept", "erms", "est", "f16c", "flexpriority", "flush_l1d", "fma", "fpu", "fsgsbase", "fxsr", "hle", "ht", "ibpb", "ibrs", "ida", "intel_ppin", "intel_pt", "intel_stibp", "invpcid", "invpcid_single", "lahf_lm", "lm", "mba", "mca", "mce", "md_clear", "mmx", "monitor", "movbe", "mpx", "msr", "mtrr", "nonstop_tsc", "nopl", "nx", "ospke", "pae", "pat", "pbe", "pcid", "pclmulqdq", "pdcm", "pdpe1gb", "pebs", "pge", "pku", "pln", "pni", "popcnt", "pse", "pse36", "pts", "rdrand", "rdseed", "rdt_a", "rdtscp", "rep_good", "rtm", "sdbg", "sep", "smap", "smep", "smx", "spec_ctrl", "ss", "ssbd", "sse", "sse2", "sse4_1", "sse4_2", "ssse3", "stibp", "syscall", "tm", "tm2", "tpr_shadow", "tsc", "tsc_adjust", "tsc_deadline_timer", "vme", "vmx", "vnmi", "vpid", "x2apic", "xgetbv1", "xsave", "xsavec", "xsaveopt", "xtopology", "xtpr",]
l3_cache_size = 20185088
l2_cache_size = 1048576
l1_data_cache_size = 32768
l1_instruction_cache_size = 32768

["numpy copy (small)"]
"mean (s)" = 1.1178132678781236e-5
"std (s)" = 5.011513837019554e-6
"memory size (MB)" = 0.25
"copy speed (GB/s)" = 21.840913148529467

["numpy copy (large)"]
"mean (s)" = 0.026373280079237053
"std (s)" = 4.602961172974751e-5
"memory size (MB)" = 128.0
"copy speed (GB/s)" = 4.739645566438624

["numpy float sum (small)"]
"mean (s)" = 3.434957138129643e-5
"std (s)" = 4.679396683218411e-5
"array size" = 32768
"sum speed (G element/s)" = 0.9539565904988963

["numpy float sum (large)"]
"mean (s)" = 0.010427683059658324
"std (s)" = 0.00014817220223253664
"array size" = 16777216
"sum speed (G element/s)" = 1.608911193792049

["HDF5 IO (small)"]
"array size (MB)" = 0.262144
"writing speed (GB/s)" = 0.7202630350684285
"reading speed (GB/s)" = 0.8985166189617461

["HDF5 IO (large)"]
"array size (MB)" = 134.217728
"writing speed (GB/s)" = 3.1393396298376257
"reading speed (GB/s)" = 2.7125911269788285

["pybind11 primes"]
"mean (s)" = 0.2675456145778298
"std (s)" = 0.0008004213826208625
"number of primes" = 300000
method = "pybind11"

["cython primes"]
"mean (s)" = 0.265121999476105
"std (s)" = 0.0010889179504643964
"number of primes" = 300000
method = "cython"

["numba primes"]
"mean (s)" = 0.43397085471078756
"std (s)" = 4.618149147343743e-5
"number of primes" = 300000
method = "numba"

import numpy as np
import numba


@numba.jit(boundscheck=False)
def primes(nb_primes):
    p = np.empty(nb_primes, np.int32)

    len_p = 0  # The current number of elements in p.
    n = 2
    upper = 3
    while len_p < nb_primes:
        if upper * upper < n:
            upper += 1
        # Is n prime?
        flag = True
        for i in p[:len_p]:
            if i > upper:
                break
            if n % i == 0:
                flag = False
                break
        # If no break occurred in the loop, we have a prime.
        if flag:
            p[len_p] = n
            len_p += 1
        n += 1
    return p

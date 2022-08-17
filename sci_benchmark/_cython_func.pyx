import cython
from libc.stdlib cimport malloc, free

__all__ = ["primes"]


@cython.wraparound(False)
@cython.cdivision(True)
@cython.boundscheck(False)
def primes(int nb_primes):
    cdef int n, i, len_p
    cdef int *p = <int *> malloc(nb_primes * sizeof(int))
    cdef int upper

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

    # Let's return the result in a python list:
    result_as_list  = [prime for prime in p[:len_p]]
    free(p)
    return result_as_list



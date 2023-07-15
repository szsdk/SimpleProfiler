#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

std::vector<int> primes(int nb_primes) {
    std::vector<int> p{};
    p.reserve(nb_primes);
    
    for(int n = 2, upper=3; p.size() < nb_primes; n++) {
        // Is n prime?
        bool flag = true;
        if (upper * upper < n) {
            upper ++;
        }
        // auto upper = (int)std::sqrt((double)n);
        for(auto &&i: p) {
            if (i > upper) {
                break;
            }
            if (n % i == 0) {
                flag = false;
                break;
            }
        }
        // If no break occurred in the loop, we have a prime.
        if (flag) {
            p.push_back(n);
        }
    }
    return p;
}

PYBIND11_MODULE(pybind11_func, m) {
    m.def("primes", &primes);
}

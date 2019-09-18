import gmpy2
from timeit import default_timer as timer

p = 1099511627791


def jacobi_bit_mpz(a, n):
    return gmpy2.legendre(a, n) > 0


def jacobi_bench():
    N = 10000000
    res = False
    start = timer()
    for i in range(N):
        res ^= jacobi_bit_mpz(i, p)
    end = timer()
    t = end - start
    print((t/N) * 10e9, " ns")


if __name__ == "__main__":
    jacobi_bench()

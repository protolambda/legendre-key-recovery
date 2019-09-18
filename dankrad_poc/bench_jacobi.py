import gmpy2
from timeit import default_timer as timer

p = 1099511627791


def jacobi_bit_mpz(a, n):
    return gmpy2.legendre(a, n) > 0


def jacobi_bench():
    N = 10000000
    res = False
    start = p // 2
    end = start + N
    start_time = timer()
    for i in range(start, end):
        res ^= jacobi_bit_mpz(i, p)
    end_time = timer()
    t = end_time - start_time
    print((t/N) * 10e9, " ns")


if __name__ == "__main__":
    jacobi_bench()

# Implements the algorithm described in https://eprint.iacr.org/2019/862.pdf

import gmpy2
import math
from timeit import default_timer as timer
from collections import defaultdict

# import numpy as np
# import matplotlib.pyplot as plt

p = gmpy2.next_prime(2**40)
print("p: ", p)
check_len = math.ceil(math.log2(p) * 2)
print("check len: ", check_len)

num_challenge_bits = 2 ** 20
legendre_evals = 0

def jacobi_bit_mpz(a, n):
    global legendre_evals
    legendre_evals += 1
    return gmpy2.legendre(a, n) > 0

# Create challenge
key = 3**1000 % p
print("key: ", key)
challenge = [jacobi_bit_mpz(key + x, p) for x in range(num_challenge_bits)]

# Solve challenge using Khovratovich algorithm
logN1 = math.ceil(math.log2(len(challenge)))

print("logN1: ", logN1)

N1 = len(challenge) - logN1

print("N1: ", N1)

def bitstring_to_int(a):
    return sum(x*2**i for i, x in enumerate(a))

fp_count = 0

def find_match(challenge, p):
    global fp_count
    # Create dictionary of all strings of logN1 bits in the challenge
    cdict = defaultdict(list)
    for i in range(N1):
        c = bitstring_to_int(challenge[i: i + logN1])
        cdict[c].append(i)

    # rowlen = math.ceil(2**(logN1/2))
    # a = [[len(cdict[i]) for i in range(j, j+rowlen)] for j in range(0, rowlen*rowlen, rowlen)]
    # plt.imshow(a, cmap='hot', interpolation='nearest')
    # plt.show()

    global matching_start
    matching_start = timer()
    current_key = 0
    expected_N2 = p // N1 // 2
    number_of_tries = 0
    while True:
        number_of_tries += 1
        # checking when to print with modulo is costly, do it every 2**16 times instead.
        if number_of_tries & ((1 << 16) - 1) == 0:
            print("Tried ", number_of_tries, "keys (expected = {0})".format(expected_N2))
        current_key = (current_key + N1) % p
        c = bitstring_to_int(jacobi_bit_mpz(current_key + x, p) for x in range(logN1))
        if c in cdict:
            for key_offset in cdict[c]:
                predicted_key = current_key - key_offset
                if all(jacobi_bit_mpz(predicted_key + x, p) == challenge[x] for x in range(check_len)):
                    return predicted_key
                fp_count += 1


start = timer()
legendre_evals = 0
assert find_match(challenge, p) == key
end = timer()
print("False positive count ", fp_count)
print("Total Time taken: {0:.2f} s".format(end - start))
print("Matching Time taken: {0:.2f} s".format(end - matching_start))
print("Total Legendre evaluations: {0}".format(legendre_evals))

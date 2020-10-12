import random
import time

from digitalSignature.Algorithms import solovay_strassen_test, modexp, gcd
from digitalSignature.types import Keys


def generate_keys(numberOfBits=256, confidence=32):
    t_start_prime = time.time()
    p = find_prime(numberOfBits, confidence) # простое
    # print("простое: ", p)
    # print("время поиска простого числа, dT: ", time.time() - t_start_prime)

    g = find_primitive_root(p) # первообразный корень p
    # print("первообразный корень: ", g)

    # закрытый ключ
    t_start_x = time.time()
    x = find_mutually_prime(p) # взаимно простое с (p-1) такое, что 1<x<p-1
    # print("время поиска x, dT: ", time.time() - t_start_x)
    # print("x: ", x)

    # открытый ключ
    t_start_y = time.time()
    y = modexp(g, x, p)
    # print("время вычисления y, dT: ", time.time() - t_start_y)
    # print("y: ", y)

    keys = Keys(p, g, x, y)

    return {'Keys': keys}



def find_mutually_prime(p):
    while (1):
        x = random.randint(2, p - 2)
        if gcd(p-1, x) == 1:
            return x

def find_primitive_root(p):
    if p == 2:
        return 1
    # делители p-1 - это 2 и (p-1)/2
    p1 = 2
    p2 = (p - 1) // 2

    while (1):
        g = random.randint(2, p - 1)
        if not (modexp(g, p1, p) == 1):
            if not modexp(g, p2, p) == 1:

                return g


def find_prime(numberOfBits, confidence):
    while (1):
        p = random.randint(2 ** (numberOfBits - 2), 2 ** (numberOfBits - 1))
        if p % 2 == 0:
            continue

        if not solovay_strassen_test(p, confidence):
            continue
        p = p * 2 + 1
        if solovay_strassen_test(p, confidence):
            return p


import random


def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


# Тест Соловея — Штрассена
def solovay_strassen_test(num, confidence):
    for i in range(confidence):
        a = random.randint(1, 18446744073709551616)  # сокращает время > чем в 2 раза

        if gcd(a, num) > 1:
            return False

        if not modexp(a, (num - 1) // 2, num) == jacobi(a, num) % num:
            return False

    return True


def jacobi(a, n):
    if a == 0:
        if n == 1:
            return 1
        else:
            return 0
    elif a == -1:
        if n % 2 == 0:
            return 1
        else:
            return -1
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        elif n % 8 == 3 or n % 8 == 5:
            return -1
    elif a >= n:
        return jacobi(a % n, n)
    elif a % 2 == 0:
        return jacobi(2, n) * jacobi(a // 2, n)
    else:
        if a % 4 == 3 and n % 4 == 3:
            return -1 * jacobi(n, a)
        else:
            return jacobi(n, a)

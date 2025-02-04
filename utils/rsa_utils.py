# utils/rsa_utils.py
import base64
import math
from math import gcd
from functools import reduce
import random


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError(f"模逆不存在 (gcd({a}, {m}) = {g})")
    return x % m


def chinese_remainder(n, a):
    sumsum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sumsum += a_i * modinv(p, n_i) * p
    return sumsum % prod


def continued_fraction(x, y):
    while y:
        a = x // y
        yield a
        x, y = y, x % y


def wiener_attack(e, n):
    cf = list(continued_fraction(e, n))
    for i in range(1, len(cf)):
        k, d = 0, 1
        for j in cf[:i][::-1]:
            k, d = d, d * j + k
        if d != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            if (n - phi + 1) % 2 == 0:
                p = ((n - phi + 1) // 2)
                q = n // p
                if p * q == n:
                    return d
    raise ValueError("维纳攻击失败")


def fermat_factorization(n):
    a = math.isqrt(n) + 1
    b2 = a * a - n
    while not math.isqrt(b2) ** 2 == b2:
        a += 1
        b2 = a * a - n
    b = math.isqrt(b2)
    return a - b, a + b


def pollards_p_1(n, B=10000):
    a = 2
    for p in sieve(B):
        a = pow(a, p, n)
    d = gcd(a - 1, n)
    if 1 < d < n: return d
    # 自动重试机制
    for _ in range(5):
        a = random.randint(2, n - 1)
        d = gcd(a, n)
        if d != 1:
            return d
        for _ in range(B):
            a = pow(a, random.randint(2, B), n)
            d = gcd(a - 1, n)
            if d != 1 and d != n:
                return d
    return None


def sieve(limit):
    is_prime = [True] * (limit + 1)
    for n in range(2, int(limit ** 0.5) + 1):
        if is_prime[n]:
            for i in range(n * n, limit + 1, n):
                is_prime[i] = False
    return [i for i, prime in enumerate(is_prime) if prime and i >= 2]


def safe_bytes_decode(data):
    encodings = ['utf-8', 'latin-1', 'gbk', 'utf-16-le']
    for enc in encodings:
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    result = "原始字节：\n" + data.hex()
    result += "\n\nBase64:\n" + base64.b64encode(data).decode()
    return result


def rsa_decrypt(n, e, d, c):
    m = pow(int(c), int(d), int(n))
    byte_len = (m.bit_length() + 7) // 8
    byte_data = m.to_bytes(byte_len, 'big')

    result = byte_data.decode('utf-8', errors='ignore') + "\n\n"
    result += "原始数据：\n" + str(m) + "\n\n"
    result += "Base64：\n" + base64.b64encode(byte_data).decode() + "\n\n"
    result += "十六进制：\n" + byte_data.hex() + "\n\n"
    result += "尝试解码：\n" + safe_bytes_decode(byte_data)
    return result

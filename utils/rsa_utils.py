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


def sieve(limit):
    is_primeee = [True] * (limit + 1)
    for n in range(2, int(limit ** 0.5) + 1):
        if is_primeee[n]:
            for i in range(n * n, limit + 1, n):
                is_primeee[i] = False
    return [i for i, prime in enumerate(is_primeee) if prime and i >= 2]


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


def chinese_remainder(n, a):
    sumsum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sumsum += a_i * modinv(p, n_i) * p
    return sumsum % prod


def williams_p_plus_1(n, B1=10000, B2=100000):
    # Williams' p+1 分解算法

    def _lucas_mod(P, Q, k, n):
        # 计算Lucas序列模n
        U, V = 1, P
        for bit in bin(k)[3:]:
            U, V = (U * V) % n, (V * V - 2 * Q) % n
            if bit == '1':
                U, V = (P * U + V) % n, (P * V + D * U) % n
        return U

    D = random.randint(1, n - 1)
    while True:
        P = random.randint(1, n - 1)
        Q = (P * P - D) % n
        if Q == 0: continue

        # 阶段1
        m = 1
        for p in sieve(B1):
            m *= p ** int(math.log(B1, p))

        U = _lucas_mod(P, Q, m, n)
        g = gcd(U, n)
        if g not in (1, n): return g

        # 阶段2
        for p in sieve(B2):
            if p <= B1: continue
            U = _lucas_mod(P, Q, p, n)
            g = gcd(U, n)
            if g not in (1, n): return g
        break
    return None


def is_prime(n, k=5):
    # Miller-Rabin素性测试
    if n <= 1:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, min(n - 2, 2 ** 20))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def williams_pp1(n, B1=10 ** 5, B2=10 ** 6):
    # Williams' p+1 分解算法
    from random import randint
    for _ in range(3):  # 尝试不同种子
        V = randint(2, n - 2)
        m = V
        for i in range(1, B1 + 1):
            m = (m ** 2 - 2) % n
        d = gcd(m - 2, n)
        if d not in (1, n):
            return d
        # 第二阶段
        for i in range(B1 + 1, B2 + 1):
            m = (m ** 2 - 2) % n
            if i % 100 == 0:
                d = gcd(m - 2, n)
                if d not in (1, n):
                    return d
    return None


def pollards_rho(n, seed=1, max_steps=10 ** 6):
    # 增强的Pollard's Rho算法
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    f = lambda x: (pow(x, 2, n) + seed) % n
    x, y, d = 2, 2, 1

    for _ in range(max_steps):
        x = f(f(x))
        y = f(y)
        d = gcd(abs(x - y), n)
        if d not in (1, n):
            return d
        if _ % 1000 == 0 and d == n:  # 检测异常情况
            return None
    return None


def pollards_p_1_optimized(n, B=10 ** 6):
    # 优化版Pollard's p-1算法
    a = 2
    for i in range(2, B + 1):
        a = pow(a, i, n)
        if i % 10000 == 0:
            d = gcd(a - 1, n)
            if d not in (1, n):
                return d
    d = gcd(a - 1, n)
    return d if d not in (1, n) else None

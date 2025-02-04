# attack_methods/DP泄露攻击.py
MODULE_NAME = "DP泄露攻击"
REQUIRED_PARAMS = ["n", "e", "dp", "c"]


def attack(n, e, dp, c):
    from utils.rsa_utils import gcd, modinv
    n, e, dp, c = int(n), int(e), int(dp), int(c)

    for k in range(2, e):
        p = gcd(pow(2, e * dp, n) - 2, n)
        if p != 1 and p != n:
            q = n // p
            d = modinv(e, (p - 1) * (q - 1))
            m = pow(c, d, n)
            return bytes.fromhex(hex(m)[2:]).decode('utf-8', errors='ignore')
    raise ValueError("DP泄露攻击失败")

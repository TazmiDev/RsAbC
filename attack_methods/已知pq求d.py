# attack_methods/已知pq求d.py
MODULE_NAME = "已知p/q求d"
REQUIRED_PARAMS = ["p", "q", "e"]


def attack(p, q, e):
    from utils.rsa_utils import modinv
    p, q, e = int(p), int(q), int(e)

    # 计算n和φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # 计算模逆
    try:
        d = modinv(e, phi)
    except Exception:
        raise ValueError("e和φ(n)不互质，无法计算d")

    return f"""解密参数：
p = {p}
q = {q}
n = {n}
φ(n) = {phi}
d = {d}"""

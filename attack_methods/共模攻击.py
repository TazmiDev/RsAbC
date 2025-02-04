# attack_methods/共模攻击.py
MODULE_NAME = "共模攻击"
REQUIRED_PARAMS = ["n", "e1", "c1", "e2", "c2"]


def attack(n, e1, c1, e2, c2):
    from utils.rsa_utils import egcd, modinv
    n = int(n)
    e1, c1 = int(e1), int(c1)
    e2, c2 = int(e2), int(c2)

    gcd, a, b = egcd(e1, e2)
    if gcd != 1:
        raise ValueError("指数不互质")

    m = (pow(c1, a, n) * pow(c2, b, n)) % n
    return bytes.fromhex(hex(m)[2:]).decode('utf-8', errors='ignore')

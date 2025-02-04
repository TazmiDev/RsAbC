# attack_methods/小指数攻击.py
MODULE_NAME = "低加密指数攻击"
REQUIRED_PARAMS = ["e", "n1", "c1", "n2", "c2", "n3", "c3"]


def attack(e, n1, c1, n2, c2, n3, c3):
    from utils.rsa_utils import chinese_remainder
    e = int(e)
    n = [int(n1), int(n2), int(n3)]
    c = [int(c1), int(c2), int(c3)]

    m_e = chinese_remainder(n, c)
    m = int(m_e ** (1 / e))
    return bytes.fromhex(hex(m)[2:]).decode('utf-8', errors='ignore')

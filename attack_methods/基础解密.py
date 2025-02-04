# attack_methods/基础解密.py
MODULE_NAME = "基础RSA解密"
REQUIRED_PARAMS = ["n", "e", "d", "c"]


def attack(n, e, d, c):
    from utils.rsa_utils import rsa_decrypt
    return rsa_decrypt(int(n), int(e), int(d), int(c))

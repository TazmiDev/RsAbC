# attack_methods/维纳攻击.py
MODULE_NAME = "维纳攻击"
REQUIRED_PARAMS = ["n", "e"]


def attack(n, e):
    from utils.rsa_utils import wiener_attack
    n, e = int(n), int(e)
    d = wiener_attack(e, n)
    return f"破解成功！d = {d}"

# attack_methods/Pollard分解.py
MODULE_NAME = "Pollard分解"
REQUIRED_PARAMS = ["n"]


def attack(n):
    from utils.rsa_utils import pollards_p_1
    n = int(n)
    p = pollards_p_1(n)
    if p:
        return f"分解成功！\np = {p}\nq = {n // p}"
    raise ValueError("Pollard分解失败")

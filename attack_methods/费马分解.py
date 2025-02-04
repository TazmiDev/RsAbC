# attack_methods/费马分解.py
MODULE_NAME = "费马分解"
REQUIRED_PARAMS = ["n"]


def attack(n):
    from utils.rsa_utils import fermat_factorization
    n = int(n)
    p, q = fermat_factorization(n)
    return f"分解成功！\np = {p}\nq = {q}"

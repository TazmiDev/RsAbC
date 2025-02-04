# attack_methods/CRT快速解密.py
MODULE_NAME = "CRT快速解密"
REQUIRED_PARAMS = ["p", "q", "dp", "dq", "c"]


def attack(p, q, dp, dq, c):
    from utils.rsa_utils import chinese_remainder
    p, q = int(p), int(q)
    dp, dq, c = int(dp), int(dq), int(c)
    
    # 计算模指数
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    
    # 中国剩余定理
    m = chinese_remainder([p, q], [m1, m2])
    return bytes.fromhex(hex(m)[2:]).decode('utf-8', errors='ignore')
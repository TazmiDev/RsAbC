# attack_methods/中国剩余定理攻击.py
MODULE_NAME = "中国剩余定理攻击"
REQUIRED_PARAMS = ["e", "n[]", "c[]"]  # 支持动态参数输入


def attack(*args):
    from utils.rsa_utils import chinese_remainder
    e = int(args[0])
    params = args[1:]

    if len(params) % 2 != 0:
        raise ValueError("参数格式应为e, n1,c1, n2,c2,...")

    n = []
    c = []
    for i in range(0, len(params), 2):
        n.append(int(params[i]))
        c.append(int(params[i + 1]))

    m_e = chinese_remainder(n, c)
    m = int(m_e ** (1 / e))

    result = "可能的明文格式：\n"
    result += f"Hex: {hex(m)[2:]}\n"
    result += "尝试解码：\n"
    result += decode_bytes(m)
    return result


def decode_bytes(m):
    byte_data = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    encodings = ['utf-8', 'latin-1', 'utf-16', 'ascii']
    results = []

    for enc in encodings:
        try:
            decoded = byte_data.decode(enc)
            results.append(f"[{enc.upper()}]: {decoded}")
        except UnicodeDecodeError:
            continue

    if not results:
        return "无法自动解码，原始字节：\n" + byte_data.hex()
    return '\n'.join(results)

# attack_methods/自动分解攻击.py 最终优化版
import threading
import logging
from queue import Queue
from utils.rsa_utils import (
    fermat_factorization,
    pollards_rho,
    pollards_p_1_optimized,
    williams_pp1,
    modinv,
    rsa_decrypt,
    is_prime,
    gcd
)

MODULE_NAME = "n/e/c自动解密"
REQUIRED_PARAMS = ["n", "e", "c"]

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FactorizationWorker(threading.Thread):
    def __init__(self, n, result_queue, method_name):
        super().__init__()
        self.n = n
        self.result_queue = result_queue
        self.method_name = method_name
        self.daemon = True

    def run(self):
        try:
            result = None
            if self.method_name == "fermat":
                result = fermat_factorization(self.n, max_attempts=100000)
            elif self.method_name == "pollards_rho":
                result = pollards_rho(self.n, max_steps=10**6)
            elif self.method_name == "pollards_p1":
                result = pollards_p_1_optimized(self.n, B=10**6)
            elif self.method_name == "williams_pp1":
                result = williams_pp1(self.n, B1=10**5, B2=10**6)
            
            if result and 1 < result < self.n:
                self.result_queue.put((self.method_name, result))
        except Exception as e:
            logger.debug(f"{self.method_name} failed: {str(e)}")

def attack(n, e, c):
    n = int(n)
    e = int(e)
    c = int(c)
    
    logger.info(f"开始分解 n={n}")
    
    # 预处理检查
    if n % 2 == 0:
        p, q = 2, n//2
    else:
        # 初始化多线程分解
        result_queue = Queue()
        methods = [
            "fermat",
            "pollards_rho",
            "pollards_p1", 
            "williams_pp1"
        ]
        
        workers = []
        for method in methods:
            worker = FactorizationWorker(n, result_queue, method)
            workers.append(worker)
            worker.start()
        
        # 等待结果
        found = False
        while not found:
            if not result_queue.empty():
                method_name, p = result_queue.get()
                q = n // p
                if p * q == n:
                    logger.info(f"分解成功! 使用方法: {method_name}")
                    found = True
                else:
                    logger.warning(f"无效分解结果 from {method_name}")
            if all(not w.is_alive() for w in workers):
                break
            threading.Event().wait(0.1)
        
        if not found:
            raise ValueError(f"分解失败，尝试以下方法：\n1. 检查n是否正确\n2. 尝试使用https://factordb.com/index.php进行n分解\n3. 尝试其他攻击方式")

    # 验证分解结果
    if p * q != n:
        raise ValueError("分解验证失败")
    
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("分解得到的p/q不是质数")
    
    # 计算私钥
    phi = (p-1)*(q-1)
    d = modinv(e, phi)
    return rsa_decrypt(n, e, d, c)
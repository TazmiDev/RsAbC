# RsAbC 工具

## 简介
这是一个用于CTF用于简单处理 RSA 加密的工具

## 功能
```bash
1.基础解密
2.共模攻击
3.小指数攻击
4.维纳攻击
5.费马分解
6.DP泄露攻击
7.Pollard分解
8.已知pq求d
9.中国剩余定理攻击
10.CRT快速解密
11.自动分解攻击
```

## 安装
请确保你已经安装了 Python 3。然后运行以下命令来安装所需的依赖项：

```bash
python -m venv rsaenv
rsaenv\Scripts\activate
pip install -r requirements.txt
```

## 使用方法
1. 克隆此仓库：
    ```bash
    git clone https://github.com/TazmiDev/RsAbC.git
    ```
2. 进入项目目录：
    ```bash
    cd RsAbC
    pip install -r requirements.txt
    ```
3. 运行工具：
    ```bash
    python main.py
    ```
   
4. 打包：
    ```bash
    pyinstaller build.spec
    ```

## 贡献
欢迎贡献代码！请 fork 此仓库并提交 pull request
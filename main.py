# main.py
import importlib.util
import sys
import tkinter as tk
from tkinter import ttk
import importlib
import os


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def load_attack_modules():
    modules = {}
    base_path = get_base_path()
    attack_dir = os.path.join(base_path, "attack_methods")

    for file in os.listdir(attack_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    os.path.join(attack_dir, file)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                modules[module.MODULE_NAME] = {
                    "params": module.REQUIRED_PARAMS,
                    "function": module.attack
                }
            except Exception as e:
                print(f"加载模块 {module_name} 失败: {str(e)}")
    return modules


def configure_style():
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("primary.TButton",
                    foreground="white",
                    background="#2196F3",
                    font=('微软雅黑', 10, 'bold'))
    style.map("primary.TButton",
              background=[('active', '#1976D2'), ('disabled', '#BBDEFB')])

    style.configure("TCombobox", padding=5)
    style.configure("TLabel", background="#f0f0f0", font=('微软雅黑', 9))
    style.configure("TEntry", padding=5)
    style.configure("TText", font=('Consolas', 9))

    # 结果区域标签样式
    style.configure("Result.TLabel",
                    foreground="#4CAF50",
                    font=('微软雅黑', 10, 'bold'))


class RSADecryptTool:
    def __init__(self, master):
        self.param_frame = None
        self.attack_var = None
        self.result_text = None
        self.master = master
        master.title("RsAbC v1.0")
        master.geometry("800x600")

        # 加载攻击模块
        self.attack_modules = load_attack_modules()

        # 创建GUI
        self.create_widgets()
        self.current_params = []

        configure_style()
        # 添加图标
        if os.path.exists("assets/app.ico"):
            master.iconbitmap("assets/app.ico")

    def create_widgets(self):
        # 主题样式
        style = ttk.Style()
        style.theme_use("clam")

        # 主框架
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="攻击参数配置")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # 攻击方式选择
        ttk.Label(control_frame, text="选择攻击方式:").pack(anchor=tk.W)
        self.attack_var = tk.StringVar()
        attack_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.attack_var,
            values=list(self.attack_modules.keys())
        )
        attack_combobox.pack(fill=tk.X, pady=5)
        attack_combobox.bind("<<ComboboxSelected>>", self.update_parameters)

        # 参数输入区域
        self.param_frame = ttk.Frame(control_frame)
        self.param_frame.pack(fill=tk.X, pady=10)

        # 操作按钮
        ttk.Button(
            control_frame,
            text="执行攻击",
            command=self.execute_attack,
            style="primary.TButton"
        ).pack(side=tk.BOTTOM, pady=10)

        # 右侧结果展示
        result_frame = ttk.LabelFrame(main_frame, text="攻击结果")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_text = tk.Text(
            result_frame,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def update_parameters(self, event=None):
        # 清空现有参数
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        # 获取当前选择的攻击方式
        attack_name = self.attack_var.get()
        if not attack_name:
            return

        # 创建新的参数输入框
        params = self.attack_modules[attack_name]["params"]
        self.current_params = []
        for param in params:
            frame = ttk.Frame(self.param_frame)
            frame.pack(fill=tk.X, pady=2)

            ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.current_params.append(entry)

    def execute_attack(self):
        attack_name = self.attack_var.get()
        if not attack_name:
            return

        # 收集参数
        params = [entry.get() for entry in self.current_params]

        try:
            # 调用攻击函数
            result = self.attack_modules[attack_name]["function"](*params)
            self.show_result(f"攻击成功！\n解密结果：\n{result}")
        except Exception as e:
            self.show_result(f"攻击失败：{str(e)}")

    def show_result(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = RSADecryptTool(root)
    root.mainloop()

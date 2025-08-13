"""
电脑实用工具集
作者: AI Assistant
版本: 1.0.0
"""


import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目路径
from main_window import MainWindow


def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        app = MainWindow(root)
        
        # 启动应用
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
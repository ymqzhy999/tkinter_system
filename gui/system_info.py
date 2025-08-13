#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息界面
"""

import tkinter as tk
from tkinter import ttk
import psutil
import platform
import threading
import time
import socket

class SystemInfoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.monitoring = False
        self.monitor_thread = None
        self.create_widgets()
        self.start_monitoring()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建选项卡
        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # 系统概览选项卡
        self.create_overview_tab(notebook)
        
        # CPU信息选项卡
        self.create_cpu_tab(notebook)
        
        # 内存信息选项卡
        self.create_memory_tab(notebook)
        
        # 磁盘信息选项卡
        self.create_disk_tab(notebook)
        
        # 网络信息选项卡
        self.create_network_tab(notebook)
        
    def create_overview_tab(self, notebook):
        """创建系统概览选项卡"""
        overview_frame = ttk.Frame(notebook)
        notebook.add(overview_frame, text="系统概览")
        
        # 系统基本信息
        info_frame = ttk.LabelFrame(overview_frame, text="系统信息", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 获取系统信息
        system_info = self.get_system_info()
        
        # 显示系统信息
        row = 0
        for key, value in system_info.items():
            ttk.Label(info_frame, text=f"{key}:").grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Label(info_frame, text=value).grid(row=row, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            row += 1
            
        # 实时监控框架
        monitor_frame = ttk.LabelFrame(overview_frame, text="实时监控", padding="10")
        monitor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # CPU使用率
        ttk.Label(monitor_frame, text="CPU使用率:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cpu_label = ttk.Label(monitor_frame, text="0%")
        self.cpu_label.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 内存使用率
        ttk.Label(monitor_frame, text="内存使用率:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.memory_label = ttk.Label(monitor_frame, text="0%")
        self.memory_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 磁盘使用率
        ttk.Label(monitor_frame, text="磁盘使用率:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.disk_label = ttk.Label(monitor_frame, text="0%")
        self.disk_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 网络状态
        ttk.Label(monitor_frame, text="网络状态:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.network_label = ttk.Label(monitor_frame, text="检查中...")
        self.network_label.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 监控控制按钮
        control_frame = ttk.Frame(monitor_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(
            control_frame,
            text="开始监控",
            command=self.start_monitoring
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(
            control_frame,
            text="停止监控",
            command=self.stop_monitoring,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # 配置网格权重
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.rowconfigure(1, weight=1)
        
    def create_cpu_tab(self, notebook):
        """创建CPU信息选项卡"""
        cpu_frame = ttk.Frame(notebook)
        notebook.add(cpu_frame, text="CPU信息")
        
        # CPU详细信息
        cpu_info = self.get_cpu_info()
        
        # 创建树形视图
        tree = ttk.Treeview(cpu_frame, columns=("value",), show="tree headings")
        tree.heading("#0", text="属性")
        tree.heading("value", text="值")
        
        # 添加CPU信息
        for category, items in cpu_info.items():
            category_item = tree.insert("", "end", text=category)
            for key, value in items.items():
                tree.insert(category_item, "end", text=key, values=(value,))
                
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        cpu_frame.columnconfigure(0, weight=1)
        cpu_frame.rowconfigure(0, weight=1)
        
    def create_memory_tab(self, notebook):
        """创建内存信息选项卡"""
        memory_frame = ttk.Frame(notebook)
        notebook.add(memory_frame, text="内存信息")
        
        # 内存详细信息
        memory_info = self.get_memory_info()
        
        # 创建树形视图
        tree = ttk.Treeview(memory_frame, columns=("value",), show="tree headings")
        tree.heading("#0", text="属性")
        tree.heading("value", text="值")
        
        # 添加内存信息
        for category, items in memory_info.items():
            category_item = tree.insert("", "end", text=category)
            for key, value in items.items():
                tree.insert(category_item, "end", text=key, values=(value,))
                
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        memory_frame.columnconfigure(0, weight=1)
        memory_frame.rowconfigure(0, weight=1)
        
    def create_disk_tab(self, notebook):
        """创建磁盘信息选项卡"""
        disk_frame = ttk.Frame(notebook)
        notebook.add(disk_frame, text="磁盘信息")
        
        # 磁盘详细信息
        disk_info = self.get_disk_info()
        
        # 创建树形视图
        tree = ttk.Treeview(disk_frame, columns=("total", "used", "free", "percent"), show="tree headings")
        tree.heading("#0", text="磁盘")
        tree.heading("total", text="总容量")
        tree.heading("used", text="已使用")
        tree.heading("free", text="可用空间")
        tree.heading("percent", text="使用率")
        
        # 添加磁盘信息
        for disk, info in disk_info.items():
            tree.insert("", "end", text=disk, values=(
                info["total"],
                info["used"],
                info["free"],
                f"{info['percent']}%"
            ))
            
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        disk_frame.columnconfigure(0, weight=1)
        disk_frame.rowconfigure(0, weight=1)
        
    def create_network_tab(self, notebook):
        """创建网络信息选项卡"""
        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="网络信息")
        
        # 网络详细信息
        network_info = self.get_network_info()
        
        # 创建树形视图
        tree = ttk.Treeview(network_frame, columns=("value",), show="tree headings")
        tree.heading("#0", text="属性")
        tree.heading("value", text="值")
        
        # 添加网络信息
        for interface, info in network_info.items():
            interface_item = tree.insert("", "end", text=interface)
            for key, value in info.items():
                tree.insert(interface_item, "end", text=key, values=(value,))
                
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        network_frame.columnconfigure(0, weight=1)
        network_frame.rowconfigure(0, weight=1)
        
    def get_system_info(self):
        """获取系统基本信息"""
        return {
            "操作系统": platform.system() + " " + platform.release(),
            "系统版本": platform.version(),
            "架构": platform.machine(),
            "处理器": platform.processor(),
            "主机名": platform.node(),
            "Python版本": platform.python_version()
        }
        
    def get_cpu_info(self):
        """获取CPU详细信息"""
        cpu_info = {}
        
        # CPU核心信息
        cpu_info["核心信息"] = {
            "物理核心数": psutil.cpu_count(logical=False),
            "逻辑核心数": psutil.cpu_count(logical=True),
            "当前频率": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "未知",
            "最大频率": f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "未知"
        }
        
        # CPU使用率统计
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_info["使用率统计"] = {
            "当前使用率": f"{cpu_percent}%",
            "平均使用率": f"{psutil.cpu_percent(interval=1)}%"
        }
        
        return cpu_info
        
    def get_memory_info(self):
        """获取内存详细信息"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        memory_info = {}
        
        # 物理内存
        memory_info["物理内存"] = {
            "总容量": self.format_bytes(memory.total),
            "可用容量": self.format_bytes(memory.available),
            "已使用": self.format_bytes(memory.used),
            "使用率": f"{memory.percent}%"
        }
        
        # 交换内存
        memory_info["交换内存"] = {
            "总容量": self.format_bytes(swap.total),
            "可用容量": self.format_bytes(swap.free),
            "已使用": self.format_bytes(swap.used),
            "使用率": f"{swap.percent}%"
        }
        
        return memory_info
        
    def get_disk_info(self):
        """获取磁盘详细信息"""
        disk_info = {}
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "total": self.format_bytes(usage.total),
                    "used": self.format_bytes(usage.used),
                    "free": self.format_bytes(usage.free),
                    "percent": usage.percent
                }
            except PermissionError:
                continue
                
        return disk_info
        
    def get_network_info(self):
        """获取网络详细信息"""
        network_info = {}
        
        for interface, addresses in psutil.net_if_addrs().items():
            network_info[interface] = {}
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    network_info[interface]["IPv4地址"] = addr.address
                    network_info[interface]["子网掩码"] = addr.netmask
                elif addr.family == socket.AF_INET6:  # IPv6
                    network_info[interface]["IPv6地址"] = addr.address
                    
        return network_info
        
    def format_bytes(self, bytes_value):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
        
    def start_monitoring(self):
        """开始监控"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        def monitor():
            while self.monitoring:
                try:
                    # 检查组件是否还存在
                    if not self.winfo_exists():
                        break
                        
                    # 更新CPU使用率
                    cpu_percent = psutil.cpu_percent(interval=1)
                    if self.cpu_label.winfo_exists():
                        self.cpu_label.config(text=f"{cpu_percent}%")
                    
                    # 更新内存使用率
                    memory = psutil.virtual_memory()
                    if self.memory_label.winfo_exists():
                        self.memory_label.config(text=f"{memory.percent}%")
                    
                    # 更新磁盘使用率
                    try:
                        disk = psutil.disk_usage('/')
                        if self.disk_label.winfo_exists():
                            self.disk_label.config(text=f"{disk.percent}%")
                    except:
                        # Windows系统使用C盘
                        try:
                            disk = psutil.disk_usage('C:\\')
                            if self.disk_label.winfo_exists():
                                self.disk_label.config(text=f"{disk.percent}%")
                        except:
                            if self.disk_label.winfo_exists():
                                self.disk_label.config(text="未知")
                    
                    # 更新网络状态
                    network_status = "已连接" if psutil.net_if_stats() else "未连接"
                    if self.network_label.winfo_exists():
                        self.network_label.config(text=network_status)
                    
                    time.sleep(2)  # 每2秒更新一次
                    
                except Exception as e:
                    print(f"监控错误: {e}")
                    time.sleep(5)
                    
        # 在后台线程中运行监控
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
    def destroy(self):
        """销毁时停止监控"""
        self.stop_monitoring()
        super().destroy() 
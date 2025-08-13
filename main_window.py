#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.load_config()
        self.setup_window()
        self.create_widgets()
        self.apply_theme()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title("电脑实用工具集 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置窗口图标
        icon_path = Path(__file__).parent.parent / "assets" / "icons" / "app.ico"
        if icon_path.exists():
            self.root.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # 创建标题
        title_label = ttk.Label(
            self.main_frame, 
            text=self.get_text("title"),
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 创建左侧导航栏
        self.create_navigation()
        
        # 创建右侧内容区域
        self.create_content_area()
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_navigation(self):
        """创建导航栏"""
        # 导航框架
        nav_frame = ttk.LabelFrame(self.main_frame, text=self.get_text("modules"), padding="10")
        nav_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 导航按钮
        nav_buttons = [
            (self.get_text("system_info"), self.show_system_info),
            (self.get_text("maintenance"), self.show_maintenance),
            (self.get_text("network_tools"), self.show_network_tools),
            (self.get_text("file_manager"), self.show_file_manager),
            (self.get_text("quick_commands"), self.show_quick_commands),
            (self.get_text("settings"), self.show_settings)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = ttk.Button(
                nav_frame, 
                text=text, 
                command=command,
                width=15
            )
            btn.grid(row=i, column=0, pady=2, sticky=(tk.W, tk.E))
            
    def create_content_area(self):
        """创建内容区域"""
        # 内容框架
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 默认显示欢迎页面
        self.show_welcome()
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Label(
            self.main_frame, 
            text=self.get_text("ready"), 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def load_config(self):
        """加载配置文件"""
        config_path = Path(__file__).parent.parent / "config" / "settings.json"
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.get_default_config()
                self.save_config()
        except Exception as e:
            messagebox.showwarning("警告", f"配置文件加载失败: {str(e)}")
            self.config = self.get_default_config()
            
    def get_default_config(self):
        """获取默认配置"""
        return {
            "theme": "default",
            "language": "zh_CN",
            "auto_update": True,
            "startup_scan": False,
            "log_level": "INFO",
            "window_size": {"width": 800, "height": 600},
            "window_position": {"x": -1, "y": -1}
        }
        
    def save_config(self):
        """保存配置文件"""
        config_path = Path(__file__).parent.parent / "config" / "settings.json"
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("错误", f"配置文件保存失败: {str(e)}")
            
    def apply_theme(self):
        """应用主题"""
        try:
            theme = self.config.get("theme", "default")
            style = ttk.Style()
            
            # 设置主题
            if theme in style.theme_names():
                style.theme_use(theme)
            else:
                style.theme_use("default")
                
            # 自定义样式
            style.configure("Accent.TButton", 
                          background="#0078d4", 
                          foreground="white",
                          font=("Arial", 10, "bold"))
                          
            style.map("Accent.TButton",
                     background=[("active", "#106ebe"), ("pressed", "#005a9e")])
                     
        except Exception as e:
            print(f"主题应用失败: {e}")
            
    def get_text(self, key):
        """获取多语言文本"""
        texts = {
            "zh_CN": {
                "title": "电脑实用工具集",
                "modules": "功能模块",
                "system_info": "系统信息",
                "maintenance": "系统维护",
                "network_tools": "网络工具",
                "file_manager": "文件管理",
                "quick_commands": "快速指令",
                "settings": "设置",
                "ready": "就绪",
                "welcome_title": "欢迎使用电脑实用工具集！",
                "welcome_desc": "本工具集提供系统信息查看、系统维护、网络工具、文件管理等功能，\n帮助您更好地管理和维护电脑。\n\n请从左侧选择功能模块开始使用。",
                "loading_system_info": "正在加载系统信息...",
                "loading_maintenance": "正在加载系统维护...",
                "loading_network": "正在加载网络工具...",
                "loading_file_manager": "正在加载文件管理...",
                "loading_commands": "正在加载快速指令...",
                "loading_settings": "正在加载设置...",
                "theme_label": "界面主题:",
                "language_label": "界面语言:",
                "auto_update": "启用自动更新",
                "startup_scan": "启动时进行系统扫描",
                "save_settings": "保存设置",
                "settings_saved": "设置已保存",
                "executing": "正在执行:",
                "command_completed": "命令执行完成",
                "command_failed": "命令执行失败",
                "config_load_failed": "配置文件加载失败:",
                "config_save_failed": "配置文件保存失败:",
                "warning": "警告",
                "error": "错误",
                "success": "成功"
            },
            "en_US": {
                "title": "Computer Utility Toolkit",
                "modules": "Modules",
                "system_info": "System Info",
                "maintenance": "Maintenance",
                "network_tools": "Network Tools",
                "file_manager": "File Manager",
                "quick_commands": "Quick Commands",
                "settings": "Settings",
                "ready": "Ready",
                "welcome_title": "Welcome to Computer Utility Toolkit!",
                "welcome_desc": "This toolkit provides system information viewing, system maintenance, network tools, file management and other functions,\nto help you better manage and maintain your computer.\n\nPlease select a function module from the left to start using.",
                "loading_system_info": "Loading system information...",
                "loading_maintenance": "Loading system maintenance...",
                "loading_network": "Loading network tools...",
                "loading_file_manager": "Loading file manager...",
                "loading_commands": "Loading quick commands...",
                "loading_settings": "Loading settings...",
                "theme_label": "Theme:",
                "language_label": "Language:",
                "auto_update": "Enable auto update",
                "startup_scan": "Scan system on startup",
                "save_settings": "Save Settings",
                "settings_saved": "Settings saved",
                "executing": "Executing:",
                "command_completed": "Command completed",
                "command_failed": "Command failed",
                "config_load_failed": "Config file load failed:",
                "config_save_failed": "Config file save failed:",
                "warning": "Warning",
                "error": "Error",
                "success": "Success"
            }
        }
        
        language = self.config.get("language", "zh_CN")
        return texts.get(language, texts["zh_CN"]).get(key, key)
        
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def show_welcome(self):
        """显示欢迎页面"""
        # 清空内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # 创建欢迎内容
        welcome_frame = ttk.Frame(self.content_frame, padding="20")
        welcome_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        welcome_label = ttk.Label(
            welcome_frame,
            text=self.get_text("welcome_title"),
            font=("Arial", 14, "bold")
        )
        welcome_label.grid(row=0, column=0, pady=(0, 20))
        
        desc_label = ttk.Label(
            welcome_frame,
            text=self.get_text("welcome_desc"),
            font=("Arial", 10),
            justify=tk.CENTER
        )
        desc_label.grid(row=1, column=0)
        
    def show_system_info(self):
        """显示系统信息页面"""
        self.update_status(self.get_text("loading_system_info"))
        # 这里将调用系统信息模块
        try:
            from gui.system_info import SystemInfoFrame
            self.show_module(SystemInfoFrame)
        except ImportError as e:
            messagebox.showerror("错误", f"无法加载系统信息模块: {str(e)}")
        
    def show_maintenance(self):
        """显示系统维护页面"""
        self.update_status(self.get_text("loading_maintenance"))
        try:
            from gui.maintenance import MaintenanceFrame
            self.show_module(MaintenanceFrame)
        except ImportError as e:
            messagebox.showerror("错误", f"无法加载系统维护模块: {str(e)}")
        
    def show_network_tools(self):
        """显示网络工具页面"""
        self.update_status(self.get_text("loading_network"))
        try:
            from gui.network import NetworkFrame
            self.show_module(NetworkFrame)
        except ImportError as e:
            messagebox.showerror("错误", f"无法加载网络工具模块: {str(e)}")
        
    def show_file_manager(self):
        """显示文件管理页面"""
        self.update_status(self.get_text("loading_file_manager"))
        try:
            from gui.file_manager import FileManagerFrame
            self.show_module(FileManagerFrame)
        except ImportError as e:
            messagebox.showerror("错误", f"无法加载文件管理模块: {str(e)}")
        
    def show_quick_commands(self):
        """显示快速指令页面"""
        self.update_status(self.get_text("loading_commands"))
        self.show_quick_commands_page()
        
    def show_settings(self):
        """显示设置页面"""
        self.update_status(self.get_text("loading_settings"))
        self.show_settings_page()
        
    def show_module(self, module_class):
        """显示模块页面"""
        # 清空内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # 创建模块实例
        module_instance = module_class(self.content_frame)
        module_instance.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
    def show_quick_commands_page(self):
        """显示快速指令页面"""
        # 清空内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # 创建快速指令界面
        commands_frame = ttk.LabelFrame(self.content_frame, text=self.get_text("quick_commands"), padding="10")
        commands_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        commands_frame.columnconfigure(0, weight=1)
        
        # 加载快速指令
        self.load_quick_commands(commands_frame)
        
    def load_quick_commands(self, parent):
        """加载快速指令"""
        commands = [
            ("打开任务管理器", "taskmgr"),
            ("打开系统属性", "sysdm.cpl"),
            ("打开设备管理器", "devmgmt.msc"),
            ("打开服务", "services.msc"),
            ("打开注册表编辑器", "regedit"),
            ("打开命令提示符", "cmd"),
            ("打开计算器", "calc"),
            ("打开记事本", "notepad"),
            ("打开画图", "mspaint"),
            ("打开控制面板", "control"),
            ("清理临时文件", "cleanmgr"),
            ("磁盘碎片整理", "dfrgui"),
            ("系统文件检查", "sfc /scannow"),
            ("网络诊断", "netsh wlan show networks"),
            ("查看IP配置", "ipconfig /all")
        ]
        
        # 创建按钮网格
        for i, (name, command) in enumerate(commands):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                parent,
                text=name,
                command=lambda cmd=command: self.execute_command(cmd),
                width=20
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))
            
    def execute_command(self, command):
        """执行命令"""
        try:
            import subprocess
            import os
            import platform
            self.update_status(f"{self.get_text('executing')} {command}")
            
            # 设置环境变量以解决编码问题
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            if platform.system() == "Windows":
                # Windows系统使用os.startfile()避免编码问题
                if command == "cmd":
                    # 打开命令提示符
                    os.startfile("cmd.exe")
                elif command == "taskmgr":
                    # 打开任务管理器
                    os.startfile("taskmgr.exe")
                elif command == "calc":
                    # 打开计算器
                    os.startfile("calc.exe")
                elif command == "notepad":
                    # 打开记事本
                    os.startfile("notepad.exe")
                elif command == "mspaint":
                    # 打开画图
                    os.startfile("mspaint.exe")
                elif command == "control":
                    # 打开控制面板
                    os.startfile("control.exe")
                elif command == "cleanmgr":
                    # 打开磁盘清理
                    os.startfile("cleanmgr.exe")
                elif command == "dfrgui":
                    # 打开磁盘碎片整理
                    os.startfile("dfrgui.exe")
                elif command == "sfc /scannow":
                    # 系统文件检查（需要管理员权限）
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", "sfc /scannow"], shell=True, env=env)
                elif command == "netsh wlan show networks":
                    # 显示无线网络
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", "netsh wlan show networks"], shell=True, env=env)
                elif command == "ipconfig /all":
                    # 显示IP配置
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", "ipconfig /all"], shell=True, env=env)
                else:
                    # 执行其他命令
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command], shell=True, env=env)
            else:
                # 非Windows系统使用subprocess
                if command == "cmd":
                    subprocess.Popen(["xterm"], shell=True, env=env)
                else:
                    subprocess.Popen(command, shell=True, env=env)
                
            self.update_status(self.get_text("command_completed"))
            
        except Exception as e:
            messagebox.showerror(self.get_text("error"), f"{self.get_text('command_failed')}: {str(e)}")
            self.update_status(self.get_text("command_failed"))
            
    def show_settings_page(self):
        """显示设置页面"""
        # 清空内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # 创建设置界面
        settings_frame = ttk.LabelFrame(self.content_frame, text=self.get_text("settings"), padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # 创建设置选项
        self.create_settings_options(settings_frame)
        
    def create_settings_options(self, parent):
        """创建设置选项"""
        # 主题设置
        ttk.Label(parent, text=self.get_text("theme_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        theme_var = tk.StringVar(value=self.config.get("theme", "default"))
        theme_combo = ttk.Combobox(
            parent, 
            textvariable=theme_var,
            values=["default", "clam", "alt", "classic"],
            state="readonly"
        )
        theme_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 语言设置
        ttk.Label(parent, text=self.get_text("language_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        lang_var = tk.StringVar(value=self.config.get("language", "zh_CN"))
        lang_combo = ttk.Combobox(
            parent, 
            textvariable=lang_var,
            values=["zh_CN", "en_US"],
            state="readonly"
        )
        lang_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 自动更新
        auto_update_var = tk.BooleanVar(value=self.config.get("auto_update", True))
        auto_update_check = ttk.Checkbutton(
            parent,
            text=self.get_text("auto_update"),
            variable=auto_update_var
        )
        auto_update_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 启动时扫描
        startup_scan_var = tk.BooleanVar(value=self.config.get("startup_scan", False))
        startup_scan_check = ttk.Checkbutton(
            parent,
            text=self.get_text("startup_scan"),
            variable=startup_scan_var
        )
        startup_scan_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 保存按钮
        save_btn = ttk.Button(
            parent,
            text=self.get_text("save_settings"),
            command=lambda: self.save_settings({
                "theme": theme_var.get(),
                "language": lang_var.get(),
                "auto_update": auto_update_var.get(),
                "startup_scan": startup_scan_var.get()
            })
        )
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
    def save_settings(self, new_config):
        """保存设置"""
        old_theme = self.config.get("theme")
        old_language = self.config.get("language")
        
        self.config.update(new_config)
        self.save_config()
        
        # 应用新设置
        if new_config.get("theme") != old_theme:
            self.apply_theme()
            
        if new_config.get("language") != old_language:
            # 重新创建界面以应用新语言
            self.refresh_interface()
            
        messagebox.showinfo(self.get_text("success"), self.get_text("settings_saved"))
        
    def refresh_interface(self):
        """刷新界面以应用新设置"""
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # 重新创建界面
        self.create_widgets() 
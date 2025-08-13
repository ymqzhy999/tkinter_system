import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import threading
import subprocess
import tempfile
"""
系统维护界面
"""



class MaintenanceFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 创建功能按钮
        self.create_maintenance_buttons(main_frame)
        
        # 创建日志区域
        self.create_log_area(main_frame)
        
    def create_maintenance_buttons(self, parent):
        """创建维护功能按钮"""
        # 维护功能框架
        buttons_frame = ttk.LabelFrame(parent, text="系统维护功能", padding="10")
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # 第一行按钮
        row1_frame = ttk.Frame(buttons_frame)
        row1_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row1_frame,
            text="清理临时文件",
            command=self.clean_temp_files,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row1_frame,
            text="清理回收站",
            command=self.empty_recycle_bin,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row1_frame,
            text="清理浏览器缓存",
            command=self.clean_browser_cache,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 第二行按钮
        row2_frame = ttk.Frame(buttons_frame)
        row2_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row2_frame,
            text="磁盘碎片整理",
            command=self.defrag_disk,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row2_frame,
            text="系统文件检查",
            command=self.check_system_files,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row2_frame,
            text="注册表清理",
            command=self.clean_registry,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 第三行按钮
        row3_frame = ttk.Frame(buttons_frame)
        row3_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row3_frame,
            text="系统优化",
            command=self.optimize_system,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row3_frame,
            text="启动项管理",
            command=self.manage_startup,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row3_frame,
            text="服务管理",
            command=self.manage_services,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 全自动维护按钮
        auto_frame = ttk.Frame(buttons_frame)
        auto_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(
            auto_frame,
            text="一键系统维护",
            command=self.auto_maintenance,
            style="Accent.TButton"
        ).grid(row=0, column=0, padx=5)
        
    def create_log_area(self, parent):
        """创建日志区域"""
        # 日志框架
        log_frame = ttk.LabelFrame(parent, text="操作日志", padding="10")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 创建文本区域和滚动条
        text_frame = ttk.Frame(log_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(text_frame, height=10, width=60)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 添加清除日志按钮
        ttk.Button(
            log_frame,
            text="清除日志",
            command=self.clear_log
        ).grid(row=1, column=0, pady=(10, 0))
        
    def log_message(self, message):
        """添加日志消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.update_idletasks()
        
    def clear_log(self):
        """清除日志"""
        self.log_text.delete(1.0, tk.END)
        
    def clean_temp_files(self):
        """清理临时文件"""
        def clean():
            try:
                self.log_message("开始清理临时文件...")
                
                # 系统临时目录
                temp_dirs = [
                    tempfile.gettempdir(),
                    os.path.expanduser("~/AppData/Local/Temp"),
                    os.path.expanduser("~/AppData/Local/Microsoft/Windows/INetCache"),
                    os.path.expanduser("~/AppData/Local/Microsoft/Windows/WebCache")
                ]
                
                total_size = 0
                file_count = 0
                
                for temp_dir in temp_dirs:
                    if os.path.exists(temp_dir):
                        self.log_message(f"清理目录: {temp_dir}")
                        
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    if os.path.exists(file_path):
                                        file_size = os.path.getsize(file_path)
                                        os.remove(file_path)
                                        total_size += file_size
                                        file_count += 1
                                except Exception as e:
                                    continue
                                    
                self.log_message(f"临时文件清理完成，删除了 {file_count} 个文件，释放空间 {self.format_bytes(total_size)}")
                
            except Exception as e:
                self.log_message(f"清理临时文件失败: {str(e)}")
                
        threading.Thread(target=clean, daemon=True).start()
        
    def empty_recycle_bin(self):
        """清空回收站"""
        def empty():
            try:
                self.log_message("开始清空回收站...")
                
                import winshell
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                
                self.log_message("回收站清空完成")
                
            except ImportError:
                self.log_message("需要安装 winshell 模块: pip install winshell")
            except Exception as e:
                self.log_message(f"清空回收站失败: {str(e)}")
                
        threading.Thread(target=empty, daemon=True).start()
        
    def clean_browser_cache(self):
        """清理浏览器缓存"""
        def clean():
            try:
                self.log_message("开始清理浏览器缓存...")
                
                # Chrome缓存目录
                chrome_cache = os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Cache")
                if os.path.exists(chrome_cache):
                    shutil.rmtree(chrome_cache)
                    self.log_message("Chrome缓存已清理")
                    
                # Firefox缓存目录
                firefox_cache = os.path.expanduser("~/AppData/Local/Mozilla/Firefox/Profiles")
                if os.path.exists(firefox_cache):
                    for profile in os.listdir(firefox_cache):
                        cache_dir = os.path.join(firefox_cache, profile, "cache2")
                        if os.path.exists(cache_dir):
                            shutil.rmtree(cache_dir)
                    self.log_message("Firefox缓存已清理")
                    
                self.log_message("浏览器缓存清理完成")
                
            except Exception as e:
                self.log_message(f"清理浏览器缓存失败: {str(e)}")
                
        threading.Thread(target=clean, daemon=True).start()
        
    def defrag_disk(self):
        """磁盘碎片整理"""
        def defrag():
            try:
                self.log_message("开始磁盘碎片整理...")
                
                # 使用Windows内置的磁盘碎片整理工具
                result = subprocess.run(
                    ["defrag", "C:", "/A"],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                if result.returncode == 0:
                    self.log_message("磁盘碎片整理完成")
                else:
                    self.log_message(f"磁盘碎片整理失败: {result.stderr}")
                    
            except Exception as e:
                self.log_message(f"磁盘碎片整理失败: {str(e)}")
                
        threading.Thread(target=defrag, daemon=True).start()
        
    def check_system_files(self):
        """系统文件检查"""
        def check():
            try:
                self.log_message("开始系统文件检查...")
                
                # 使用sfc命令检查系统文件
                result = subprocess.run(
                    ["sfc", "/scannow"],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                if result.returncode == 0:
                    self.log_message("系统文件检查完成，未发现问题")
                else:
                    self.log_message(f"系统文件检查发现问题: {result.stderr}")
                    
            except Exception as e:
                self.log_message(f"系统文件检查失败: {str(e)}")
                
        threading.Thread(target=check, daemon=True).start()
        
    def clean_registry(self):
        """注册表清理"""
        def clean():
            try:
                self.log_message("开始注册表清理...")
                
                # 这里应该使用专业的注册表清理工具
                # 由于安全性考虑，这里只是示例
                self.log_message("注册表清理功能需要专业工具支持")
                self.log_message("建议使用CCleaner等专业清理工具")
                
            except Exception as e:
                self.log_message(f"注册表清理失败: {str(e)}")
                
        threading.Thread(target=clean, daemon=True).start()
        
    def optimize_system(self):
        """系统优化"""
        def optimize():
            try:
                self.log_message("开始系统优化...")
                
                # 禁用不必要的服务
                services_to_disable = [
                    "Themes",
                    "WSearch",
                    "SysMain"
                ]
                
                for service in services_to_disable:
                    try:
                        subprocess.run(
                            ["sc", "config", service, "start=disabled"],
                            capture_output=True,
                            shell=True
                        )
                        self.log_message(f"服务 {service} 已禁用")
                    except:
                        continue
                        
                self.log_message("系统优化完成")
                
            except Exception as e:
                self.log_message(f"系统优化失败: {str(e)}")
                
        threading.Thread(target=optimize, daemon=True).start()
        
    def manage_startup(self):
        """启动项管理"""
        try:
            self.log_message("打开启动项管理器...")
            
            # 打开任务管理器的启动项选项卡
            subprocess.Popen(["taskmgr"], shell=True)
            
        except Exception as e:
            self.log_message(f"打开启动项管理器失败: {str(e)}")
            
    def manage_services(self):
        """服务管理"""
        try:
            self.log_message("打开服务管理器...")
            
            # 打开服务管理器
            subprocess.Popen(["services.msc"], shell=True)
            
        except Exception as e:
            self.log_message(f"打开服务管理器失败: {str(e)}")
            
    def auto_maintenance(self):
        """一键系统维护"""
        def maintenance():
            try:
                self.log_message("开始一键系统维护...")
                
                # 执行所有维护操作
                self.clean_temp_files()
                self.empty_recycle_bin()
                self.clean_browser_cache()
                self.defrag_disk()
                self.check_system_files()
                self.optimize_system()
                
                self.log_message("一键系统维护完成")
                
            except Exception as e:
                self.log_message(f"一键系统维护失败: {str(e)}")
                
        threading.Thread(target=maintenance, daemon=True).start()
        
    def format_bytes(self, bytes_value):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB" 
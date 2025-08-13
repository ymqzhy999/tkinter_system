#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import hashlib
import threading
from pathlib import Path
import zipfile
import time

class FileManagerFrame(ttk.Frame):
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
        
        # 创建文件管理按钮
        self.create_file_buttons(main_frame)
        
        # 创建结果显示区域
        self.create_result_area(main_frame)
        
    def create_file_buttons(self, parent):
        """创建文件管理按钮"""
        # 文件管理框架
        buttons_frame = ttk.LabelFrame(parent, text="文件管理功能", padding="10")
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
            text="批量重命名",
            command=self.batch_rename,
            width=15
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row1_frame,
            text="文件搜索",
            command=self.search_files,
            width=15
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row1_frame,
            text="查找重复文件",
            command=self.find_duplicates,
            width=15
        ).grid(row=0, column=2, padx=5)
        
        # 第二行按钮
        row2_frame = ttk.Frame(buttons_frame)
        row2_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row2_frame,
            text="压缩文件",
            command=self.compress_files,
            width=15
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row2_frame,
            text="解压文件",
            command=self.extract_files,
            width=15
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row2_frame,
            text="文件分类",
            command=self.categorize_files,
            width=15
        ).grid(row=0, column=2, padx=5)
        
        # 第三行按钮
        row3_frame = ttk.Frame(buttons_frame)
        row3_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row3_frame,
            text="磁盘空间分析",
            command=self.analyze_disk_space,
            width=15
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row3_frame,
            text="权限管理",
            command=self.manage_permissions,
            width=15
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row3_frame,
            text="文件同步",
            command=self.sync_files,
            width=15
        ).grid(row=0, column=2, padx=5)
        
        # 路径选择框架
        path_frame = ttk.LabelFrame(buttons_frame, text="路径设置", padding="10")
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 源路径
        ttk.Label(path_frame, text="源路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_path = tk.StringVar()
        source_entry = ttk.Entry(path_frame, textvariable=self.source_path, width=40)
        source_entry.grid(row=0, column=1, padx=(10, 5), pady=5)
        
        ttk.Button(
            path_frame,
            text="浏览",
            command=self.browse_source
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # 目标路径
        ttk.Label(path_frame, text="目标路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.target_path = tk.StringVar()
        target_entry = ttk.Entry(path_frame, textvariable=self.target_path, width=40)
        target_entry.grid(row=1, column=1, padx=(10, 5), pady=5)
        
        ttk.Button(
            path_frame,
            text="浏览",
            command=self.browse_target
        ).grid(row=1, column=2, padx=5, pady=5)
        
    def create_result_area(self, parent):
        """创建结果显示区域"""
        # 结果框架
        result_frame = ttk.LabelFrame(parent, text="操作结果", padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 创建文本区域和滚动条
        text_frame = ttk.Frame(result_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(text_frame, height=15, width=70)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 添加清除结果按钮
        ttk.Button(
            result_frame,
            text="清除结果",
            command=self.clear_results
        ).grid(row=1, column=0, pady=(10, 0))
        
    def log_result(self, message):
        """添加结果消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.result_text.insert(tk.END, log_entry)
        self.result_text.see(tk.END)
        self.update_idletasks()
        
    def clear_results(self):
        """清除结果"""
        self.result_text.delete(1.0, tk.END)
        
    def browse_source(self):
        """浏览源路径"""
        path = filedialog.askdirectory(title="选择源目录")
        if path:
            self.source_path.set(path)
            
    def browse_target(self):
        """浏览目标路径"""
        path = filedialog.askdirectory(title="选择目标目录")
        if path:
            self.target_path.set(path)
            
    def batch_rename(self):
        """批量重命名"""
        def rename():
            try:
                source_dir = self.source_path.get().strip()
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                self.log_result("开始批量重命名...")
                
                # 获取所有文件
                files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
                
                renamed_count = 0
                for i, filename in enumerate(files, 1):
                    if not self.winfo_exists():
                        break
                        
                    name, ext = os.path.splitext(filename)
                    new_name = f"file_{i:03d}{ext}"
                    old_path = os.path.join(source_dir, filename)
                    new_path = os.path.join(source_dir, new_name)
                    
                    try:
                        os.rename(old_path, new_path)
                        self.log_result(f"重命名: {filename} -> {new_name}")
                        renamed_count += 1
                    except Exception as e:
                        self.log_result(f"重命名失败 {filename}: {str(e)}")
                        
                self.log_result(f"批量重命名完成，共重命名 {renamed_count} 个文件")
                
            except Exception as e:
                self.log_result(f"批量重命名失败: {str(e)}")
                
        threading.Thread(target=rename, daemon=True).start()
        
    def search_files(self):
        """文件搜索"""
        def search():
            try:
                source_dir = self.source_path.get().strip()
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                self.log_result("开始文件搜索...")
                
                # 搜索条件（可以根据需要扩展）
                search_pattern = "*.txt"  # 默认搜索txt文件
                
                found_files = []
                for root, dirs, files in os.walk(source_dir):
                    if not self.winfo_exists():
                        break
                        
                    for file in files:
                        if file.endswith('.txt'):  # 简单示例
                            file_path = os.path.join(root, file)
                            found_files.append(file_path)
                            self.log_result(f"找到文件: {file_path}")
                            
                self.log_result(f"文件搜索完成，共找到 {len(found_files)} 个文件")
                
            except Exception as e:
                self.log_result(f"文件搜索失败: {str(e)}")
                
        threading.Thread(target=search, daemon=True).start()
        
    def find_duplicates(self):
        """查找重复文件"""
        def find():
            try:
                source_dir = self.source_path.get().strip()
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                self.log_result("开始查找重复文件...")
                
                # 计算文件哈希
                file_hashes = {}
                duplicate_count = 0
                
                for root, dirs, files in os.walk(source_dir):
                    if not self.winfo_exists():
                        break
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_hash = self.calculate_file_hash(file_path)
                            if file_hash in file_hashes:
                                self.log_result(f"发现重复文件: {file_path}")
                                self.log_result(f"  与文件重复: {file_hashes[file_hash]}")
                                duplicate_count += 1
                            else:
                                file_hashes[file_hash] = file_path
                        except Exception as e:
                            self.log_result(f"计算文件哈希失败 {file_path}: {str(e)}")
                            
                self.log_result(f"重复文件查找完成，发现 {duplicate_count} 个重复文件")
                
            except Exception as e:
                self.log_result(f"查找重复文件失败: {str(e)}")
                
        threading.Thread(target=find, daemon=True).start()
        
    def compress_files(self):
        """压缩文件"""
        def compress():
            try:
                source_dir = self.source_path.get().strip()
                target_dir = self.target_path.get().strip()
                
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                if not target_dir:
                    target_dir = os.path.dirname(source_dir)
                    
                self.log_result("开始压缩文件...")
                
                # 创建压缩文件名
                archive_name = f"archive_{int(time.time())}.zip"
                archive_path = os.path.join(target_dir, archive_name)
                
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(source_dir):
                        if not self.winfo_exists():
                            break
                            
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_dir)
                            zipf.write(file_path, arcname)
                            self.log_result(f"添加文件: {arcname}")
                            
                self.log_result(f"文件压缩完成: {archive_path}")
                
            except Exception as e:
                self.log_result(f"文件压缩失败: {str(e)}")
                
        threading.Thread(target=compress, daemon=True).start()
        
    def extract_files(self):
        """解压文件"""
        def extract():
            try:
                source_file = filedialog.askopenfilename(
                    title="选择压缩文件",
                    filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
                )
                
                if not source_file:
                    return
                    
                target_dir = self.target_path.get().strip()
                if not target_dir:
                    target_dir = os.path.dirname(source_file)
                    
                self.log_result("开始解压文件...")
                
                with zipfile.ZipFile(source_file, 'r') as zipf:
                    zipf.extractall(target_dir)
                    file_list = zipf.namelist()
                    
                    for file in file_list:
                        self.log_result(f"解压文件: {file}")
                        
                self.log_result(f"文件解压完成，共解压 {len(file_list)} 个文件")
                
            except Exception as e:
                self.log_result(f"文件解压失败: {str(e)}")
                
        threading.Thread(target=extract, daemon=True).start()
        
    def categorize_files(self):
        """文件分类"""
        def categorize():
            try:
                source_dir = self.source_path.get().strip()
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                self.log_result("开始文件分类...")
                
                # 文件类型映射
                type_mapping = {
                    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
                    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
                    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
                    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
                }
                
                categorized_count = 0
                for filename in os.listdir(source_dir):
                    if not self.winfo_exists():
                        break
                        
                    file_path = os.path.join(source_dir, filename)
                    if not os.path.isfile(file_path):
                        continue
                        
                    # 获取文件扩展名
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    # 确定文件类型
                    file_type = None
                    for category, extensions in type_mapping.items():
                        if ext in extensions:
                            file_type = category
                            break
                            
                    if file_type:
                        # 创建分类目录
                        category_dir = os.path.join(source_dir, file_type)
                        os.makedirs(category_dir, exist_ok=True)
                        
                        # 移动文件
                        new_path = os.path.join(category_dir, filename)
                        try:
                            shutil.move(file_path, new_path)
                            self.log_result(f"分类文件: {filename} -> {file_type}/")
                            categorized_count += 1
                        except Exception as e:
                            self.log_result(f"移动文件失败 {filename}: {str(e)}")
                            
                self.log_result(f"文件分类完成，共分类 {categorized_count} 个文件")
                
            except Exception as e:
                self.log_result(f"文件分类失败: {str(e)}")
                
        threading.Thread(target=categorize, daemon=True).start()
        
    def analyze_disk_space(self):
        """磁盘空间分析"""
        def analyze():
            try:
                source_dir = self.source_path.get().strip()
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                self.log_result("开始磁盘空间分析...")
                
                total_size = 0
                file_count = 0
                dir_count = 0
                
                for root, dirs, files in os.walk(source_dir):
                    if not self.winfo_exists():
                        break
                        
                    dir_count += len(dirs)
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            total_size += file_size
                            file_count += 1
                        except:
                            continue
                            
                self.log_result(f"磁盘空间分析完成:")
                self.log_result(f"  总大小: {self.format_bytes(total_size)}")
                self.log_result(f"  文件数量: {file_count}")
                self.log_result(f"  目录数量: {dir_count}")
                
            except Exception as e:
                self.log_result(f"磁盘空间分析失败: {str(e)}")
                
        threading.Thread(target=analyze, daemon=True).start()
        
    def manage_permissions(self):
        """权限管理"""
        def manage():
            try:
                self.log_result("权限管理功能需要系统管理员权限")
                self.log_result("建议使用操作系统自带的权限管理工具")
                self.log_result("Windows: 右键文件 -> 属性 -> 安全")
                self.log_result("Linux: chmod, chown 命令")
                
            except Exception as e:
                self.log_result(f"权限管理失败: {str(e)}")
                
        threading.Thread(target=manage, daemon=True).start()
        
    def sync_files(self):
        """文件同步"""
        def sync():
            try:
                source_dir = self.source_path.get().strip()
                target_dir = self.target_path.get().strip()
                
                if not source_dir or not os.path.exists(source_dir):
                    self.log_result("请选择有效的源目录")
                    return
                    
                if not target_dir:
                    self.log_result("请选择目标目录")
                    return
                    
                self.log_result("开始文件同步...")
                
                synced_count = 0
                for root, dirs, files in os.walk(source_dir):
                    if not self.winfo_exists():
                        break
                        
                    # 创建对应的目标目录
                    rel_path = os.path.relpath(root, source_dir)
                    target_subdir = os.path.join(target_dir, rel_path)
                    os.makedirs(target_subdir, exist_ok=True)
                    
                    for file in files:
                        source_file = os.path.join(root, file)
                        target_file = os.path.join(target_subdir, file)
                        
                        # 检查是否需要同步
                        if not os.path.exists(target_file) or \
                           os.path.getmtime(source_file) > os.path.getmtime(target_file):
                            try:
                                shutil.copy2(source_file, target_file)
                                self.log_result(f"同步文件: {file}")
                                synced_count += 1
                            except Exception as e:
                                self.log_result(f"同步文件失败 {file}: {str(e)}")
                                
                self.log_result(f"文件同步完成，共同步 {synced_count} 个文件")
                
            except Exception as e:
                self.log_result(f"文件同步失败: {str(e)}")
                
        threading.Thread(target=sync, daemon=True).start()
        
    def calculate_file_hash(self, file_path):
        """计算文件哈希值"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
        
    def format_bytes(self, bytes_value):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB" 
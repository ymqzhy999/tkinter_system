#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具核心模块
"""

import os
import shutil
import hashlib
import zipfile
import fnmatch
from pathlib import Path
import threading
import time

class FileUtils:
    @staticmethod
    def batch_rename(directory, pattern="*", prefix="", suffix="", extension=None):
        """批量重命名文件"""
        try:
            renamed_count = 0
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            
            for i, filename in enumerate(files, 1):
                name, ext = os.path.splitext(filename)
                
                # 应用扩展名过滤
                if extension and ext.lower() != extension.lower():
                    continue
                    
                # 应用模式过滤
                if not fnmatch.fnmatch(filename, pattern):
                    continue
                    
                # 生成新文件名
                new_name = f"{prefix}{name}{suffix}{ext}"
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1
                except Exception:
                    continue
                    
            return {
                "success": True,
                "renamed_count": renamed_count,
                "total_files": len(files)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def search_files(directory, pattern="*", file_type="all", recursive=True):
        """搜索文件"""
        try:
            found_files = []
            
            if recursive:
                for root, dirs, files in os.walk(directory):
                    if file_type in ["all", "files"]:
                        for file in files:
                            if fnmatch.fnmatch(file, pattern):
                                found_files.append(os.path.join(root, file))
                                
                    if file_type in ["all", "dirs"]:
                        for dir_name in dirs:
                            if fnmatch.fnmatch(dir_name, pattern):
                                found_files.append(os.path.join(root, dir_name))
            else:
                items = os.listdir(directory)
                for item in items:
                    item_path = os.path.join(directory, item)
                    
                    if file_type in ["all", "files"] and os.path.isfile(item_path):
                        if fnmatch.fnmatch(item, pattern):
                            found_files.append(item_path)
                            
                    if file_type in ["all", "dirs"] and os.path.isdir(item_path):
                        if fnmatch.fnmatch(item, pattern):
                            found_files.append(item_path)
                            
            return {
                "success": True,
                "files": found_files,
                "count": len(found_files)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def find_duplicates(directory, hash_algorithm="md5"):
        """查找重复文件"""
        try:
            file_hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_hash = FileUtils.calculate_file_hash(file_path, hash_algorithm)
                        if file_hash in file_hashes:
                            duplicates.append({
                                "hash": file_hash,
                                "files": [file_hashes[file_hash], file_path]
                            })
                        else:
                            file_hashes[file_hash] = file_path
                    except Exception:
                        continue
                        
            return {
                "success": True,
                "duplicates": duplicates,
                "duplicate_count": len(duplicates)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def compress_files(source_dir, output_path, compression_type="zip"):
        """压缩文件"""
        try:
            if compression_type.lower() == "zip":
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_dir)
                            zipf.write(file_path, arcname)
                            
            return {
                "success": True,
                "output_path": output_path,
                "compression_type": compression_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def extract_files(archive_path, extract_dir):
        """解压文件"""
        try:
            if zipfile.is_zipfile(archive_path):
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(extract_dir)
                    file_list = zipf.namelist()
                    
                return {
                    "success": True,
                    "extract_dir": extract_dir,
                    "extracted_files": file_list,
                    "file_count": len(file_list)
                }
            else:
                return {
                    "success": False,
                    "error": "不支持的文件格式"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def categorize_files(directory, category_mapping=None):
        """文件分类"""
        try:
            if category_mapping is None:
                category_mapping = {
                    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
                    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
                    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
                    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
                }
                
            categorized_count = 0
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if not os.path.isfile(file_path):
                    continue
                    
                # 获取文件扩展名
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                
                # 确定文件类型
                file_type = None
                for category, extensions in category_mapping.items():
                    if ext in extensions:
                        file_type = category
                        break
                        
                if file_type:
                    # 创建分类目录
                    category_dir = os.path.join(directory, file_type)
                    os.makedirs(category_dir, exist_ok=True)
                    
                    # 移动文件
                    new_path = os.path.join(category_dir, filename)
                    try:
                        shutil.move(file_path, new_path)
                        categorized_count += 1
                    except Exception:
                        continue
                        
            return {
                "success": True,
                "categorized_count": categorized_count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def analyze_disk_space(directory):
        """分析磁盘空间"""
        try:
            total_size = 0
            file_count = 0
            dir_count = 0
            type_sizes = {}
            
            for root, dirs, files in os.walk(directory):
                dir_count += len(dirs)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        file_count += 1
                        
                        # 按文件类型统计
                        _, ext = os.path.splitext(file)
                        ext = ext.lower()
                        if ext not in type_sizes:
                            type_sizes[ext] = 0
                        type_sizes[ext] += file_size
                    except Exception:
                        continue
                        
            return {
                "success": True,
                "total_size": total_size,
                "file_count": file_count,
                "dir_count": dir_count,
                "type_sizes": type_sizes
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def sync_files(source_dir, target_dir, sync_type="copy"):
        """同步文件"""
        try:
            synced_count = 0
            
            for root, dirs, files in os.walk(source_dir):
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
                            if sync_type == "copy":
                                shutil.copy2(source_file, target_file)
                            elif sync_type == "move":
                                shutil.move(source_file, target_file)
                            synced_count += 1
                        except Exception:
                            continue
                            
            return {
                "success": True,
                "synced_count": synced_count,
                "sync_type": sync_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    def calculate_file_hash(file_path, algorithm="md5"):
        """计算文件哈希值"""
        try:
            if algorithm.lower() == "md5":
                hash_obj = hashlib.md5()
            elif algorithm.lower() == "sha1":
                hash_obj = hashlib.sha1()
            elif algorithm.lower() == "sha256":
                hash_obj = hashlib.sha256()
            else:
                raise ValueError(f"不支持的哈希算法: {algorithm}")
                
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
                    
            return hash_obj.hexdigest()
        except Exception as e:
            raise Exception(f"计算文件哈希失败: {str(e)}")
            
    @staticmethod
    def format_bytes(bytes_value):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
        
    @staticmethod
    def get_file_info(file_path):
        """获取文件信息"""
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "is_file": os.path.isfile(file_path),
                "is_dir": os.path.isdir(file_path),
                "extension": os.path.splitext(file_path)[1]
            }
        except Exception as e:
            return {
                "error": str(e)
            }
            
    @staticmethod
    def monitor_directory(directory, callback, recursive=True):
        """监控目录变化（示例）"""
        # 这里可以实现目录监控功能
        # 由于需要复杂的文件系统监控，这里只是示例
        return "目录监控功能需要实现"
        
    @staticmethod
    def backup_files(source_dir, backup_dir, backup_type="full"):
        """备份文件"""
        try:
            timestamp = int(time.time())
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            if backup_type == "full":
                shutil.copytree(source_dir, backup_path)
            elif backup_type == "incremental":
                # 增量备份需要更复杂的实现
                pass
                
            return {
                "success": True,
                "backup_path": backup_path,
                "backup_type": backup_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 
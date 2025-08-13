#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统工具核心模块
"""

import os
import platform
import subprocess
import psutil
import tempfile
import shutil
from pathlib import Path

class SystemUtils:
    @staticmethod
    def get_system_info():
        """获取系统基本信息"""
        return {
            "操作系统": platform.system() + " " + platform.release(),
            "系统版本": platform.version(),
            "架构": platform.machine(),
            "处理器": platform.processor(),
            "主机名": platform.node(),
            "Python版本": platform.python_version()
        }
        
    @staticmethod
    def get_cpu_info():
        """获取CPU信息"""
        return {
            "物理核心数": psutil.cpu_count(logical=False),
            "逻辑核心数": psutil.cpu_count(logical=True),
            "当前频率": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "未知",
            "最大频率": f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "未知",
            "当前使用率": f"{psutil.cpu_percent()}%"
        }
        
    @staticmethod
    def get_memory_info():
        """获取内存信息"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "物理内存": {
                "总容量": SystemUtils.format_bytes(memory.total),
                "可用容量": SystemUtils.format_bytes(memory.available),
                "已使用": SystemUtils.format_bytes(memory.used),
                "使用率": f"{memory.percent}%"
            },
            "交换内存": {
                "总容量": SystemUtils.format_bytes(swap.total),
                "可用容量": SystemUtils.format_bytes(swap.free),
                "已使用": SystemUtils.format_bytes(swap.used),
                "使用率": f"{swap.percent}%"
            }
        }
        
    @staticmethod
    def get_disk_info():
        """获取磁盘信息"""
        disk_info = {}
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "total": SystemUtils.format_bytes(usage.total),
                    "used": SystemUtils.format_bytes(usage.used),
                    "free": SystemUtils.format_bytes(usage.free),
                    "percent": usage.percent
                }
            except PermissionError:
                continue
                
        return disk_info
        
    @staticmethod
    def get_network_info():
        """获取网络信息"""
        network_info = {}
        
        for interface, addresses in psutil.net_if_addrs().items():
            network_info[interface] = {}
            for addr in addresses:
                if addr.family == 2:  # IPv4
                    network_info[interface]["IPv4地址"] = addr.address
                    network_info[interface]["子网掩码"] = addr.netmask
                elif addr.family == 10:  # IPv6
                    network_info[interface]["IPv6地址"] = addr.address
                    
        return network_info
        
    @staticmethod
    def clean_temp_files():
        """清理临时文件"""
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
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.exists(file_path):
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                total_size += file_size
                                file_count += 1
                        except Exception:
                            continue
                            
        return {
            "file_count": file_count,
            "total_size": total_size,
            "formatted_size": SystemUtils.format_bytes(total_size)
        }
        
    @staticmethod
    def clean_browser_cache():
        """清理浏览器缓存"""
        cleaned_browsers = []
        
        # Chrome缓存
        chrome_cache = os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Cache")
        if os.path.exists(chrome_cache):
            try:
                shutil.rmtree(chrome_cache)
                cleaned_browsers.append("Chrome")
            except:
                pass
                
        # Firefox缓存
        firefox_cache = os.path.expanduser("~/AppData/Local/Mozilla/Firefox/Profiles")
        if os.path.exists(firefox_cache):
            try:
                for profile in os.listdir(firefox_cache):
                    cache_dir = os.path.join(firefox_cache, profile, "cache2")
                    if os.path.exists(cache_dir):
                        shutil.rmtree(cache_dir)
                cleaned_browsers.append("Firefox")
            except:
                pass
                
        return cleaned_browsers
        
    @staticmethod
    def optimize_system():
        """系统优化"""
        try:
            # 禁用不必要的服务
            services_to_disable = [
                "Themes",
                "WSearch",
                "SysMain"
            ]
            
            disabled_services = []
            for service in services_to_disable:
                try:
                    subprocess.run(
                        ["sc", "config", service, "start=disabled"],
                        capture_output=True,
                        shell=True
                    )
                    disabled_services.append(service)
                except:
                    continue
                    
            return disabled_services
        except:
            return []
            
    @staticmethod
    def check_system_files():
        """检查系统文件"""
        try:
            result = subprocess.run(
                ["sfc", "/scannow"],
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    def defrag_disk(drive="C:"):
        """磁盘碎片整理"""
        try:
            result = subprocess.run(
                ["defrag", drive, "/A"],
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    def get_process_list():
        """获取进程列表"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes
        
    @staticmethod
    def kill_process(pid):
        """结束进程"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except:
            return False
            
    @staticmethod
    def get_startup_programs():
        """获取启动程序"""
        try:
            import winreg
            startup_programs = []
            
            # 注册表启动项
            reg_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
            ]
            
            for reg_path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append({"name": name, "command": value})
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except:
                    continue
                    
            return startup_programs
        except ImportError:
            return []
            
    @staticmethod
    def format_bytes(bytes_value):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB" 
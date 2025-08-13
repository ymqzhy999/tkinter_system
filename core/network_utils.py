#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络工具核心模块
"""

import socket
import subprocess
import platform
import re
import threading
import time
import psutil

class NetworkUtils:
    @staticmethod
    def get_ip_config():
        """获取IP配置"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ipconfig", "/all"],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["ifconfig"],
                    capture_output=True,
                    text=True
                )
                
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"获取IP配置失败: {str(e)}"
            
    @staticmethod
    def ping_host(host, count=1):
        """Ping主机"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ping", "-n", str(count), host],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["ping", "-c", str(count), host],
                    capture_output=True,
                    text=True
                )
                
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    def is_port_open(host, port, timeout=2):
        """检查端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
            
    @staticmethod
    def scan_ports(host, ports):
        """扫描端口"""
        open_ports = []
        for port in ports:
            if NetworkUtils.is_port_open(host, port):
                open_ports.append(port)
        return open_ports
        
    @staticmethod
    def dns_lookup(domain):
        """DNS查询"""
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except socket.gaierror:
            return None
            
    @staticmethod
    def reverse_dns_lookup(ip):
        """反向DNS查询"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except socket.herror:
            return None
            
    @staticmethod
    def trace_route(target):
        """路由跟踪"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["tracert", target],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["traceroute", target],
                    capture_output=True,
                    text=True
                )
                
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"路由跟踪失败: {str(e)}"
            
    @staticmethod
    def get_network_interfaces():
        """获取网络接口信息"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["netsh", "interface", "show", "interface"],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["ip", "link", "show"],
                    capture_output=True,
                    text=True
                )
                
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"获取网络接口失败: {str(e)}"
            
    @staticmethod
    def get_network_connections():
        """获取网络连接信息"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["netstat", "-an"],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["netstat", "-tuln"],
                    capture_output=True,
                    text=True
                )
                
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"获取网络连接失败: {str(e)}"
            
    @staticmethod
    def get_default_gateway():
        """获取默认网关"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["route", "print"],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '0.0.0.0' in line and '0.0.0.0' in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                return parts[3]
            else:
                result = subprocess.run(
                    ["ip", "route", "show", "default"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', result.stdout)
                    if match:
                        return match.group(1)
                        
            return None
        except:
            return None
            
    @staticmethod
    def reset_network():
        """重置网络"""
        try:
            if platform.system() == "Windows":
                commands = [
                    ["ipconfig", "/release"],
                    ["ipconfig", "/renew"],
                    ["ipconfig", "/flushdns"],
                    ["netsh", "winsock", "reset"]
                ]
                
                results = []
                for cmd in commands:
                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk')
                    results.append({
                        "command": " ".join(cmd),
                        "success": result.returncode == 0,
                        "output": result.stdout if result.returncode == 0 else result.stderr
                    })
                    
                return results
            else:
                return "此功能仅支持Windows系统"
        except Exception as e:
            return f"重置网络失败: {str(e)}"
            
    @staticmethod
    def test_network_connectivity():
        """测试网络连接性"""
        tests = []
        
        # 测试本地回环
        if NetworkUtils.ping_host("127.0.0.1"):
            tests.append({"test": "本地回环", "status": "正常"})
        else:
            tests.append({"test": "本地回环", "status": "异常"})
            
        # 测试默认网关
        gateway = NetworkUtils.get_default_gateway()
        if gateway and NetworkUtils.ping_host(gateway):
            tests.append({"test": f"默认网关 ({gateway})", "status": "正常"})
        else:
            tests.append({"test": "默认网关", "status": "异常"})
            
        # 测试DNS服务器
        if NetworkUtils.ping_host("8.8.8.8"):
            tests.append({"test": "DNS服务器 (8.8.8.8)", "status": "正常"})
        else:
            tests.append({"test": "DNS服务器", "status": "异常"})
            
        # 测试外网连接
        if NetworkUtils.ping_host("www.baidu.com"):
            tests.append({"test": "外网连接", "status": "正常"})
        else:
            tests.append({"test": "外网连接", "status": "异常"})
            
        return tests
        
    @staticmethod
    def get_network_speed():
        """获取网络速度（示例）"""
        # 这里可以实现网络速度测试
        # 由于需要复杂的网络测试，这里只是示例
        return "网络速度测试功能需要实现"
        
    @staticmethod
    def monitor_network_traffic(duration=60):
        """监控网络流量"""
        try:
            # 获取初始网络统计
            initial_stats = psutil.net_io_counters()
            time.sleep(duration)
            final_stats = psutil.net_io_counters()
            
            # 计算流量
            bytes_sent = final_stats.bytes_sent - initial_stats.bytes_sent
            bytes_recv = final_stats.bytes_recv - initial_stats.bytes_recv
            
            return {
                "duration": duration,
                "bytes_sent": bytes_sent,
                "bytes_recv": bytes_recv,
                "bytes_sent_per_sec": bytes_sent / duration,
                "bytes_recv_per_sec": bytes_recv / duration
            }
        except:
            return None
            
    @staticmethod
    def check_port_availability(host, port):
        """检查端口可用性"""
        return NetworkUtils.is_port_open(host, port)
        
    @staticmethod
    def get_local_ip():
        """获取本地IP地址"""
        try:
            # 创建一个UDP套接字来获取本地IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
            
    @staticmethod
    def is_internet_available():
        """检查互联网连接"""
        try:
            # 尝试连接Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
            
    @staticmethod
    def get_network_usage():
        """获取网络使用情况"""
        try:
            stats = psutil.net_io_counters()
            return {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errin": stats.errin,
                "errout": stats.errout,
                "dropin": stats.dropin,
                "dropout": stats.dropout
            }
        except:
            return None 
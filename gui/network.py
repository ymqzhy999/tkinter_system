from tkinter import ttk, messagebox
import tkinter as tk
import socket
import subprocess
import threading
import platform
import re

class NetworkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scanning = False
        self.scan_thread = None
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
        
        # 创建网络工具按钮
        self.create_network_buttons(main_frame)
        
        # 创建结果显示区域
        self.create_result_area(main_frame)
        
    def create_network_buttons(self, parent):
        """创建网络工具按钮"""
        # 网络工具框架
        tools_frame = ttk.LabelFrame(parent, text="网络工具", padding="10")
        tools_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        tools_frame.columnconfigure(1, weight=1)
        
        # 第一行按钮
        row1_frame = ttk.Frame(tools_frame)
        row1_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row1_frame,
            text="查看IP配置",
            command=self.show_ip_config,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row1_frame,
            text="网络连接测试",
            command=self.test_network_connection,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row1_frame,
            text="端口扫描",
            command=self.scan_ports,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 第二行按钮
        row2_frame = ttk.Frame(tools_frame)
        row2_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row2_frame,
            text="DNS查询",
            command=self.dns_lookup,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row2_frame,
            text="路由跟踪",
            command=self.trace_route,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row2_frame,
            text="网络诊断",
            command=self.network_diagnosis,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 第三行按钮
        row3_frame = ttk.Frame(tools_frame)
        row3_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            row3_frame,
            text="查看网络接口",
            command=self.show_network_interfaces,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            row3_frame,
            text="查看网络统计",
            command=self.show_network_stats,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            row3_frame,
            text="重置网络",
            command=self.reset_network,
            width=20
        ).grid(row=0, column=2, padx=5)
        
        # 自定义测试框架
        custom_frame = ttk.LabelFrame(tools_frame, text="自定义测试", padding="10")
        custom_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 主机输入
        ttk.Label(custom_frame, text="主机/IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(custom_frame, width=20)
        self.host_entry.grid(row=0, column=1, padx=(10, 5), pady=5)
        self.host_entry.insert(0, "8.8.8.8")
        
        # 端口输入
        ttk.Label(custom_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.port_entry = ttk.Entry(custom_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=(10, 5), pady=5)
        self.port_entry.insert(0, "80")
        
        # 测试按钮
        ttk.Button(
            custom_frame,
            text="测试连接",
            command=self.custom_test
        ).grid(row=0, column=4, padx=5, pady=5)
        
    def create_result_area(self, parent):
        """创建结果显示区域"""
        # 结果框架
        result_frame = ttk.LabelFrame(parent, text="测试结果", padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # 配置网格权重
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 创建文本区域和滚动条
        text_frame = ttk.Frame(result_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(text_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 添加控制按钮
        control_frame = ttk.Frame(result_frame)
        control_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(
            control_frame,
            text="清除结果",
            command=self.clear_results
        ).grid(row=0, column=0, padx=5)
        
        # 端口扫描控制按钮
        self.scan_start_btn = ttk.Button(
            control_frame,
            text="开始扫描",
            command=self.scan_ports,
            state="disabled"
        )
        self.scan_start_btn.grid(row=0, column=1, padx=5)
        
        self.scan_stop_btn = ttk.Button(
            control_frame,
            text="停止扫描",
            command=self.stop_scan,
            state="disabled"
        )
        self.scan_stop_btn.grid(row=0, column=2, padx=5)
        
    def log_result(self, message):
        """添加结果消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        result_entry = f"[{timestamp}] {message}\n"
        
        self.result_text.insert(tk.END, result_entry)
        self.result_text.see(tk.END)
        self.update_idletasks()
        
    def clear_results(self):
        """清除结果"""
        self.result_text.delete(1.0, tk.END)
        
    def show_ip_config(self):
        """查看IP配置"""
        def show():
            try:
                self.log_result("正在获取IP配置信息...")
                
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
                    
                if result.returncode == 0:
                    self.log_result("IP配置信息:")
                    self.log_result(result.stdout)
                else:
                    self.log_result(f"获取IP配置失败: {result.stderr}")
                    
            except Exception as e:
                self.log_result(f"获取IP配置失败: {str(e)}")
                
        threading.Thread(target=show, daemon=True).start()
        
    def test_network_connection(self):
        """网络连接测试"""
        def test():
            try:
                self.log_result("开始网络连接测试...")
                
                # 测试本地回环
                self.log_result("测试本地回环 (127.0.0.1)...")
                if self.ping_host("127.0.0.1"):
                    self.log_result("✓ 本地回环正常")
                else:
                    self.log_result("✗ 本地回环异常")
                
                # 测试默认网关
                self.log_result("测试默认网关...")
                gateway = self.get_default_gateway()
                if gateway and self.ping_host(gateway):
                    self.log_result(f"✓ 默认网关 {gateway} 正常")
                else:
                    self.log_result("✗ 默认网关异常")
                
                # 测试DNS服务器
                self.log_result("测试DNS服务器 (8.8.8.8)...")
                if self.ping_host("8.8.8.8"):
                    self.log_result("✓ DNS服务器正常")
                else:
                    self.log_result("✗ DNS服务器异常")
                
                # 测试外网连接
                self.log_result("测试外网连接 (www.baidu.com)...")
                if self.ping_host("www.baidu.com"):
                    self.log_result("✓ 外网连接正常")
                else:
                    self.log_result("✗ 外网连接异常")
                    
            except Exception as e:
                self.log_result(f"网络连接测试失败: {str(e)}")
                
        threading.Thread(target=test, daemon=True).start()
        
    def scan_ports(self):
        """端口扫描"""
        if self.scanning:
            return
            
        self.scanning = True
        self.scan_start_btn.config(state="disabled")
        self.scan_stop_btn.config(state="normal")
        
        def scan():
            try:
                self.log_result("开始端口扫描...")
                
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
                target_host = "127.0.0.1"
                
                self.log_result(f"扫描主机: {target_host}")
                self.log_result("常用端口扫描结果:")
                
                for port in common_ports:
                    if not self.scanning:
                        self.log_result("端口扫描已停止")
                        break
                        
                    if self.is_port_open(target_host, port):
                        self.log_result(f"✓ 端口 {port} 开放")
                    else:
                        self.log_result(f"✗ 端口 {port} 关闭")
                        
                if self.scanning:
                    self.log_result("端口扫描完成")
                    
            except Exception as e:
                self.log_result(f"端口扫描失败: {str(e)}")
            finally:
                self.scanning = False
                self.scan_start_btn.config(state="normal")
                self.scan_stop_btn.config(state="disabled")
                
        self.scan_thread = threading.Thread(target=scan, daemon=True)
        self.scan_thread.start()
        
    def stop_scan(self):
        """停止端口扫描"""
        self.scanning = False
        self.log_result("正在停止端口扫描...")
        
    def dns_lookup(self):
        """DNS查询"""
        def lookup():
            try:
                self.log_result("开始DNS查询...")
                
                domains = ["www.baidu.com", "www.google.com", "www.github.com"]
                
                for domain in domains:
                    try:
                        ip = socket.gethostbyname(domain)
                        self.log_result(f"✓ {domain} -> {ip}")
                    except socket.gaierror:
                        self.log_result(f"✗ {domain} 解析失败")
                        
            except Exception as e:
                self.log_result(f"DNS查询失败: {str(e)}")
                
        threading.Thread(target=lookup, daemon=True).start()
        
    def trace_route(self):
        """路由跟踪"""
        def trace():
            try:
                self.log_result("开始路由跟踪...")
                
                target = "www.baidu.com"
                
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
                    
                if result.returncode == 0:
                    self.log_result(f"路由跟踪结果 ({target}):")
                    self.log_result(result.stdout)
                else:
                    self.log_result(f"路由跟踪失败: {result.stderr}")
                    
            except Exception as e:
                self.log_result(f"路由跟踪失败: {str(e)}")
                
        threading.Thread(target=trace, daemon=True).start()
        
    def network_diagnosis(self):
        """网络诊断"""
        def diagnose():
            try:
                self.log_result("开始网络诊断...")
                
                # 检查网络接口
                self.log_result("检查网络接口...")
                interfaces = self.get_network_interfaces()
                for interface, info in interfaces.items():
                    self.log_result(f"接口: {interface}")
                    for key, value in info.items():
                        self.log_result(f"  {key}: {value}")
                
                # 检查网络连接
                self.log_result("检查网络连接...")
                connections = self.get_network_connections()
                for conn in connections:
                    self.log_result(f"连接: {conn}")
                    
            except Exception as e:
                self.log_result(f"网络诊断失败: {str(e)}")
                
        threading.Thread(target=diagnose, daemon=True).start()
        
    def show_network_interfaces(self):
        """查看网络接口"""
        def show():
            try:
                self.log_result("正在获取网络接口信息...")
                
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
                
                if result.returncode == 0:
                    self.log_result("网络接口信息:")
                    self.log_result(result.stdout)
                else:
                    self.log_result(f"获取网络接口失败: {result.stderr}")
                    
            except Exception as e:
                self.log_result(f"获取网络接口失败: {str(e)}")
                
        threading.Thread(target=show, daemon=True).start()
        
    def show_network_stats(self):
        """查看网络统计"""
        def show():
            try:
                self.log_result("正在获取网络统计信息...")
                
                if platform.system() == "Windows":
                    result = subprocess.run(
                        ["netstat", "-e"],
                        capture_output=True,
                        text=True,
                        encoding='gbk'
                    )
                else:
                    result = subprocess.run(
                        ["netstat", "-i"],
                        capture_output=True,
                        text=True
                    )
                
                if result.returncode == 0:
                    self.log_result("网络统计信息:")
                    self.log_result(result.stdout)
                else:
                    self.log_result(f"获取网络统计失败: {result.stderr}")
                    
            except Exception as e:
                self.log_result(f"获取网络统计失败: {str(e)}")
                
        threading.Thread(target=show, daemon=True).start()
        
    def reset_network(self):
        """重置网络"""
        def reset():
            try:
                self.log_result("开始重置网络...")
                
                if platform.system() == "Windows":
                    # 重置网络配置
                    commands = [
                        ["ipconfig", "/release"],
                        ["ipconfig", "/renew"],
                        ["ipconfig", "/flushdns"],
                        ["netsh", "winsock", "reset"]
                    ]
                    
                    for cmd in commands:
                        self.log_result(f"执行命令: {' '.join(cmd)}")
                        result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk')
                        if result.returncode == 0:
                            self.log_result("✓ 命令执行成功")
                        else:
                            self.log_result(f"✗ 命令执行失败: {result.stderr}")
                            
                    self.log_result("网络重置完成，请重启计算机")
                    
            except Exception as e:
                self.log_result(f"重置网络失败: {str(e)}")
                
        threading.Thread(target=reset, daemon=True).start()
        
    def custom_test(self):
        """自定义测试"""
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not host:
            messagebox.showwarning("警告", "请输入主机地址")
            return
            
        if not port.isdigit():
            messagebox.showwarning("警告", "请输入有效的端口号")
            return
            
        def test():
            try:
                self.log_result(f"开始测试连接: {host}:{port}")
                
                # 测试端口连接
                if self.is_port_open(host, int(port)):
                    self.log_result(f"✓ 端口 {port} 开放")
                else:
                    self.log_result(f"✗ 端口 {port} 关闭")
                    
                # 测试Ping
                if self.ping_host(host):
                    self.log_result(f"✓ 主机 {host} 可达")
                else:
                    self.log_result(f"✗ 主机 {host} 不可达")
                    
            except Exception as e:
                self.log_result(f"自定义测试失败: {str(e)}")
                
        threading.Thread(target=test, daemon=True).start()
        
    def ping_host(self, host):
        """Ping主机"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ping", "-n", "1", host],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
            else:
                result = subprocess.run(
                    ["ping", "-c", "1", host],
                    capture_output=True,
                    text=True
                )
                
            return result.returncode == 0
        except:
            return False
            
    def is_port_open(self, host, port):
        """检查端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
            
    def get_default_gateway(self):
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
                        
        except:
            pass
            
        return None
        
    def get_network_interfaces(self):
        """获取网络接口信息"""
        interfaces = {}
        try:
            for interface, addresses in socket.getaddrinfo(socket.gethostname(), None):
                if interface not in interfaces:
                    interfaces[interface] = {}
                interfaces[interface]["地址"] = addresses[4][0]
        except:
            pass
        return interfaces
        
    def get_network_connections(self):
        """获取网络连接信息"""
        connections = []
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["netstat", "-an"],
                    capture_output=True,
                    text=True,
                    encoding='gbk'
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'ESTABLISHED' in line or 'LISTENING' in line:
                            connections.append(line.strip())
            else:
                result = subprocess.run(
                    ["netstat", "-tuln"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    connections = result.stdout.split('\n')
                    
        except:
            pass
        return connections 
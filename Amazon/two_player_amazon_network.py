# two_player_amazon_network.py
"""
Network module for Amazon Chess multiplayer
This should be saved as a separate file for testing
"""

import socket
import threading
import json
import time
import queue
from enum import Enum
from typing import Optional, Callable, Any
import logging
import miniupnpc
import struct

class NetworkRole(Enum):
    HOST = "host"
    CLIENT = "client"

class MessageType(Enum):
    CONNECTION_HANDSHAKE = "connection_handshake"
    GAME_INVITATION = "game_invitation"
    GAME_ACTION = "game_action"
    STATE_UPDATE = "state_update"
    MOVE_VALIDATION = "move_validation"
    CHAT_MESSAGE = "chat_message"
    CONNECTION_STATUS = "connection_status"
    ERROR = "error"

class NetworkManager:
    def __init__(self, role: NetworkRole, host_ip: str = 'localhost', host_port: int = 12345):
        self.role = role
        self.host_ip = host_ip
        self.host_port = host_port
        self.socket: Optional[socket.socket] = None
        self.connection: Optional[socket.socket] = None
        self.is_connected = False
        self.network_thread: Optional[threading.Thread] = None
        self.should_stop = False
        self._receive_buffer = b''  # 新增：接收缓冲区
        
        # 先设置日志
        self.setup_logging()
        
        # UPnP相关属性
        self.upnp = None
        self.upnp_mapped = False
        self.local_ip = self._get_local_ip()
        
        # 消息队列
        self.outgoing_queue = queue.Queue()
        self.incoming_queue = queue.Queue()
        
        # 回调函数
        self.on_message_received: Optional[Callable] = None
        self.on_connection_change: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        
        self.connection_attempts = 0
        self.max_retries = 5
        self.retry_delay = 1

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('AmazonChessNetwork')

    def _get_local_ip(self) -> str:
        """获取本地IP地址（不使用netifaces）"""
        try:
            # 方法1: 通过连接外部地址获取本地IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            self.logger.info(f"检测到本地IP: {local_ip}")
            return local_ip
        except Exception as e:
            self.logger.warning(f"方法1获取本地IP失败: {e}")
            try:
                # 方法2: 通过主机名获取
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                self.logger.info(f"通过主机名获取本地IP: {local_ip}")
                return local_ip
            except Exception as e2:
                self.logger.error(f"获取本地IP失败: {e2}")
                return '127.0.0.1'  # 回退到本地回路
    
    def detect_zerotier_network(self):
        """检测ZeroTier网络状态"""
        try:
            # 获取所有网络接口的IP
            all_ips = self._get_all_local_ips()
            
            # 筛选ZeroTier IP（包括你的两个网段）
            zt_ips = []
            zt_networks = [
                '10.147.', '10.244.', '10.255.', '10.3.70.', '192.168.196.'  # 添加你的两个网段
            ]
            
            for ip in all_ips:
                for network in zt_networks:
                    if ip.startswith(network):
                        zt_ips.append(ip)
                        break
            
            if zt_ips:
                self.zerotier_ips = zt_ips
                self.logger.info(f"检测到ZeroTier网络，IP地址: {', '.join(zt_ips)}")
                return zt_ips[0]  # 返回第一个IP
            
            self.logger.info("未检测到ZeroTier网络")
            return None
            
        except Exception as e:
            self.logger.warning(f"ZeroTier检测失败: {e}")
            return None
    
    def setup_upnp(self) -> bool:
        """设置UPnP端口转发"""
        if self.role != NetworkRole.HOST:
            return True
        
        if self.host_ip not in ['localhost', '127.0.0.1', '0.0.0.0']:
            self.logger.info("使用指定IP，跳过UPnP")
            return True
        
        try:
            self.logger.info("正在设置UPnP端口转发...")
            self.upnp = miniupnpc.UPnP()
            self.upnp.discoverdelay = 300
            
            self.logger.info("搜索UPnP设备...")
            devices = self.upnp.discover()
            self.logger.info(f"发现 {devices} 个UPnP设备")
            
            if devices == 0:
                self.logger.warning("未找到UPnP设备 - 可能的原因:")
                self.logger.warning("1. 路由器不支持UPnP")
                self.logger.warning("2. 路由器UPnP功能未启用") 
                self.logger.warning("3. 防火墙阻止了UPnP通信")
                return False
            
            # 尝试获取路由器信息
            try:
                router_info = self.upnp.selectigd()
                self.logger.info(f"路由器信息: {router_info}")
            except Exception as e:
                self.logger.warning(f"无法获取路由器详细信息: {e}")
            
            # 获取外部IP
            external_ip = self.upnp.externalipaddress()
            if not external_ip:
                self.logger.error("无法从路由器获取外部IP地址")
                return False
                
            self.logger.info(f"路由器报告的外部IP: {external_ip}")
            
            # 验证IP有效性
            if external_ip.startswith('10.') or external_ip.startswith('192.168.') or \
               (external_ip.startswith('172.') and 16 <= int(external_ip.split('.')[1]) <= 31):
                self.logger.warning(f"路由器返回的是私有IP {external_ip}，可能处于双重NAT环境")
            
            # 添加端口映射
            self.logger.info(f"添加端口映射: {self.host_port} -> {self.local_ip}:{self.host_port}")
            result = self.upnp.addportmapping(
                self.host_port, 'TCP', self.local_ip, self.host_port, 
                'Amazon Chess Game', ''
            )
            
            if result:
                self.upnp_mapped = True
                self.host_ip = external_ip
                self.logger.info(f"UPnP端口转发成功! 外部地址: {external_ip}:{self.host_port}")
                return True
            else:
                self.logger.error("UPnP端口映射失败 - 可能的原因:")
                self.logger.error("1. 路由器拒绝了UPnP请求")
                self.logger.error("2. 端口已被占用") 
                self.logger.error("3. 权限不足")
                return False
                
        except Exception as e:
            self.logger.error(f"UPnP设置失败: {str(e)}")
            self.logger.info("建议使用手动端口转发或第三方VPN工具")
            return False

    def _get_all_local_ips(self):
        """获取所有本地IP地址"""
        ips = []
        try:
            # 获取主机名
            hostname = socket.gethostname()
            # 获取所有IP地址
            all_ips = socket.getaddrinfo(hostname, None)
            for ip_info in all_ips:
                ip = ip_info[4][0]
                if ip not in ips and not ip.startswith('127.'):
                    ips.append(ip)
        except:
            pass
        
        # 如果没有找到，使用常见方法
        if not ips:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    local_ip = s.getsockname()[0]
                    if local_ip not in ips:
                        ips.append(local_ip)
            except:
                pass
                
        return ips

    def _get_public_ip(self) -> str:
        """获取公网IP地址"""
        try:
            import requests
            response = requests.get('http://httpbin.org/ip', timeout=5)
            return response.json()['origin']
        except:
            try:
                response = requests.get('http://api.ipify.org', timeout=5)
                return response.text.strip()
            except:
                return None

    
    def cleanup_upnp(self):
        """清理UPnP端口映射"""
        if self.upnp and self.upnp_mapped:
            try:
                self.logger.info("清理UPnP端口映射...")
                self.upnp.deleteportmapping(self.host_port, 'TCP')
                self.upnp_mapped = False
                self.logger.info("UPnP端口映射已清理")
            except Exception as e:
                self.logger.error(f"清理UPnP映射失败: {e}")
    
    def get_network_info(self):
        """获取完整的网络信息"""
        info = {
            "local_ip": self.local_ip,
            "host_ip": self.host_ip,
            "port": self.host_port,
            "upnp_status": "enabled" if self.upnp_mapped else "disabled",
            "zerotier_ips": self.zerotier_ips if hasattr(self, 'zerotier_ips') else []
        }
        
        # 获取公网IP
        public_ip = self._get_public_ip()
        if public_ip:
            info["public_ip"] = public_ip
        
        return info

    def _display_connection_info(self, network_info):
        """显示连接信息"""
        print("\n" + "="*60)
        print("🎮 游戏连接信息 - 主机已就绪")
        print("="*60)
        
        # ZeroTier连接（优先显示）
        zt_ips = network_info.get('zerotier_ips', [])
        if zt_ips:
            print("🔗 ZeroTier连接（推荐）:")
            for i, ip in enumerate(zt_ips, 1):
                print(f"   {i}. {ip}:{network_info['port']}")
            print("   告诉其他玩家使用上述任意地址连接")
        else:
            print("🔗 ZeroTier连接: 未检测到")
        
        # 局域网连接
        print(f"📍 局域网连接: {network_info['local_ip']}:{network_info['port']}")
        
        # 公网IP连接
        public_ip = network_info.get('public_ip')
        if public_ip:
            status = "✅ 已启用" if network_info['upnp_status'] == 'enabled' else "❌ 需要手动端口转发"
            print(f"🌐 公网连接: {public_ip}:{network_info['port']} ({status})")
        
        print("\n💡 连接说明:")
        if zt_ips:
            print("   • 其他玩家必须加入同一个ZeroTier网络")
            print("   • 他们在 https://my.zerotier.com/ 需要被授权")
            print("   • 然后他们可以使用上述ZeroTier IP连接")
        else:
            print("   • 只能在局域网内游戏")
            print("   • 或设置端口转发/使用VPN")
        
        print("="*60)

    def start(self):
        """启动网络管理器"""
        # 检测ZeroTier网络
        zt_ip = self.detect_zerotier_network()
        
        # 如果是主机，设置网络
        if self.role == NetworkRole.HOST:
            # 如果有ZeroTier IP，优先使用
            if zt_ip:
                self.logger.info(f"使用ZeroTier网络，IP: {zt_ip}")
                self.local_ip = zt_ip
                # 对于ZeroTier，不需要UPnP
                self.logger.info("ZeroTier网络已激活，跳过UPnP设置")
                self.upnp_mapped = True  # 标记为已映射，避免UPnP尝试
            else:
                # 没有ZeroTier，尝试UPnP
                upnp_success = self.setup_upnp()
                if not upnp_success:
                    self.logger.warning("UPnP设置失败，可能无法接受外部连接")
        
        self.network_thread = threading.Thread(target=self._network_worker, daemon=True)
        self.network_thread.start()
        self.logger.info(f"网络管理器启动为 {self.role.value}")


    def stop(self):
        """停止网络管理器"""
        self.should_stop = True
        self.is_connected = False
        
        # 清理UPnP
        self.cleanup_upnp()
        
        # 关闭连接
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.logger.info("网络管理器已停止")
    def _run_as_host(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 绑定到0.0.0.0
            bind_ip = '0.0.0.0'
            try:
                self.socket.bind((bind_ip, self.host_port))
                self.socket.listen(1)
                self.socket.settimeout(1.0)
                
                self.logger.info(f"主机监听在 {bind_ip}:{self.host_port}")
                
                # 获取网络信息
                network_info = self.get_network_info()
                
                # 显示所有可用的连接方式
                self._display_connection_info(network_info)
                
            except OSError as e:
                self.logger.error(f"无法绑定到端口 {self.host_port}: {e}")
                return
            
            while not self.should_stop:
                try:
                    if not self.is_connected:
                        client_socket, client_address = self.socket.accept()
                        self.connection = client_socket
                        self.is_connected = True
                        self._notify_connection_change(True, client_address)
                        self.logger.info(f"客户端连接来自 {client_address}")
                        
                        handshake = self._create_handshake_message()
                        self._send_message_direct(handshake)
                    
                    if self.is_connected:
                        self._handle_connection()
                        
                except socket.timeout:
                    continue
                except BlockingIOError:
                    continue
                except OSError as e:
                    if not self.should_stop:
                        self.logger.error(f"主机socket错误: {e}")
                        break
        except Exception as e:
            self.logger.error(f"主机执行错误: {e}")

    def show_port_forward_help(self):
        """显示端口转发帮助信息"""
        print("\n" + "="*60)
        print("网络连接帮助")
        print("="*60)
        
        print(f"本地IP: {self.local_ip}")
        print(f"公网IP: {self.host_ip}")
        print(f"端口: {self.host_port}")
        
        # 检查本地端口状态
        if self._check_local_port():
            print("✓ 本地端口已开放")
        else:
            print("✗ 本地端口未开放")
        
        print("\n=== 路由器端口转发设置指南 ===")
        
        # 常见路由器管理地址
        routers = [
            {"品牌": "TP-Link", "管理地址": "192.168.1.1 或 192.168.0.1", "用户名": "admin", "密码": "admin"},
            {"品牌": "华为", "管理地址": "192.168.3.1 或 192.168.1.1", "用户名": "admin", "密码": "admin"},
            {"品牌": "小米", "管理地址": "192.168.31.1", "用户名": "无", "密码": "无"},
            {"品牌": "腾达", "管理地址": "192.168.0.1", "用户名": "admin", "密码": "admin"},
            {"品牌": "水星", "管理地址": "192.168.1.1", "用户名": "admin", "密码": "admin"},
            {"品牌": "华硕", "管理地址": "192.168.50.1 或 192.168.1.1", "用户名": "admin", "密码": "admin"},
        ]
        
        print("常见路由器管理信息:")
        for router in routers:
            print(f"  {router['品牌']}: 地址 {router['管理地址']}, 用户: {router['用户名']}, 密码: {router['密码']}")
        
        print(f"\n端口转发设置步骤:")
        print(f"1. 打开浏览器，输入路由器管理地址")
        print(f"2. 登录路由器管理界面")
        print(f"3. 找到'端口转发'、'虚拟服务器'或'NAT设置'")
        print(f"4. 添加新规则:")
        print(f"   - 服务名称: Amazon Chess")
        print(f"   - 外部端口: {self.host_port}")
        print(f"   - 内部IP地址: {self.local_ip}")
        print(f"   - 内部端口: {self.host_port}")
        print(f"   - 协议: TCP (或选择Both)")
        print(f"5. 保存并启用规则")
        print(f"6. 重启游戏主机")
        
        print(f"\n连接信息:")
        print(f"外部玩家应该使用这个地址连接: {self.host_ip}:{self.host_port}")
        print(f"同一局域网玩家可以使用: {self.local_ip}:{self.host_port}")
        
        print("\n=== 快速解决方案 ===")
        print("方案1: 使用第三方VPN工具 (推荐)")
        print("  - ZeroTier (免费): https://www.zerotier.com/")
        print("  - Hamachi: https://www.vpn.net/")
        print("  - Radmin VPN: https://www.radmin-vpn.com/")
        print("  步骤: 安装 → 创建网络 → 邀请朋友加入 → 使用分配的IP连接")
        
        print("\n方案2: 使用云服务器")
        print("  - 在阿里云、腾讯云等购买云服务器")
        print("  - 在服务器上运行游戏")
        print("  - 所有玩家连接到服务器IP")
        
        print("\n方案3: 局域网游戏")
        print("  - 确保所有玩家在同一个WiFi/网络下")
        print(f"  - 使用本地IP连接: {self.local_ip}:{self.host_port}")
        
        print("\n" + "="*60)

    def _check_local_port(self):
        """检查本地端口是否开放"""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            result = test_socket.connect_ex((self.local_ip, self.host_port))
            test_socket.close()
            return result == 0
        except:
            return False

    # 其他现有方法保持不变...
    def _network_worker(self):
        try:
            if self.role == NetworkRole.HOST:
                self._run_as_host()
            else:
                self._run_as_client()
        except Exception as e:
            self.logger.error(f"Network worker error: {e}")
            if self.on_error:
                self.on_error(f"Network error: {e}")
    
    def _run_as_client(self):
        attempt = 0
        while not self.should_stop and attempt < self.max_retries:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10.0)
                
                self.logger.info(f"Connecting to {self.host_ip}:{self.host_port} (attempt {attempt + 1})")
                self.socket.connect((self.host_ip, self.host_port))
                
                self.connection = self.socket
                self.is_connected = True
                self._notify_connection_change(True, (self.host_ip, self.host_port))
                self.logger.info("Successfully connected to host")
                
                while self.is_connected and not self.should_stop:
                    self._handle_connection()
                break
                
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                attempt += 1
                self.connection_attempts = attempt
                self.logger.warning(f"Connection attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)
                else:
                    self.logger.error("Max connection attempts reached")
                    if self.on_error:
                        self.on_error(f"Failed to connect after {attempt} attempts")
                    break
    
    def _handle_connection(self):
        try:
            self._process_outgoing_queue()
            self.connection.settimeout(0.1)
            try:
                data = self._receive_data()
                if data:
                    messages = self._parse_messages(data)
                    for message in messages:
                        # 处理握手消息
                        if message.get('type') == MessageType.CONNECTION_HANDSHAKE.value:
                            self.logger.info("主机收到握手消息")
                            # 发送确认
                            self._send_message_direct({
                                'type': MessageType.CONNECTION_STATUS.value,
                                'data': {'status': 'connected'}
                            })
                        else:
                            # 处理其他消息
                            self._process_incoming_message(message)
            except socket.timeout:
                pass
            except ConnectionResetError:
                self._handle_disconnection("Connection reset by peer")
            except BrokenPipeError:
                self._handle_disconnection("Broken pipe - connection lost")
            except Exception as e:
                self.logger.error(f"Connection handling error: {e}")
                self._handle_disconnection(f"Connection error: {e}")
        except Exception as e:
            self.logger.error(f"Connection handling error: {e}")
            self._handle_disconnection(f"Connection error: {e}")

    def _process_outgoing_queue(self):
        try:
            while not self.outgoing_queue.empty():
                message = self.outgoing_queue.get_nowait()
                self._send_message_direct(message)
        except queue.Empty:
            pass
        except Exception as e:
            self.logger.error(f"Error sending queued message: {e}")
    
    def _send_message_direct(self, message: dict):
        if self.connection and self.is_connected:
            try:
                # 序列化消息
                serialized = json.dumps(message)
                # 添加长度前缀
                length_prefix = struct.pack('!I', len(serialized))
                # 发送长度前缀 + 序列化数据
                self.connection.sendall(length_prefix + serialized.encode('utf-8'))
            except Exception as e:
                self.logger.error(f"Error sending message: {e}")
                raise
    
    def _receive_data(self) -> Optional[bytes]:
        if not self.connection:
            return None
        try:
            data = self.connection.recv(4096)
            if not data:
                self._handle_disconnection("Connection closed by peer")
                return None
            return data
        except socket.timeout:
            return None
        except ConnectionResetError:
            self._handle_disconnection("Connection reset by peer")
            return None
        except Exception as e:
            self.logger.error(f"Error receiving data: {e}")
            return None
    
    def _parse_messages(self, data: bytes) -> list:
        """使用长度前缀解析消息，解决JSON分割问题"""
        messages = []
        self._receive_buffer += data  # 将新数据添加到缓冲区
        
        while len(self._receive_buffer) >= 4:  # 至少需要4字节长度前缀
            # 读取长度前缀
            length_prefix = self._receive_buffer[:4]
            message_length = struct.unpack('!I', length_prefix)[0]
            
            # 检查是否有足够的数据
            if len(self._receive_buffer) < 4 + message_length:
                break  # 数据不足，等待更多数据
                
            # 提取完整消息
            message_str = self._receive_buffer[4:4+message_length]
            self._receive_buffer = self._receive_buffer[4+message_length:]
            
            try:
                # 解析JSON
                message = json.loads(message_str.decode('utf-8'))
                messages.append(message)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse message: {e}")
                # 尝试恢复：移除第一个字节，继续解析
                self._receive_buffer = self._receive_buffer[1:]
                
        return messages
    
    def _process_incoming_message(self, message: dict):
        try:
            if not isinstance(message, dict) or 'type' not in message:
                self.logger.warning("Received invalid message format")
                return
            self.incoming_queue.put(message)
            if self.on_message_received:
                self.on_message_received(message)
        except Exception as e:
            self.logger.error(f"Error processing incoming message: {e}")
    
    def _handle_disconnection(self, reason: str):
        self.logger.warning(f"Disconnected: {reason}")
        self.is_connected = False
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        self._notify_connection_change(False, reason)
        if self.on_error and reason != "Connection closed by peer":
            self.on_error(f"Disconnected: {reason}")
    
    def _notify_connection_change(self, connected: bool, info: Any):
        if self.on_connection_change:
            self.on_connection_change(connected, info)
    
    def send_message(self, message_type: MessageType, data: dict):
        message = {
            'type': message_type.value,
            'timestamp': time.time(),
            'data': data
        }
        if message_type == MessageType.CONNECTION_HANDSHAKE:
            message['role'] = self.role.value
        self.outgoing_queue.put(message)
        self.logger.debug(f"Queued message: {message_type.value}")
    
    def get_messages(self) -> list:
        messages = []
        try:
            while not self.incoming_queue.empty():
                message = self.incoming_queue.get_nowait()
                messages.append(message)
        except queue.Empty:
            pass
        return messages
    
    def _create_handshake_message(self) -> dict:
        return {
            'type': MessageType.CONNECTION_HANDSHAKE.value,
            'version': '1.0',
            'role': self.role.value,
            'player_name': 'TestPlayer',
            'game_id': 'amazon_chess_v1',
            'timestamp': time.time()
        }

# Message creation functions
def create_game_action_message(action: str, player: str, from_pos: tuple, to_pos: tuple, move_id: str) -> dict:
    return {
        'type': MessageType.GAME_ACTION.value,
        'timestamp': time.time(),
        'data': {
            'action': action,
            'player': player,
            'from': from_pos,
            'to': to_pos,
            'move_id': move_id
        }
    }

def create_state_update_message(changes: list, current_player: str, phase: str, turn_number: int, game_over: bool = False, winner: str = None) -> dict:
    """Create a state update message with game over support"""
    return {
        'type': MessageType.STATE_UPDATE.value,
        'timestamp': time.time(),
        'data': {
            'changes': changes,
            'current_player': current_player,
            'phase': phase,
            'turn_number': turn_number,
            'game_over': game_over,  # ADD THIS
            'winner': winner         # ADD THIS
        }
    }

def create_move_validation_message(move_id: str, valid: bool, message: str, available_moves: list = None, available_shots: list = None) -> dict:
    return {
        'type': MessageType.MOVE_VALIDATION.value,
        'timestamp': time.time(),
        'data': {
            'move_id': move_id,
            'valid': valid,
            'message': message,
            'available_moves': available_moves or [],
            'available_shots': available_shots or []
        }
    }

def create_chat_message(player: str, message: str, message_id: str = None) -> dict:
    return {
        'type': MessageType.CHAT_MESSAGE.value,
        'timestamp': time.time(),
        'data': {
            'player': player,
            'message': message,
            'message_id': message_id or f"chat_{int(time.time() * 1000)}"
        }
    }

def create_connection_status_message(status: str, info: dict = None) -> dict:
    return {
        'type': MessageType.CONNECTION_STATUS.value,
        'timestamp': time.time(),
        'data': {
            'status': status,
            'info': info or {}
        }
    }

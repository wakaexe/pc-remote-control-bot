"""
Network utilities module
Handles network information and diagnostics
"""
import socket
import subprocess
import platform
import psutil
from typing import Dict, List
from utils.logger import logger

def get_network_info() -> str:
    """
    Get detailed network information

    Returns:
        Network info message
    """
    try:
        info = []

        # Hostname and IPs
        hostname = socket.gethostname()
        info.append(f"🖥️ **Hostname:** {hostname}")

        # Network interfaces
        interfaces = psutil.net_if_addrs()
        info.append("\n📡 **Сетевые интерфейсы:**")

        for interface_name, addresses in interfaces.items():
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    info.append(f"  • {interface_name}: {addr.address}")

        # Network stats
        net_io = psutil.net_io_counters()
        info.append(f"\n📊 **Статистика:**")
        info.append(f"  • Отправлено: {format_bytes(net_io.bytes_sent)}")
        info.append(f"  • Получено: {format_bytes(net_io.bytes_recv)}")

        return "\n".join(info)

    except Exception as e:
        logger.error(f"Failed to get network info: {e}")
        return f"❌ Ошибка: {str(e)}"

def ping(host: str, count: int = 4) -> str:
    """
    Ping a host

    Args:
        host: Hostname or IP address
        count: Number of ping attempts

    Returns:
        Ping result
    """
    try:
        system = platform.system()

        if system == "Windows":
            cmd = ["ping", "-n", str(count), host]
        else:
            cmd = ["ping", "-c", str(count), host]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout if result.stdout else result.stderr

        return f"🌐 **Ping {host}:**\n```\n{output[:1000]}\n```"

    except subprocess.TimeoutExpired:
        return f"❌ Превышено время ожидания при пинге {host}"
    except Exception as e:
        logger.error(f"Failed to ping: {e}")
        return f"❌ Ошибка: {str(e)}"

def get_active_connections() -> str:
    """
    Get active network connections

    Returns:
        List of connections
    """
    try:
        connections = psutil.net_connections(kind='inet')

        if not connections:
            return "📡 Нет активных соединений"

        info = ["📡 **Активные соединения:**\n"]

        # Group by status
        by_status = {}
        for conn in connections[:20]:  # Limit to 20
            status = conn.status
            if status not in by_status:
                by_status[status] = 0
            by_status[status] += 1

        for status, count in by_status.items():
            info.append(f"  • {status}: {count}")

        return "\n".join(info)

    except Exception as e:
        logger.error(f"Failed to get connections: {e}")
        return f"❌ Ошибка: {str(e)}"

def get_wifi_networks() -> str:
    """
    Get available WiFi networks (Windows only)

    Returns:
        List of WiFi networks
    """
    try:
        system = platform.system()

        if system != "Windows":
            return "❌ Доступно только на Windows"

        result = subprocess.run(
            ["netsh", "wlan", "show", "networks"],
            capture_output=True,
            text=True,
            encoding='cp866'  # Windows console encoding
        )

        if result.returncode != 0:
            return "❌ Не удалось получить список WiFi сетей"

        return f"📶 **WiFi сети:**\n```\n{result.stdout[:1500]}\n```"

    except Exception as e:
        logger.error(f"Failed to get WiFi networks: {e}")
        return f"❌ Ошибка: {str(e)}"

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

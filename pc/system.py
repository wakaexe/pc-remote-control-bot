"""
System control module
Handles shutdown, reboot, lock, sleep, and system information
"""
import platform
import subprocess
import psutil
import socket
from datetime import datetime, timedelta
from typing import Dict, Optional
from utils.logger import logger
from utils.helpers import format_bytes, get_external_ip

# Global variable to track shutdown process
_shutdown_process: Optional[subprocess.Popen] = None

def get_system_info() -> Dict[str, str]:
    """
    Get comprehensive system information

    Returns:
        Dictionary with system details
    """
    try:
        # CPU information (non-blocking)
        cpu_percent = psutil.cpu_percent(interval=0)
        cpu_count = psutil.cpu_count()

        # Memory information
        memory = psutil.virtual_memory()
        memory_used = format_bytes(memory.used)
        memory_total = format_bytes(memory.total)
        memory_percent = memory.percent

        # Disk information
        disk_info = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append(
                    f"{partition.device}: {format_bytes(usage.free)} free / {format_bytes(usage.total)} total ({usage.percent}% used)"
                )
            except PermissionError:
                continue

        # Network information
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        external_ip = get_external_ip()

        # Uptime
        uptime = get_uptime()

        info = {
            "OS": f"{platform.system()} {platform.release()}",
            "Architecture": platform.machine(),
            "Processor": platform.processor() or "Unknown",
            "CPU Usage": f"{cpu_percent}% ({cpu_count} cores)",
            "RAM": f"{memory_used} / {memory_total} ({memory_percent}% used)",
            "Disks": "\n".join(disk_info) if disk_info else "No disk info available",
            "Hostname": hostname,
            "Local IP": local_ip,
            "External IP": external_ip,
            "Uptime": uptime
        }

        return info

    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        return {"Error": str(e)}

def get_uptime() -> str:
    """
    Get system uptime

    Returns:
        Formatted uptime string
    """
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_duration = datetime.now() - boot_time

        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")

        return " ".join(parts)

    except Exception as e:
        logger.error(f"Failed to get uptime: {e}")
        return "Unknown"

def shutdown_pc(delay: int = 60) -> str:
    """
    Shutdown PC after delay

    Args:
        delay: Delay in seconds before shutdown

    Returns:
        Status message
    """
    global _shutdown_process

    try:
        system = platform.system()

        if system == "Windows":
            cmd = ["shutdown", "/s", "/t", str(delay), "/c", "Shutdown initiated by Telegram Bot"]
        elif system in ["Linux", "Darwin"]:
            cmd = ["sudo", "shutdown", "-h", f"+{delay//60}"]
        else:
            return f"❌ Unsupported OS: {system}"

        _shutdown_process = subprocess.Popen(cmd)
        logger.info(f"Shutdown scheduled in {delay} seconds")
        return f"✅ PC will shutdown in {delay} seconds. Use /abort to cancel."

    except Exception as e:
        logger.error(f"Failed to shutdown: {e}")
        return f"❌ Failed to shutdown: {str(e)}"

def reboot_pc(delay: int = 60) -> str:
    """
    Reboot PC after delay

    Args:
        delay: Delay in seconds before reboot

    Returns:
        Status message
    """
    global _shutdown_process

    try:
        system = platform.system()

        if system == "Windows":
            cmd = ["shutdown", "/r", "/t", str(delay), "/c", "Reboot initiated by Telegram Bot"]
        elif system in ["Linux", "Darwin"]:
            cmd = ["sudo", "shutdown", "-r", f"+{delay//60}"]
        else:
            return f"❌ Unsupported OS: {system}"

        _shutdown_process = subprocess.Popen(cmd)
        logger.info(f"Reboot scheduled in {delay} seconds")
        return f"✅ PC will reboot in {delay} seconds. Use /abort to cancel."

    except Exception as e:
        logger.error(f"Failed to reboot: {e}")
        return f"❌ Failed to reboot: {str(e)}"

def abort_shutdown() -> str:
    """
    Abort scheduled shutdown/reboot

    Returns:
        Status message
    """
    global _shutdown_process

    try:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["shutdown", "/a"], check=True)
        elif system in ["Linux", "Darwin"]:
            subprocess.run(["sudo", "shutdown", "-c"], check=True)
        else:
            return f"❌ Unsupported OS: {system}"

        _shutdown_process = None
        logger.info("Shutdown/reboot aborted")
        return "✅ Shutdown/reboot cancelled successfully."

    except subprocess.CalledProcessError:
        return "⚠️ No shutdown/reboot was scheduled."
    except Exception as e:
        logger.error(f"Failed to abort shutdown: {e}")
        return f"❌ Failed to abort: {str(e)}"

def lock_pc() -> str:
    """
    Lock the PC

    Returns:
        Status message
    """
    try:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
        elif system == "Linux":
            # Try multiple lock commands
            for cmd in [["loginctl", "lock-session"], ["xdg-screensaver", "lock"], ["gnome-screensaver-command", "-l"]]:
                try:
                    subprocess.run(cmd, check=True)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
        elif system == "Darwin":
            subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], check=True)
        else:
            return f"❌ Unsupported OS: {system}"

        logger.info("PC locked")
        return "🔒 PC locked successfully."

    except Exception as e:
        logger.error(f"Failed to lock PC: {e}")
        return f"❌ Failed to lock: {str(e)}"

def sleep_pc() -> str:
    """
    Put PC to sleep/hibernate

    Returns:
        Status message
    """
    try:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
        elif system == "Linux":
            subprocess.run(["systemctl", "suspend"], check=True)
        elif system == "Darwin":
            subprocess.run(["pmset", "sleepnow"], check=True)
        else:
            return f"❌ Unsupported OS: {system}"

        logger.info("PC going to sleep")
        return "😴 PC is going to sleep."

    except Exception as e:
        logger.error(f"Failed to sleep PC: {e}")
        return f"❌ Failed to sleep: {str(e)}"

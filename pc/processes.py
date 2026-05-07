"""
Process management module
Handles process listing and termination
"""
import psutil
from typing import List, Dict
from utils.logger import logger
from utils.helpers import format_bytes

def get_process_list(top_n: int = 10, sort_by: str = 'cpu') -> str:
    """
    Get list of running processes

    Args:
        top_n: Number of top processes to return
        sort_by: Sort by 'cpu' or 'memory'

    Returns:
        Formatted process list
    """
    try:
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu': pinfo['cpu_percent'] or 0,
                    'memory': pinfo['memory_info'].rss if pinfo['memory_info'] else 0,
                    'user': pinfo['username'] or 'N/A'
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort processes
        if sort_by == 'memory':
            processes.sort(key=lambda x: x['memory'], reverse=True)
        else:
            processes.sort(key=lambda x: x['cpu'], reverse=True)

        # Format output
        lines = [
            "🔄 **Top Processes**\n",
            f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'Memory':<12} {'User':<15}",
            "-" * 80
        ]

        for proc in processes[:top_n]:
            lines.append(
                f"{proc['pid']:<8} {proc['name'][:29]:<30} {proc['cpu']:<8.1f} {format_bytes(proc['memory']):<12} {proc['user'][:14]:<15}"
            )

        lines.append(f"\nTotal processes: {len(processes)}")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to get process list: {e}")
        return f"❌ Error: {str(e)}"

def kill_process(pid: int) -> str:
    """
    Kill process by PID

    Args:
        pid: Process ID to kill

    Returns:
        Status message
    """
    try:
        process = psutil.Process(pid)
        process_name = process.name()

        # Don't allow killing critical system processes
        critical_processes = ['System', 'csrss.exe', 'wininit.exe', 'services.exe',
                             'lsass.exe', 'winlogon.exe', 'systemd', 'init']

        if process_name in critical_processes:
            return f"⛔ Cannot kill critical system process: {process_name}"

        process.terminate()
        process.wait(timeout=5)

        logger.info(f"Killed process: {process_name} (PID: {pid})")
        return f"✅ Process terminated: {process_name} (PID: {pid})"

    except psutil.NoSuchProcess:
        return f"❌ Process not found: PID {pid}"
    except psutil.AccessDenied:
        return f"❌ Access denied: Cannot kill PID {pid} (insufficient permissions)"
    except psutil.TimeoutExpired:
        try:
            process.kill()
            return f"✅ Process forcefully killed: {process_name} (PID: {pid})"
        except:
            return f"❌ Failed to kill process: PID {pid}"
    except Exception as e:
        logger.error(f"Failed to kill process {pid}: {e}")
        return f"❌ Error: {str(e)}"

def get_process_info(pid: int) -> str:
    """
    Get detailed information about a process

    Args:
        pid: Process ID

    Returns:
        Formatted process information
    """
    try:
        process = psutil.Process(pid)

        info = {
            "PID": pid,
            "Name": process.name(),
            "Status": process.status(),
            "CPU %": f"{process.cpu_percent(interval=0.1)}%",
            "Memory": format_bytes(process.memory_info().rss),
            "Threads": process.num_threads(),
            "User": process.username(),
            "Created": process.create_time()
        }

        lines = [f"**Process Information (PID: {pid})**\n"]
        for key, value in info.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)

    except psutil.NoSuchProcess:
        return f"❌ Process not found: PID {pid}"
    except psutil.AccessDenied:
        return f"❌ Access denied: Cannot access PID {pid}"
    except Exception as e:
        logger.error(f"Failed to get process info for {pid}: {e}")
        return f"❌ Error: {str(e)}"

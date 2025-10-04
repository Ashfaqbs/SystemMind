import sys
import logging
import psutil
import platform
import shutil
import socket
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import datetime
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Universal OS Information Helper")

# Global variable to store OS information
OS_INFO = {
    "initialized": False,
    "system": None,
    "platform": None,
    "version": None,
    "architecture": None,
    "hostname": None,
    "python_version": None
}

def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def get_process_category(name: str) -> str:
    """Categorize processes for better understanding (works across all OS)"""
    name_lower = name.lower()
    
    # System processes (Windows, Linux, macOS)
    if any(sys_name in name_lower for sys_name in [
        'system', 'kernel', 'csrss', 'winlogon', 'services', 'lsass', 'svchost',
        'systemd', 'init', 'launchd', 'kworker', 'ksoftirqd', 'migration'
    ]):
        return "System Process"
    
    # Web browsers
    if any(browser in name_lower for browser in [
        'chrome', 'firefox', 'safari', 'edge', 'opera', 'brave', 'chromium', 'vivaldi'
    ]):
        return "Web Browser"
    
    # Media/Entertainment
    if any(media in name_lower for media in [
        'spotify', 'vlc', 'media', 'music', 'video', 'netflix', 'youtube', 
        'itunes', 'rhythmbox', 'audacity'
    ]):
        return "Media & Entertainment"
    
    # Development tools
    if any(dev in name_lower for dev in [
        'code', 'visual', 'git', 'python', 'node', 'java', 'docker', 'terminal',
        'vscode', 'pycharm', 'intellij', 'sublime', 'atom', 'vim', 'emacs'
    ]):
        return "Development Tool"
    
    # Office/Productivity
    if any(office in name_lower for office in [
        'word', 'excel', 'powerpoint', 'outlook', 'teams', 'slack', 'zoom', 
        'office', 'libreoffice', 'openoffice', 'notion', 'obsidian'
    ]):
        return "Office & Productivity"
    
    # Security
    if any(sec in name_lower for sec in [
        'antivirus', 'defender', 'security', 'firewall', 'malware', 'avast', 'norton'
    ]):
        return "Security Software"
    
    # Package managers and system tools
    if any(pkg in name_lower for pkg in [
        'apt', 'yum', 'dnf', 'pacman', 'brew', 'snap', 'flatpak'
    ]):
        return "Package Manager"
    
    return "Application"

def get_os_specific_commands() -> Dict[str, Any]:
    """Get OS-specific commands and paths"""
    system = platform.system()
    
    if system == "Windows":
        return {
            "clear_command": "cls",
            "path_separator": "\\",
            "temp_dir": os.environ.get('TEMP', 'C:\\Windows\\Temp'),
            "home_dir": os.environ.get('USERPROFILE', 'C:\\Users\\'),
            "package_manager": "winget or chocolatey",
            "shell": "PowerShell or CMD"
        }
    elif system == "Darwin":  # macOS
        return {
            "clear_command": "clear",
            "path_separator": "/",
            "temp_dir": "/tmp",
            "home_dir": os.environ.get('HOME', '/Users/'),
            "package_manager": "Homebrew",
            "shell": "bash or zsh"
        }
    else:  # Linux and other Unix-like
        return {
            "clear_command": "clear",
            "path_separator": "/",
            "temp_dir": "/tmp",
            "home_dir": os.environ.get('HOME', '/home/'),
            "package_manager": "apt/yum/dnf/pacman (distro-specific)",
            "shell": "bash or zsh"
        }

@mcp.tool
def initialize_os_connection() -> str:
    """
    Initialize and detect the operating system.
    This should be called first to establish OS-specific configurations.
    Works on Windows, macOS, Linux, and other Unix-like systems.
    """
    try:
        global OS_INFO
        
        # Get system information
        uname = platform.uname()
        
        OS_INFO = {
            "initialized": True,
            "system": uname.system,
            "platform": platform.platform(),
            "version": uname.version,
            "release": uname.release,
            "architecture": uname.machine,
            "hostname": socket.gethostname(),
            "python_version": platform.python_version(),
            "processor": uname.processor or platform.processor(),
        }
        
        # Get OS-specific configurations
        os_commands = get_os_specific_commands()
        OS_INFO.update(os_commands)
        
        result = "🔌 **OS CONNECTION INITIALIZED**\n\n"
        result += "✅ Successfully connected to your operating system!\n\n"
        
        result += "**DETECTED SYSTEM:**\n"
        result += f"• Operating System: {OS_INFO['system']}\n"
        result += f"• Platform: {OS_INFO['platform']}\n"
        result += f"• Architecture: {OS_INFO['architecture']}\n"
        result += f"• Computer Name: {OS_INFO['hostname']}\n"
        result += f"• Processor: {OS_INFO['processor']}\n"
        result += f"• Python Version: {OS_INFO['python_version']}\n\n"
        
        result += "**OS-SPECIFIC CONFIGURATION:**\n"
        result += f"• Shell: {OS_INFO['shell']}\n"
        result += f"• Package Manager: {OS_INFO['package_manager']}\n"
        result += f"• Home Directory: {OS_INFO['home_dir']}\n"
        result += f"• Temp Directory: {OS_INFO['temp_dir']}\n\n"
        
        # OS-specific notes
        if OS_INFO['system'] == "Windows":
            result += "**📝 WINDOWS NOTES:**\n"
            result += "• Use Task Manager (Ctrl+Shift+Esc) for detailed process info\n"
            result += "• Administrative privileges may be needed for some operations\n"
            result += "• Windows Defender is your built-in security software\n"
        elif OS_INFO['system'] == "Darwin":
            result += "**📝 macOS NOTES:**\n"
            result += "• Use Activity Monitor for detailed process info\n"
            result += "• Some operations may require sudo privileges\n"
            result += "• System Integrity Protection (SIP) may restrict certain actions\n"
        else:
            result += "**📝 LINUX/UNIX NOTES:**\n"
            result += "• Use top/htop commands for detailed process info\n"
            result += "• Some operations may require sudo privileges\n"
            result += "• Package manager varies by distribution\n"
        
        result += "\n✨ All tools are now ready to use!\n"
        
        logger.info(f"OS initialized: {OS_INFO['system']} {OS_INFO['release']}")
        return result
        
    except Exception as e:
        OS_INFO["initialized"] = False
        return f"❌ Error initializing OS connection: {str(e)}"

def check_initialization() -> Optional[str]:
    """Check if OS has been initialized"""
    if not OS_INFO.get("initialized", False):
        return "⚠️ Please run 'initialize_os_connection' first to detect your operating system!"
    return None

@mcp.tool
def get_running_processes(limit: int = 15) -> str:
    """
    Get information about all running processes on the machine.
    Works across Windows, macOS, Linux, and other Unix systems.
    
    Args:
        limit: Number of top processes to display (default: 15, max: 50)
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        limit = min(max(1, limit), 50)  # Ensure limit is between 1 and 50
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'create_time', 'status', 'username']):
            try:
                pinfo = proc.info
                category = get_process_category(pinfo['name'])
                
                # Calculate memory usage
                memory_mb = pinfo['memory_info'].rss / (1024 * 1024) if pinfo['memory_info'] else 0
                
                # Calculate running time
                create_time = datetime.datetime.fromtimestamp(pinfo['create_time'])
                running_time = datetime.datetime.now() - create_time
                
                # Get username (may fail on some systems)
                username = pinfo.get('username', 'N/A')
                if username and '\\' in username:
                    username = username.split('\\')[-1]  # Remove domain on Windows
                
                processes.append({
                    'name': pinfo['name'],
                    'pid': pinfo['pid'],
                    'category': category,
                    'memory_mb': memory_mb,
                    'cpu_percent': pinfo['cpu_percent'] or 0,
                    'status': pinfo['status'],
                    'running_time': str(running_time).split('.')[0],
                    'username': username
                })
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by memory usage
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        
        # Create summary
        total_processes = len(processes)
        categories = {}
        for proc in processes:
            cat = proc['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        result = f"🖥️ **SYSTEM PROCESSES OVERVIEW** ({OS_INFO['system']})\n\n"
        result += f"**Total Running Processes:** {total_processes}\n\n"
        
        result += "**Process Categories:**\n"
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            result += f"• {category}: {count} processes\n"
        
        result += f"\n**TOP {limit} MEMORY CONSUMERS:**\n"
        result += "*(These are using the most of your computer's memory)*\n\n"
        
        for i, proc in enumerate(processes[:limit], 1):
            memory_str = f"{proc['memory_mb']:.1f} MB"
            cpu_str = f"{proc['cpu_percent']:.1f}%"
            
            result += f"{i}. **{proc['name']}** ({proc['category']})\n"
            result += f"   - Memory: {memory_str} | CPU: {cpu_str} | Running: {proc['running_time']}\n"
            result += f"   - Status: {proc['status'].title()} | User: {proc['username']}\n\n"
        
        result += "\n**WHAT THIS MEANS:**\n"
        result += "• **Memory (MB)**: How much RAM each program is using\n"
        result += "• **CPU (%)**: How much processing power each program is using\n"
        result += "• **System Processes**: Core OS operations - usually safe to leave running\n"
        result += "• **Applications**: Programs you've opened - you can usually close these if needed\n"
        result += "• **High memory usage**: Normal for browsers, media apps, or if you have many tabs open\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting process information: {str(e)}"

@mcp.tool
def get_system_overview() -> str:
    """
    Get a comprehensive overview of your computer's specifications and current status.
    Works on Windows, macOS, Linux, and other Unix-like systems.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        # CPU info
        cpu_count = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        
        # Memory info
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk info
        disk = psutil.disk_usage('/')
        
        # Boot time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        
        result = f"🖥️ **YOUR COMPUTER OVERVIEW**\n\n"
        
        # Basic info
        result += f"**Computer Name:** {OS_INFO['hostname']}\n"
        result += f"**Operating System:** {OS_INFO['system']} {OS_INFO['release']}\n"
        result += f"**Machine Type:** {OS_INFO['architecture']}\n"
        result += f"**Processor:** {OS_INFO['processor']}\n\n"
        
        # CPU details
        result += f"**🔧 PROCESSOR (CPU) DETAILS:**\n"
        result += f"• Physical CPU cores: {cpu_count}\n"
        result += f"• Logical CPU cores (threads): {cpu_logical}\n"
        if cpu_freq:
            result += f"• Current CPU Speed: {cpu_freq.current:.0f} MHz\n"
            if hasattr(cpu_freq, 'max') and cpu_freq.max > 0:
                result += f"• Max CPU Speed: {cpu_freq.max:.0f} MHz\n"
        result += f"• Current CPU Usage: {cpu_percent}%\n\n"
        
        # Memory details
        result += f"**💾 MEMORY (RAM) DETAILS:**\n"
        result += f"• Total RAM: {format_bytes(memory.total)}\n"
        result += f"• Available RAM: {format_bytes(memory.available)}\n"
        result += f"• Used RAM: {format_bytes(memory.used)} ({memory.percent}%)\n"
        
        if swap.total > 0:
            result += f"• Swap/Page File: {format_bytes(swap.total)} ({swap.percent}% used)\n"
        
        # Memory status
        if memory.percent < 50:
            result += f"• Status: ✅ Good - Plenty of memory available\n\n"
        elif memory.percent < 80:
            result += f"• Status: ⚠️ Moderate - Consider closing some programs\n\n"
        else:
            result += f"• Status: 🔴 High - Your computer might be slow\n\n"
        
        # Disk details
        result += f"**💿 STORAGE DETAILS:**\n"
        result += f"• Total Storage: {format_bytes(disk.total)}\n"
        result += f"• Used Storage: {format_bytes(disk.used)} ({disk.percent}%)\n"
        result += f"• Free Storage: {format_bytes(disk.free)}\n"
        
        # Storage status
        if disk.percent < 70:
            result += f"• Status: ✅ Good - Plenty of space available\n\n"
        elif disk.percent < 90:
            result += f"• Status: ⚠️ Moderate - Consider cleaning up files\n\n"
        else:
            result += f"• Status: 🔴 Low - Running out of space!\n\n"
        
        # Uptime
        result += f"**⏰ SYSTEM STATUS:**\n"
        result += f"• Last Started: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"• Running For: {str(uptime).split('.')[0]}\n\n"
        
        # OS-specific tips
        if OS_INFO['system'] == "Windows":
            result += f"**💡 WINDOWS TIPS:**\n"
            result += f"• Press Win+X for quick system access\n"
            result += f"• Use Disk Cleanup to free up space\n"
        elif OS_INFO['system'] == "Darwin":
            result += f"**💡 macOS TIPS:**\n"
            result += f"• Check 'About This Mac' for more details\n"
            result += f"• Use Storage Management to optimize space\n"
        else:
            result += f"**💡 LINUX TIPS:**\n"
            result += f"• Use 'df -h' for disk info\n"
            result += f"• Use 'free -h' for memory info\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting system overview: {str(e)}"

@mcp.tool
def get_network_info() -> str:
    """
    Get information about your network connections and internet status.
    Works across all operating systems.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🌐 **NETWORK INFORMATION** ({OS_INFO['system']})\n\n"
        
        # Hostname and IP
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
            result += f"**Computer Name:** {hostname}\n"
            result += f"**Local IP Address:** {local_ip}\n\n"
        except:
            result += f"**Computer Name:** {hostname}\n"
            result += f"**Local IP Address:** Unable to determine\n\n"
        
        # Network interfaces
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        result += f"**🔌 NETWORK CONNECTIONS:**\n"
        for interface_name, addresses in interfaces.items():
            if interface_name in stats:
                is_up = stats[interface_name].isup
                status = "🟢 Connected" if is_up else "🔴 Disconnected"
                speed = stats[interface_name].speed
                speed_str = f" @ {speed}Mbps" if speed > 0 else ""
                
                result += f"• **{interface_name}**: {status}{speed_str}\n"
                
                for addr in addresses:
                    if addr.family == socket.AF_INET:  # IPv4
                        result += f"  - IPv4: {addr.address}\n"
                    elif addr.family == socket.AF_INET6:  # IPv6
                        result += f"  - IPv6: {addr.address}\n"
        
        result += f"\n"
        
        # Network usage
        net_io = psutil.net_io_counters()
        result += f"**📊 NETWORK USAGE (Since Boot):**\n"
        result += f"• Data Sent: {format_bytes(net_io.bytes_sent)}\n"
        result += f"• Data Received: {format_bytes(net_io.bytes_recv)}\n"
        result += f"• Packets Sent: {net_io.packets_sent:,}\n"
        result += f"• Packets Received: {net_io.packets_recv:,}\n"
        if net_io.errin > 0 or net_io.errout > 0:
            result += f"• Errors: {net_io.errin + net_io.errout}\n"
        result += f"\n"
        
        # Active connections (with error handling for different OS)
        try:
            connections = psutil.net_connections(kind='inet')
            active_connections = [conn for conn in connections if conn.status == 'ESTABLISHED']
            
            result += f"**🔗 ACTIVE CONNECTIONS:**\n"
            result += f"• Total Active Connections: {len(active_connections)}\n"
            
            # Group by remote address
            remote_addresses = {}
            for conn in active_connections[:10]:
                if conn.raddr:
                    addr = conn.raddr.ip
                    remote_addresses[addr] = remote_addresses.get(addr, 0) + 1
            
            if remote_addresses:
                result += f"• Connected to these servers:\n"
                for addr, count in list(remote_addresses.items())[:5]:
                    result += f"  - {addr} ({count} connection{'s' if count > 1 else ''})\n"
        except (psutil.AccessDenied, PermissionError):
            result += f"**🔗 ACTIVE CONNECTIONS:**\n"
            result += f"• Requires elevated privileges to view connection details\n"
        
        result += f"\n**WHAT THIS MEANS:**\n"
        result += f"• **Local IP**: Your computer's address on your home/office network\n"
        result += f"• **Connections**: Programs communicating with internet servers\n"
        result += f"• **Data Sent/Received**: How much internet data you've used\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting network information: {str(e)}"

@mcp.tool
def get_disk_usage() -> str:
    """
    Show detailed information about disk space usage and storage devices.
    Works on Windows (C:, D:, etc.), macOS (/), and Linux (/, /home, etc.).
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"💿 **STORAGE & DISK USAGE** ({OS_INFO['system']})\n\n"
        
        # Get all disk partitions
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Format device name
                device = partition.device
                mountpoint = partition.mountpoint
                
                result += f"**Drive: {device}** (Mounted at: {mountpoint})\n"
                result += f"• File System: {partition.fstype}\n"
                result += f"• Total Size: {format_bytes(usage.total)}\n"
                result += f"• Used: {format_bytes(usage.used)} ({usage.percent}%)\n"
                result += f"• Free: {format_bytes(usage.free)}\n"
                
                # Status indicator
                if usage.percent < 70:
                    result += f"• Status: ✅ Healthy\n"
                elif usage.percent < 90:
                    result += f"• Status: ⚠️ Getting Full\n"
                else:
                    result += f"• Status: 🔴 Almost Full!\n"
                
                result += f"\n"
                
            except (PermissionError, OSError):
                result += f"**Drive: {partition.device}** - No access or unavailable\n\n"
        
        # Disk I/O statistics
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io:
                result += f"**📊 DISK ACTIVITY (Since Boot):**\n"
                result += f"• Data Read: {format_bytes(disk_io.read_bytes)}\n"
                result += f"• Data Written: {format_bytes(disk_io.write_bytes)}\n"
                result += f"• Read Operations: {disk_io.read_count:,}\n"
                result += f"• Write Operations: {disk_io.write_count:,}\n\n"
        except Exception:
            pass  # Some systems don't support disk I/O counters
        
        result += f"**WHAT THIS MEANS:**\n"
        result += f"• **Total Size**: Maximum storage capacity\n"
        result += f"• **Used**: How much space is currently occupied\n"
        result += f"• **Free**: How much space is available for new files\n"
        result += f"• **Healthy**: Below 70% usage - good performance\n"
        result += f"• **Getting Full**: 70-90% usage - consider cleanup\n"
        result += f"• **Almost Full**: Above 90% - performance may suffer\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting disk usage: {str(e)}"

@mcp.tool
def get_performance_summary() -> str:
    """
    Get a quick performance summary of your computer.
    Universal health check for Windows, macOS, and Linux.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"⚡ **COMPUTER PERFORMANCE SUMMARY** ({OS_INFO['system']})\n\n"
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory
        memory = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # Load averages (Unix/Linux/Mac only)
        load_1min = None
        try:
            load_avg = psutil.getloadavg()
            load_1min = load_avg[0]
        except (AttributeError, OSError):
            pass  # Not available on Windows
        
        # Temperature (if available)
        temps = {}
        try:
            temps = psutil.sensors_temperatures()
        except (AttributeError, OSError):
            pass  # Not available on all systems
        
        # Overall health score
        health_score = 100
        issues = []
        warnings = []
        
        # Check CPU
        if cpu_percent > 80:
            health_score -= 30
            issues.append("🔴 High CPU usage - System may be slow")
        elif cpu_percent > 60:
            health_score -= 15
            warnings.append("⚠️ Moderate CPU usage")
        
        # Check Memory
        if memory.percent > 85:
            health_score -= 30
            issues.append("🔴 Low memory available - Close some programs")
        elif memory.percent > 70:
            health_score -= 15
            warnings.append("⚠️ Moderate memory usage")
        
        # Check Disk
        if disk.percent > 90:
            health_score -= 25
            issues.append("🔴 Very low disk space - Delete files urgently")
        elif disk.percent > 80:
            health_score -= 10
            warnings.append("⚠️ Low disk space")
        
        # Performance status
        if health_score >= 85:
            status = "🟢 EXCELLENT"
            advice = "Your computer is running very well!"
        elif health_score >= 70:
            status = "🟡 GOOD"
            advice = "Your computer is running well with minor issues."
        elif health_score >= 50:
            status = "🟠 FAIR"
            advice = "Your computer has some performance issues that need attention."
        else:
            status = "🔴 POOR"
            advice = "Your computer has significant performance issues!"
        
        result += f"**OVERALL STATUS: {status}**\n"
        result += f"**Health Score: {health_score}/100**\n\n"
        
        result += f"**📊 CURRENT METRICS:**\n"
        result += f"• CPU Usage: {cpu_percent}% ({cpu_count} cores available)\n"
        result += f"• Memory Usage: {memory.percent}% ({format_bytes(memory.available)} available)\n"
        result += f"• Disk Usage: {disk.percent}% ({format_bytes(disk.free)} free)\n"
        
        if load_1min is not None:
            load_per_core = load_1min / cpu_count
            result += f"• System Load: {load_1min:.2f} ({load_per_core:.2f} per core)\n"
        
        # Temperature info if available
        if temps:
            try:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current > 0:
                            result += f"• Temperature ({name}): {entry.current}°C\n"
                            if entry.current > 80:
                                warnings.append("⚠️ High system temperature detected")
                            break
                    break  # Only show first sensor
            except Exception:
                pass
        
        result += f"\n**🎯 ASSESSMENT:**\n{advice}\n\n"
        
        if issues:
            result += f"**🔴 CRITICAL ISSUES:**\n"
            for issue in issues:
                result += f"{issue}\n"
            result += f"\n"
        
        if warnings:
            result += f"**⚠️ WARNINGS:**\n"
            for warning in warnings:
                result += f"{warning}\n"
            result += f"\n"
        
        # Quick fixes
        result += f"**🔧 RECOMMENDED ACTIONS:**\n"
        if cpu_percent > 70:
            result += f"• Close unnecessary programs and browser tabs\n"
        if memory.percent > 70:
            result += f"• Restart memory-intensive applications\n"
            result += f"• Consider restarting your computer\n"
        if disk.percent > 80:
            result += f"• Delete temporary files and downloads\n"
            result += f"• Uninstall unused programs\n"
            result += f"• Empty recycle bin/trash\n"
        
        if not issues and not warnings:
            result += f"• No immediate action needed - system is healthy!\n"
            result += f"• Continue regular maintenance\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting performance summary: {str(e)}"

@mcp.tool
def get_temperature_info() -> str:
    """
    Get temperature information from system sensors (when available).
    Works on systems with temperature monitoring support (mainly Linux and some macOS).
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🌡️ **SYSTEM TEMPERATURE MONITORING** ({OS_INFO['system']})\n\n"
        
        try:
            temps = psutil.sensors_temperatures()
            
            if not temps:
                result += "⚠️ No temperature sensors detected on this system.\n\n"
                result += "**NOTE:**\n"
                if OS_INFO['system'] == "Windows":
                    result += "• Windows requires specialized software for temperature monitoring\n"
                    result += "• Try tools like: HWMonitor, Core Temp, or Open Hardware Monitor\n"
                elif OS_INFO['system'] == "Darwin":
                    result += "• macOS has limited temperature sensor access\n"
                    result += "• Try tools like: iStat Menus or Intel Power Gadget\n"
                else:
                    result += "• Make sure lm-sensors is installed: sudo apt install lm-sensors\n"
                    result += "• Run: sudo sensors-detect\n"
                return result
            
            result += "**DETECTED SENSORS:**\n\n"
            
            for name, entries in temps.items():
                result += f"**{name.upper()}:**\n"
                for entry in entries:
                    temp = entry.current
                    label = entry.label or "Sensor"
                    
                    # Temperature status
                    if temp < 50:
                        status = "✅ Cool"
                    elif temp < 70:
                        status = "🟡 Warm"
                    elif temp < 85:
                        status = "🟠 Hot"
                    else:
                        status = "🔴 Very Hot!"
                    
                    result += f"• {label}: {temp}°C ({temp * 9/5 + 32:.1f}°F) - {status}\n"
                    
                    # Show high/critical temps if available
                    if entry.high:
                        result += f"  - Warning threshold: {entry.high}°C\n"
                    if entry.critical:
                        result += f"  - Critical threshold: {entry.critical}°C\n"
                
                result += "\n"
            
            result += "**TEMPERATURE GUIDE:**\n"
            result += "• **< 50°C**: Optimal - System is cool\n"
            result += "• **50-70°C**: Normal - System is warm under load\n"
            result += "• **70-85°C**: High - Consider improving cooling\n"
            result += "• **> 85°C**: Critical - Risk of thermal throttling or damage\n\n"
            
            result += "**COOLING TIPS:**\n"
            result += "• Ensure proper ventilation around your computer\n"
            result += "• Clean dust from vents and fans\n"
            result += "• Use laptop on hard, flat surfaces\n"
            result += "• Consider a cooling pad for laptops\n"
            
        except AttributeError:
            result += "⚠️ Temperature monitoring not supported on this platform.\n"
            result += f"Your OS ({OS_INFO['system']}) may not provide sensor access through this interface.\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting temperature information: {str(e)}"

@mcp.tool
def get_battery_info() -> str:
    """
    Get battery status and information (for laptops and devices with batteries).
    Works on Windows, macOS, and Linux laptops.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🔋 **BATTERY INFORMATION** ({OS_INFO['system']})\n\n"
        
        if not hasattr(psutil, 'sensors_battery'):
            result += "⚠️ Battery monitoring not available on this system.\n"
            return result
        
        battery = psutil.sensors_battery()
        
        if battery is None:
            result += "⚠️ No battery detected.\n"
            result += "This is likely a desktop computer or battery information is unavailable.\n"
            return result
        
        # Battery percentage
        percent = battery.percent
        plugged = battery.power_plugged
        
        # Status
        if plugged:
            if percent >= 100:
                status = "🟢 Fully Charged"
            else:
                status = "🔌 Charging"
        else:
            if percent > 50:
                status = "🟢 Discharging"
            elif percent > 20:
                status = "🟡 Discharging"
            else:
                status = "🔴 Low Battery"
        
        result += f"**BATTERY STATUS: {status}**\n\n"
        result += f"**CURRENT CHARGE:**\n"
        result += f"• Battery Level: {percent}%\n"
        result += f"• Power Plugged In: {'Yes' if plugged else 'No'}\n"
        
        # Time remaining
        if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
            hours, remainder = divmod(battery.secsleft, 3600)
            minutes = remainder // 60
            
            if plugged:
                result += f"• Time until full charge: {int(hours)}h {int(minutes)}m\n"
            else:
                result += f"• Time remaining: {int(hours)}h {int(minutes)}m\n"
        elif plugged and percent >= 100:
            result += f"• Status: Fully charged\n"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            result += f"• Status: Calculating...\n"
        
        result += "\n**BATTERY HEALTH:**\n"
        if percent < 20 and not plugged:
            result += "🔴 **Warning**: Battery is low! Plug in your charger soon.\n"
        elif percent < 10 and not plugged:
            result += "🔴 **Critical**: Battery is critically low! Plug in immediately.\n"
        elif percent > 80 and plugged:
            result += "✅ Battery is well charged.\n"
        else:
            result += "✅ Battery is in good condition.\n"
        
        result += "\n**BATTERY CARE TIPS:**\n"
        result += "• Avoid fully draining the battery regularly\n"
        result += "• Keep charge between 20-80% for optimal battery life\n"
        result += "• Avoid extreme temperatures\n"
        result += "• Unplug once fully charged (if possible)\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting battery information: {str(e)}"

@mcp.tool
def check_startup_programs() -> str:
    """
    Show programs that start automatically when your computer boots up.
    Helps identify what might be slowing down startup time.
    Works across Windows, macOS, and Linux.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🚀 **STARTUP PROGRAMS** ({OS_INFO['system']})\n\n"
        
        # Get processes and check which ones started recently (likely startup programs)
        boot_time = psutil.boot_time()
        startup_window = 300  # 5 minutes after boot
        startup_threshold = boot_time + startup_window
        
        startup_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'create_time', 'memory_info']):
            try:
                pinfo = proc.info
                
                if pinfo['create_time'] <= startup_threshold:
                    category = get_process_category(pinfo['name'])
                    memory_mb = pinfo['memory_info'].rss / (1024 * 1024) if pinfo['memory_info'] else 0
                    
                    startup_processes.append({
                        'name': pinfo['name'],
                        'category': category,
                        'memory_mb': memory_mb,
                        'start_time': datetime.datetime.fromtimestamp(pinfo['create_time'])
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by memory usage
        startup_processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        
        # Calculate stats
        total_startup = len(startup_processes)
        total_memory = sum(p['memory_mb'] for p in startup_processes)
        
        result += f"**STARTUP SUMMARY:**\n"
        result += f"• Total startup programs: {total_startup}\n"
        result += f"• Memory used by startup programs: {total_memory:.1f} MB\n"
        result += f"• System boot time: {datetime.datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Group by category
        categories = {}
        for proc in startup_processes:
            cat = proc['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(proc)
        
        result += f"**STARTUP PROGRAMS BY CATEGORY:**\n\n"
        
        for category, procs in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            result += f"**{category}** ({len(procs)} programs):\n"
            
            # Sort processes in category by memory usage
            procs.sort(key=lambda x: x['memory_mb'], reverse=True)
            
            for proc in procs[:5]:  # Show top 5 in each category
                result += f"• {proc['name']} - {proc['memory_mb']:.1f} MB\n"
            
            if len(procs) > 5:
                result += f"• ... and {len(procs) - 5} more\n"
            result += f"\n"
        
        # Performance impact assessment
        result += f"**🎯 STARTUP PERFORMANCE ASSESSMENT:**\n"
        
        if total_startup < 20:
            result += f"✅ **Good**: Reasonable number of startup programs\n"
        elif total_startup < 40:
            result += f"⚠️ **Moderate**: Quite a few startup programs\n"
        else:
            result += f"🔴 **High**: Many startup programs may slow boot time\n"
        
        if total_memory < 500:
            result += f"✅ **Good**: Startup programs use reasonable memory\n"
        elif total_memory < 1000:
            result += f"⚠️ **Moderate**: Startup programs use significant memory\n"
        else:
            result += f"🔴 **High**: Startup programs use a lot of memory\n"
        
        result += f"\n**💡 HOW TO MANAGE STARTUP PROGRAMS:**\n"
        if OS_INFO['system'] == "Windows":
            result += f"• Press Ctrl+Shift+Esc → Startup tab\n"
            result += f"• Or: Settings → Apps → Startup\n"
        elif OS_INFO['system'] == "Darwin":
            result += f"• System Preferences → Users & Groups → Login Items\n"
            result += f"• Or: System Settings → General → Login Items\n"
        else:
            result += f"• Check ~/.config/autostart/ directory\n"
            result += f"• Or use your desktop environment's startup settings\n"
        
        result += f"\n**⚠️ RECOMMENDATIONS:**\n"
        result += f"• **System Processes**: Essential - don't disable\n"
        result += f"• **Security Software**: Important - keep enabled\n"
        result += f"• **Applications**: Disable if not used daily\n"
        result += f"• **Development Tools**: Disable unless actively coding\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error checking startup programs: {str(e)}"

@mcp.tool
def get_user_info() -> str:
    """
    Get information about system users and current user session.
    Works on Windows, macOS, and Linux.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"👤 **USER INFORMATION** ({OS_INFO['system']})\n\n"
        
        # Current user
        current_user = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USER', os.environ.get('USERNAME', 'Unknown'))
        
        result += f"**CURRENT USER:**\n"
        result += f"• Username: {current_user}\n"
        result += f"• Home Directory: {Path.home()}\n"
        
        # Try to get additional user info
        try:
            import pwd
            user_info = pwd.getpwnam(current_user)
            result += f"• User ID (UID): {user_info.pw_uid}\n"
            result += f"• Group ID (GID): {user_info.pw_gid}\n"
            result += f"• Real Name: {user_info.pw_gecos}\n"
            result += f"• Shell: {user_info.pw_shell}\n"
        except (ImportError, KeyError):
            # Windows or user not found
            result += f"• User ID: {os.getuid() if hasattr(os, 'getuid') else 'N/A'}\n"
        
        result += f"\n**LOGGED IN USERS:**\n"
        
        # Get all logged in users
        users = psutil.users()
        if users:
            user_sessions = {}
            for user in users:
                username = user.name
                if username not in user_sessions:
                    user_sessions[username] = []
                
                started = datetime.datetime.fromtimestamp(user.started)
                session_info = {
                    'terminal': user.terminal or 'GUI',
                    'host': user.host or 'local',
                    'started': started
                }
                user_sessions[username].append(session_info)
            
            for username, sessions in user_sessions.items():
                result += f"• **{username}** ({len(sessions)} session{'s' if len(sessions) > 1 else ''})\n"
                for session in sessions[:3]:  # Show up to 3 sessions per user
                    result += f"  - {session['terminal']} from {session['host']} since {session['started'].strftime('%H:%M:%S')}\n"
        else:
            result += "• No active user sessions detected\n"
        
        result += f"\n**ENVIRONMENT INFO:**\n"
        result += f"• Working Directory: {os.getcwd()}\n"
        result += f"• Temp Directory: {OS_INFO['temp_dir']}\n"
        
        # Path info
        path_var = os.environ.get('PATH', '')
        path_count = len(path_var.split(os.pathsep)) if path_var else 0
        result += f"• PATH entries: {path_count}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting user information: {str(e)}"

@mcp.tool
def find_large_files(directory: str = None, min_size_mb: float = 100, limit: int = 20) -> str:
    """
    Find large files in a directory to help identify what's taking up disk space.
    
    Args:
        directory: Directory to search (default: user's home directory)
        min_size_mb: Minimum file size in MB to report (default: 100)
        limit: Maximum number of files to return (default: 20)
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        if directory is None:
            directory = str(Path.home())
        
        directory = Path(directory)
        if not directory.exists():
            return f"❌ Directory not found: {directory}"
        
        result = f"🔍 **LARGE FILES SEARCH** ({OS_INFO['system']})\n\n"
        result += f"**Search Parameters:**\n"
        result += f"• Directory: {directory}\n"
        result += f"• Minimum Size: {min_size_mb} MB\n"
        result += f"• Limit: {limit} files\n"
        result += f"• Max Depth: 5 levels (to prevent timeout)\n\n"
        
        result += "⏳ Scanning directory... (this may take a moment)\n\n"
        
        # Find large files with depth limit and timeout protection
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        scanned_count = 0
        error_count = 0
        max_files_to_scan = 10000  # Prevent scanning too many files
        max_depth = 5  # Limit recursion depth
        
        def get_depth(path, base):
            """Calculate depth relative to base directory"""
            try:
                rel = path.relative_to(base)
                return len(rel.parts)
            except ValueError:
                return 0
        
        try:
            # Use iterdir for controlled iteration instead of rglob
            directories_to_scan = [directory]
            visited = set()
            
            while directories_to_scan and scanned_count < max_files_to_scan:
                try:
                    current_dir = directories_to_scan.pop(0)
                    
                    # Prevent infinite loops
                    try:
                        real_path = current_dir.resolve()
                        if real_path in visited:
                            continue
                        visited.add(real_path)
                    except (OSError, RuntimeError):
                        continue
                    
                    # Check depth
                    depth = get_depth(current_dir, directory)
                    if depth > max_depth:
                        continue
                    
                    # Scan current directory
                    try:
                        for item in current_dir.iterdir():
                            scanned_count += 1
                            
                            # Safety check
                            if scanned_count >= max_files_to_scan:
                                result += f"⚠️ Reached scan limit ({max_files_to_scan} items). Results may be incomplete.\n\n"
                                break
                            
                            try:
                                if item.is_file():
                                    try:
                                        size = item.stat().st_size
                                        if size >= min_size_bytes:
                                            modified = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                                            large_files.append({
                                                'path': item,
                                                'size': size,
                                                'modified': modified
                                            })
                                    except (OSError, PermissionError):
                                        error_count += 1
                                        continue
                                        
                                elif item.is_dir():
                                    # Add subdirectory to scan queue if within depth limit
                                    if depth < max_depth:
                                        directories_to_scan.append(item)
                                        
                            except (PermissionError, OSError):
                                error_count += 1
                                continue
                                
                    except (PermissionError, OSError):
                        error_count += 1
                        continue
                        
                except Exception as e:
                    error_count += 1
                    continue
                    
        except Exception as e:
            return f"❌ Error during scan: {str(e)}\nScanned {scanned_count} items before error."
        
        result += f"**Scan Statistics:**\n"
        result += f"• Items scanned: {scanned_count:,}\n"
        if error_count > 0:
            result += f"• Permission errors: {error_count}\n"
        result += "\n"
        
        # Sort by size
        large_files.sort(key=lambda x: x['size'], reverse=True)
        large_files = large_files[:limit]
        
        if not large_files:
            result += f"✅ No files larger than {min_size_mb} MB found in this directory.\n"
            result += "\n**💡 TIP:** Try:\n"
            result += f"• Lowering min_size_mb (currently {min_size_mb} MB)\n"
            result += f"• Searching a different directory\n"
            result += f"• Checking if you have permission to access the files\n"
            return result
        
        result += f"**FOUND {len(large_files)} LARGE FILE(S):**\n\n"
        
        total_size = sum(f['size'] for f in large_files)
        result += f"**Total size of listed files: {format_bytes(total_size)}**\n\n"
        
        for i, file_info in enumerate(large_files, 1):
            # Better error handling for relative path
            try:
                rel_path = file_info['path'].relative_to(directory)
                location = rel_path.parent if rel_path.parent != Path('.') else "Root of search directory"
            except ValueError:
                # If path is not relative to directory, use parent
                location = file_info['path'].parent
            
            result += f"{i}. **{file_info['path'].name}**\n"
            result += f"   - Size: {format_bytes(file_info['size'])}\n"
            result += f"   - Location: {location}\n"
            result += f"   - Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            # Add file extension info
            ext = file_info['path'].suffix
            if ext:
                result += f"   - Type: {ext.upper()[1:]} file\n"
            else:
                result += f"   - Type: No extension\n"
            
            # Add full path for reference
            result += f"   - Full Path: {file_info['path']}\n\n"
        
        result += "**💡 TIPS:**\n"
        result += "• Review these files to see if they're still needed\n"
        result += "• Consider moving large media files to external storage\n"
        result += "• Delete temporary or duplicate files\n"
        result += "• Compress archives if not frequently accessed\n"
        result += "• Use Windows Storage Sense for automated cleanup\n"
        
        if error_count > 0:
            result += f"\n⚠️ Note: {error_count} files/folders were skipped due to permission errors.\n"
        
        return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"❌ Error finding large files: {str(e)}\n\nDetails:\n{error_details}"

@mcp.tool
def get_installed_software() -> str:
    """
    List installed software and applications on the system.
    Note: Results vary by operating system and available tools.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"📦 **INSTALLED SOFTWARE** ({OS_INFO['system']})\n\n"
        
        if OS_INFO['system'] == "Windows":
            result += "**NOTE**: Listing all installed software requires registry access.\n"
            result += "Showing currently running applications instead:\n\n"
            
            # Get unique application names from running processes
            apps = set()
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and not name.startswith(('System', 'svchost')):
                        apps.add(name)
                except:
                    continue
            
            result += f"**Running Applications: {len(apps)}**\n"
            for app in sorted(apps)[:50]:
                result += f"• {app}\n"
            
            result += f"\n**To see all installed software:**\n"
            result += "• Windows Settings → Apps → Installed apps\n"
            result += "• Or use: Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* in PowerShell\n"
            
        elif OS_INFO['system'] == "Darwin":
            result += "**macOS Applications:**\n\n"
            
            # Check common application directories
            app_dirs = [Path('/Applications'), Path.home() / 'Applications']
            apps = []
            
            for app_dir in app_dirs:
                if app_dir.exists():
                    for app in app_dir.glob('*.app'):
                        apps.append(app.name.replace('.app', ''))
            
            result += f"**Found {len(apps)} applications:**\n"
            for app in sorted(apps)[:50]:
                result += f"• {app}\n"
            
            if len(apps) > 50:
                result += f"• ... and {len(apps) - 50} more\n"
            
            result += f"\n**Package Manager Apps (Homebrew):**\n"
            homebrew_path = Path('/usr/local/bin/brew')
            if homebrew_path.exists() or Path('/opt/homebrew/bin/brew').exists():
                result += "• Homebrew is installed\n"
                result += "• Run 'brew list' in terminal to see installed packages\n"
            else:
                result += "• Homebrew not detected\n"
                
        else:  # Linux
            result += "**Linux Package Information:**\n\n"
            
            # Try to detect package manager
            package_managers = {
                'dpkg': '/usr/bin/dpkg',  # Debian/Ubuntu
                'rpm': '/usr/bin/rpm',     # Red Hat/Fedora
                'pacman': '/usr/bin/pacman'  # Arch
            }
            
            detected_pm = None
            for pm, path in package_managers.items():
                if Path(path).exists():
                    detected_pm = pm
                    break
            
            if detected_pm:
                result += f"• Package Manager Detected: {detected_pm}\n\n"
                result += f"**To list installed packages:**\n"
                
                if detected_pm == 'dpkg':
                    result += "• Run: dpkg -l\n"
                    result += "• Or: apt list --installed\n"
                elif detected_pm == 'rpm':
                    result += "• Run: rpm -qa\n"
                    result += "• Or: dnf list installed\n"
                elif detected_pm == 'pacman':
                    result += "• Run: pacman -Q\n"
            else:
                result += "• Package manager not detected\n"
            
            # Check for Snap and Flatpak
            if Path('/usr/bin/snap').exists():
                result += "\n• Snap is installed (run: snap list)\n"
            if Path('/usr/bin/flatpak').exists():
                result += "• Flatpak is installed (run: flatpak list)\n"
        
        result += f"\n**Running Unique Applications: {len(set(p.info['name'] for p in psutil.process_iter(['name'])))}**\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting installed software: {str(e)}"

@mcp.tool
def clean_temp_files(dry_run: bool = True) -> str:
    """
    Clean temporary files to free up disk space.
    
    Args:
        dry_run: If True, only shows what would be deleted (default: True for safety)
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🧹 **TEMPORARY FILES CLEANUP** ({OS_INFO['system']})\n\n"
        
        if dry_run:
            result += "**DRY RUN MODE** - Nothing will be deleted\n"
            result += "Set dry_run=False to actually delete files\n\n"
        else:
            result += "⚠️ **LIVE MODE** - Files will be permanently deleted!\n\n"
        
        temp_dirs = []
        
        # Get system temp directory
        temp_dirs.append(Path(OS_INFO['temp_dir']))
        
        # Add OS-specific temp locations
        if OS_INFO['system'] == "Windows":
            temp_dirs.extend([
                Path(os.environ.get('TEMP', 'C:\\Windows\\Temp')),
                Path(os.environ.get('TMP', 'C:\\Windows\\Temp')),
                Path.home() / 'AppData' / 'Local' / 'Temp'
            ])
        elif OS_INFO['system'] == "Darwin":
            temp_dirs.extend([
                Path('/private/var/tmp'),
                Path.home() / 'Library' / 'Caches'
            ])
        else:
            temp_dirs.extend([
                Path('/tmp'),
                Path('/var/tmp'),
                Path.home() / '.cache'
            ])
        
        # Remove duplicates
        temp_dirs = list(set(temp_dirs))
        
        total_files = 0
        total_size = 0
        deleted_files = 0
        deleted_size = 0
        errors = []
        
        result += "**Scanning temporary directories:**\n"
        
        for temp_dir in temp_dirs:
            if not temp_dir.exists():
                continue
            
            result += f"• {temp_dir}\n"
            
            try:
                for item in temp_dir.glob('*'):
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            total_files += 1
                            total_size += size
                            
                            if not dry_run:
                                try:
                                    item.unlink()
                                    deleted_files += 1
                                    deleted_size += size
                                except Exception as e:
                                    errors.append(f"{item.name}: {str(e)}")
                    except (PermissionError, OSError):
                        continue
            except (PermissionError, OSError) as e:
                errors.append(f"Cannot access {temp_dir}: {str(e)}")
        
        result += f"\n**RESULTS:**\n"
        result += f"• Total temp files found: {total_files}\n"
        result += f"• Total size: {format_bytes(total_size)}\n"
        
        if not dry_run:
            result += f"• Files deleted: {deleted_files}\n"
            result += f"• Space freed: {format_bytes(deleted_size)}\n"
            
            if errors:
                result += f"\n**⚠️ Errors encountered: {len(errors)}**\n"
                for error in errors[:10]:
                    result += f"• {error}\n"
                if len(errors) > 10:
                    result += f"• ... and {len(errors) - 10} more errors\n"
        else:
            result += f"• Would free up: {format_bytes(total_size)}\n"
        
        result += f"\n**💡 ADDITIONAL CLEANUP OPTIONS:**\n"
        
        if OS_INFO['system'] == "Windows":
            result += "• Run Disk Cleanup (cleanmgr.exe)\n"
            result += "• Settings → System → Storage → Temporary files\n"
            result += "• Empty Recycle Bin\n"
        elif OS_INFO['system'] == "Darwin":
            result += "• Empty Trash\n"
            result += "• Clear browser caches\n"
            result += "• Use 'Manage Storage' in About This Mac\n"
        else:
            result += "• Empty Trash: rm -rf ~/.local/share/Trash/*\n"
            result += "• Clear package manager cache\n"
            result += "• Clear browser caches\n"
        
        result += "\n**⚠️ SAFETY NOTE:**\n"
        result += "Some temporary files may be in use by running programs.\n"
        result += "Consider closing applications before cleanup.\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error cleaning temp files: {str(e)}"

@mcp.tool
def get_system_services() -> str:
    """
    List system services and their status.
    Works on Windows (services), macOS (launchd), and Linux (systemd/init).
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"⚙️ **SYSTEM SERVICES** ({OS_INFO['system']})\n\n"
        
        if OS_INFO['system'] == "Windows":
            result += "**Windows Services Information:**\n\n"
            result += "This tool shows running processes. For full service management:\n"
            result += "• Press Win+R, type 'services.msc'\n"
            result += "• Or use PowerShell: Get-Service\n\n"
            
            # Show service-like processes
            service_processes = []
            for proc in psutil.process_iter(['name', 'status']):
                try:
                    name = proc.info['name'].lower()
                    if 'svchost' in name or 'service' in name:
                        service_processes.append(proc.info['name'])
                except:
                    continue
            
            result += f"**Service-related processes running: {len(service_processes)}**\n"
            
        elif OS_INFO['system'] == "Darwin":
            result += "**macOS Services (launchd):**\n\n"
            result += "**To view services:**\n"
            result += "• User services: launchctl list\n"
            result += "• System services: sudo launchctl list\n"
            result += "• Service locations:\n"
            result += "  - ~/Library/LaunchAgents (user)\n"
            result += "  - /Library/LaunchAgents (system)\n"
            result += "  - /Library/LaunchDaemons (system daemons)\n\n"
            
        else:  # Linux
            result += "**Linux Services:**\n\n"
            
            # Check for systemd
            if Path('/bin/systemctl').exists() or Path('/usr/bin/systemctl').exists():
                result += "**Service Manager: systemd**\n\n"
                result += "**Common commands:**\n"
                result += "• List all services: systemctl list-units --type=service\n"
                result += "• List running services: systemctl list-units --type=service --state=running\n"
                result += "• Check service status: systemctl status <service>\n"
                result += "• Start service: sudo systemctl start <service>\n"
                result += "• Stop service: sudo systemctl stop <service>\n"
                result += "• Enable on boot: sudo systemctl enable <service>\n\n"
            else:
                result += "**Service Manager: init/other**\n"
                result += "• Check /etc/init.d/ for service scripts\n"
                result += "• Use: service --status-all\n\n"
        
        # Show some common system daemons/services that are running
        result += "**Common System Processes Running:**\n"
        common_services = {
            'ssh': 'SSH Server',
            'docker': 'Docker Container Runtime',
            'nginx': 'Nginx Web Server',
            'apache': 'Apache Web Server',
            'mysql': 'MySQL Database',
            'postgres': 'PostgreSQL Database',
            'mongo': 'MongoDB Database',
            'redis': 'Redis Cache',
            'cron': 'Task Scheduler',
            'systemd': 'System Manager',
        }
        
        found_services = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                for service_key, service_name in common_services.items():
                    if service_key in name and service_name not in found_services:
                        found_services.append(service_name)
            except:
                continue
        
        if found_services:
            for service in sorted(found_services):
                result += f"• ✅ {service}\n"
        else:
            result += "• No common services detected in process list\n"
        
        result += f"\n**💡 TIP:**\n"
        result += "Services are background programs that run automatically.\n"
        result += "Be careful when stopping or disabling services - some are essential!\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting system services: {str(e)}"

@mcp.tool
def check_security_status() -> str:
    """
    Check basic security status of the system.
    Includes firewall, antivirus, and security updates info.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🔒 **SECURITY STATUS** ({OS_INFO['system']})\n\n"
        
        security_score = 100
        issues = []
        recommendations = []
        
        # Check for security-related processes
        security_processes = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if any(sec in name for sec in ['defender', 'antivirus', 'firewall', 'security', 'avast', 'norton', 'mcafee', 'kaspersky']):
                    security_processes.append(proc.info['name'])
            except:
                continue
        
        result += "**SECURITY SOFTWARE:**\n"
        if security_processes:
            result += f"✅ Detected security software running:\n"
            # FIX: Convert set to list before slicing
            for proc in list(set(security_processes))[:5]:
                result += f"• {proc}\n"
        else:
            result += "⚠️ No security software detected in running processes\n"
            security_score -= 20
            issues.append("No antivirus software detected")
        
        result += "\n"
        
        # OS-specific security checks
        if OS_INFO['system'] == "Windows":
            result += "**WINDOWS SECURITY:**\n"
            result += "• Check Windows Security: Win+I → Privacy & Security → Windows Security\n"
            result += "• Ensure Windows Defender is active\n"
            result += "• Check Windows Update for security patches\n"
            result += "• Verify Firewall is enabled\n\n"
            
            # Check if Windows Defender process is running
            defender_running = any('MsMpEng' in proc.info['name'] or 'SecurityHealthService' in proc.info['name'] 
                                 for proc in psutil.process_iter(['name']))
            if defender_running:
                result += "✅ Windows Defender appears to be running\n"
            else:
                result += "⚠️ Windows Defender may not be active\n"
                recommendations.append("Enable Windows Defender")
            
        elif OS_INFO['system'] == "Darwin":
            result += "**macOS SECURITY:**\n"
            result += "• macOS has built-in security features (XProtect, Gatekeeper)\n"
            result += "• Check: System Preferences → Security & Privacy\n"
            result += "• Ensure FileVault encryption is enabled\n"
            result += "• Keep macOS updated\n"
            result += "• Enable Firewall in Security settings\n\n"
            
            # Check for XProtect
            result += "✅ macOS built-in protections (XProtect, Gatekeeper)\n"
            
        else:  # Linux
            result += "**LINUX SECURITY:**\n"
            result += "• Check firewall status: sudo ufw status (Ubuntu/Debian)\n"
            result += "• Or: sudo firewall-cmd --state (RHEL/CentOS)\n"
            result += "• Keep system updated: sudo apt update && sudo apt upgrade\n"
            result += "• Check for SELinux/AppArmor status\n"
            result += "• Review sudo access and user permissions\n\n"
            
            # Check for common security tools
            security_tools = []
            if Path('/usr/sbin/ufw').exists():
                security_tools.append("UFW Firewall available")
            if Path('/usr/bin/fail2ban-client').exists():
                security_tools.append("Fail2ban installed")
            if Path('/usr/sbin/sestatus').exists():
                security_tools.append("SELinux available")
            
            if security_tools:
                result += "**Detected Security Tools:**\n"
                for tool in security_tools:
                    result += f"• ✅ {tool}\n"
            result += "\n"
        
        # Check system uptime (for updates)
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        days_since_boot = uptime.days
        
        result += "**SYSTEM UPDATES:**\n"
        if days_since_boot > 30:
            result += f"⚠️ System uptime: {days_since_boot} days\n"
            result += "• Consider restarting to apply pending updates\n"
            security_score -= 10
            recommendations.append("Restart system to apply updates")
        else:
            result += f"✅ System uptime: {days_since_boot} days (recently restarted)\n"
        
        result += "\n**GENERAL SECURITY RECOMMENDATIONS:**\n"
        result += "• Keep your OS and software updated\n"
        result += "• Use strong, unique passwords\n"
        result += "• Enable two-factor authentication where possible\n"
        result += "• Be cautious with email attachments and downloads\n"
        result += "• Regular backups of important data\n"
        result += "• Don't disable security software\n"
        
        # Security score
        result += f"\n**🎯 SECURITY SCORE: {security_score}/100**\n"
        if security_score >= 80:
            result += "✅ Good - Your system has basic security measures\n"
        elif security_score >= 60:
            result += "⚠️ Fair - Consider improving security\n"
        else:
            result += "🔴 Poor - Security needs attention!\n"
        
        if issues:
            result += f"\n**⚠️ ISSUES FOUND:**\n"
            for issue in issues:
                result += f"• {issue}\n"
        
        if recommendations:
            result += f"\n**💡 RECOMMENDATIONS:**\n"
            for rec in recommendations:
                result += f"• {rec}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error checking security status: {str(e)}"

@mcp.tool
def get_resource_monitor(interval_seconds: int = 5) -> str:
    """
    Monitor system resources in real-time for a specified interval.
    Shows CPU, memory, disk, and network usage trends.
    
    Args:
        interval_seconds: How long to monitor (1-30 seconds, default: 5)
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        interval_seconds = max(1, min(interval_seconds, 30))  # Limit to 1-30 seconds
        
        result = f"📊 **REAL-TIME RESOURCE MONITOR** ({OS_INFO['system']})\n\n"
        result += f"Monitoring system for {interval_seconds} seconds...\n\n"
        
        # Initial readings
        cpu_start = psutil.cpu_percent(interval=0)
        net_start = psutil.net_io_counters()
        disk_start = psutil.disk_io_counters()
        
        # Monitor over interval
        import time
        samples = []
        sample_count = min(interval_seconds, 10)  # Max 10 samples
        
        for i in range(sample_count):
            time.sleep(interval_seconds / sample_count)
            
            cpu = psutil.cpu_percent(interval=0)
            mem = psutil.virtual_memory().percent
            
            samples.append({
                'cpu': cpu,
                'memory': mem,
                'time': i + 1
            })
        
        # Final readings
        net_end = psutil.net_io_counters()
        disk_end = psutil.disk_io_counters() if disk_start else None
        
        # Calculate averages
        avg_cpu = sum(s['cpu'] for s in samples) / len(samples)
        avg_mem = sum(s['memory'] for s in samples) / len(samples)
        max_cpu = max(s['cpu'] for s in samples)
        max_mem = max(s['memory'] for s in samples)
        
        result += "**MONITORING RESULTS:**\n\n"
        
        result += "**CPU Usage:**\n"
        result += f"• Average: {avg_cpu:.1f}%\n"
        result += f"• Peak: {max_cpu:.1f}%\n"
        result += f"• Status: {'🔴 High' if avg_cpu > 80 else '🟡 Moderate' if avg_cpu > 50 else '🟢 Normal'}\n\n"
        
        result += "**Memory Usage:**\n"
        result += f"• Average: {avg_mem:.1f}%\n"
        result += f"• Peak: {max_mem:.1f}%\n"
        result += f"• Status: {'🔴 High' if avg_mem > 85 else '🟡 Moderate' if avg_mem > 70 else '🟢 Normal'}\n\n"
        
        # Network activity
        net_sent = net_end.bytes_sent - net_start.bytes_sent
        net_recv = net_end.bytes_recv - net_start.bytes_recv
        
        result += "**Network Activity (during monitoring):**\n"
        result += f"• Data Sent: {format_bytes(net_sent)} ({format_bytes(net_sent/interval_seconds)}/s)\n"
        result += f"• Data Received: {format_bytes(net_recv)} ({format_bytes(net_recv/interval_seconds)}/s)\n"
        result += f"• Total: {format_bytes(net_sent + net_recv)}\n\n"
        
        # Disk activity
        if disk_end:
            disk_read = disk_end.read_bytes - disk_start.read_bytes
            disk_write = disk_end.write_bytes - disk_start.write_bytes
            
            result += "**Disk Activity (during monitoring):**\n"
            result += f"• Read: {format_bytes(disk_read)} ({format_bytes(disk_read/interval_seconds)}/s)\n"
            result += f"• Written: {format_bytes(disk_write)} ({format_bytes(disk_write/interval_seconds)}/s)\n"
            result += f"• Total: {format_bytes(disk_read + disk_write)}\n\n"
        
        # Simple visualization
        result += "**CPU USAGE TREND:**\n"
        for sample in samples:
            bar_length = int(sample['cpu'] / 5)  # Scale to 20 chars max
            bar = '█' * bar_length
            result += f"Sample {sample['time']}: {bar} {sample['cpu']:.1f}%\n"
        
        result += "\n**💡 INTERPRETATION:**\n"
        result += "• Consistent high usage may indicate a background process\n"
        result += "• Spikes are normal during application launches\n"
        result += "• High network activity could indicate downloads/uploads\n"
        result += "• Use get_running_processes() to identify resource-heavy apps\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error monitoring resources: {str(e)}"

@mcp.tool
def diagnose_slow_performance() -> str:
    """
    Comprehensive diagnosis of system performance issues.
    Identifies potential bottlenecks and provides specific recommendations.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"🔍 **PERFORMANCE DIAGNOSIS** ({OS_INFO['system']})\n\n"
        result += "Running comprehensive system analysis...\n\n"
        
        issues = []
        recommendations = []
        bottlenecks = []
        
        # CPU Analysis
        result += "**1️⃣ CPU ANALYSIS:**\n"
        cpu_percent = psutil.cpu_percent(interval=2)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        result += f"• Usage: {cpu_percent}%\n"
        result += f"• Cores: {cpu_count}\n"
        if cpu_freq:
            result += f"• Current Speed: {cpu_freq.current:.0f} MHz\n"
        
        if cpu_percent > 80:
            issues.append("CPU is heavily loaded")
            bottlenecks.append("CPU")
            recommendations.append("Close unnecessary applications")
            recommendations.append("Check for CPU-intensive background processes")
            result += "🔴 **BOTTLENECK DETECTED**: CPU is overloaded\n"
        elif cpu_percent > 60:
            result += "⚠️ CPU usage is moderately high\n"
        else:
            result += "✅ CPU is performing well\n"
        
        result += "\n**2️⃣ MEMORY ANALYSIS:**\n"
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        result += f"• RAM Usage: {memory.percent}%\n"
        result += f"• Available: {format_bytes(memory.available)}\n"
        result += f"• Swap Usage: {swap.percent}%\n"
        
        if memory.percent > 90:
            issues.append("Critically low memory")
            bottlenecks.append("RAM")
            recommendations.append("Close memory-intensive applications")
            recommendations.append("Consider upgrading RAM")
            result += "🔴 **BOTTLENECK DETECTED**: Memory is critically low\n"
        elif memory.percent > 80:
            issues.append("Low available memory")
            bottlenecks.append("RAM")
            recommendations.append("Close unnecessary browser tabs")
            result += "🔴 Memory is running low\n"
        elif swap.percent > 50:
            issues.append("Heavy swap usage")
            recommendations.append("Add more RAM to reduce swap usage")
            result += "⚠️ System is using swap memory (slower than RAM)\n"
        else:
            result += "✅ Memory is healthy\n"
        
        result += "\n**3️⃣ DISK ANALYSIS:**\n"
        disk = psutil.disk_usage('/')
        
        try:
            disk_io = psutil.disk_io_counters()
            result += f"• Disk Usage: {disk.percent}%\n"
            result += f"• Free Space: {format_bytes(disk.free)}\n"
            
            if disk.percent > 95:
                issues.append("Critically low disk space")
                bottlenecks.append("Disk Space")
                recommendations.append("Delete unnecessary files immediately")
                recommendations.append("Move files to external storage")
                result += "🔴 **BOTTLENECK DETECTED**: Disk is almost full\n"
            elif disk.percent > 85:
                issues.append("Low disk space")
                recommendations.append("Run disk cleanup")
                result += "⚠️ Disk space is running low\n"
            else:
                result += "✅ Disk space is adequate\n"
        except:
            result += "⚠️ Unable to read disk I/O statistics\n"
        
        result += "\n**4️⃣ PROCESS ANALYSIS:**\n"
        # Find resource-heavy processes
        processes = []
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                if pinfo['cpu_percent'] > 10 or pinfo['memory_percent'] > 5:
                    processes.append(pinfo)
            except:
                continue
        
        processes.sort(key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)
        
        if processes:
            result += "**Resource-heavy processes:**\n"
            for proc in processes[:5]:
                result += f"• {proc['name']}: CPU {proc['cpu_percent']:.1f}%, Memory {proc['memory_percent']:.1f}%\n"
                
            if processes[0]['cpu_percent'] > 50:
                issues.append(f"{processes[0]['name']} is using excessive CPU")
                recommendations.append(f"Check if {processes[0]['name']} is responding properly")
        else:
            result += "✅ No significantly resource-heavy processes detected\n"
        
        result += "\n**5️⃣ STARTUP IMPACT:**\n"
        boot_time = psutil.boot_time()
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
        
        # Count startup processes
        startup_count = sum(1 for proc in psutil.process_iter(['create_time']) 
                          if proc.info['create_time'] <= boot_time + 300)
        
        result += f"• Startup processes: {startup_count}\n"
        result += f"• System uptime: {uptime.days} days\n"
        
        if startup_count > 50:
            issues.append("Too many startup programs")
            recommendations.append("Disable unnecessary startup programs")
            result += "⚠️ Many programs launch at startup\n"
        
        if uptime.days > 30:
            recommendations.append("Restart your computer to apply updates and clear memory")
            result += "⚠️ System hasn't been restarted in a while\n"
        
        # Overall Assessment
        result += "\n" + "="*50 + "\n"
        result += "**📋 DIAGNOSIS SUMMARY:**\n\n"
        
        if bottlenecks:
            result += f"**🔴 BOTTLENECKS IDENTIFIED:** {', '.join(bottlenecks)}\n"
            result += "These components are limiting your system's performance.\n\n"
        else:
            result += "**✅ NO MAJOR BOTTLENECKS**\n"
            result += "Your system is performing within normal parameters.\n\n"
        
        if issues:
            result += f"**⚠️ ISSUES FOUND ({len(issues)}):**\n"
            for issue in issues:
                result += f"• {issue}\n"
            result += "\n"
        
        if recommendations:
            result += f"**💡 RECOMMENDED ACTIONS ({len(recommendations)}):**\n"
            for i, rec in enumerate(recommendations, 1):
                result += f"{i}. {rec}\n"
            result += "\n"
        
        # Performance score
        score = 100
        score -= len(bottlenecks) * 25
        score -= len(issues) * 10
        score = max(0, score)
        
        result += f"**PERFORMANCE SCORE: {score}/100**\n"
        if score >= 80:
            result += "✅ Your system is performing well!\n"
        elif score >= 60:
            result += "🟡 Your system has some performance issues.\n"
        elif score >= 40:
            result += "🟠 Your system has significant performance problems.\n"
        else:
            result += "🔴 Your system is experiencing severe performance issues!\n"
        
        result += "\n**🔧 QUICK FIXES TO TRY:**\n"
        result += "1. Restart your computer\n"
        result += "2. Close unused applications and browser tabs\n"
        result += "3. Run disk cleanup to free up space\n"
        result += "4. Check for system updates\n"
        result += "5. Scan for malware with your antivirus\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error diagnosing performance: {str(e)}"

@mcp.tool
def get_power_settings() -> str:
    """
    Get information about power settings and power consumption.
    Useful for laptops and power management.
    """
    init_check = check_initialization()
    if init_check:
        return init_check
    
    try:
        result = f"⚡ **POWER SETTINGS** ({OS_INFO['system']})\n\n"
        
        # Battery info
        battery = psutil.sensors_battery() if hasattr(psutil, 'sensors_battery') else None
        
        if battery:
            result += "**BATTERY STATUS:**\n"
            result += f"• Charge Level: {battery.percent}%\n"
            result += f"• Plugged In: {'Yes' if battery.power_plugged else 'No'}\n"
            
            if battery.secsleft > 0 and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                result += f"• Time Remaining: {hours}h {minutes}m\n"
            result += "\n"
        else:
            result += "**POWER SOURCE:**\n"
            result += "• Desktop computer or battery info unavailable\n"
            result += "• System is running on AC power\n\n"
        
        # CPU frequency (can indicate power mode)
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            result += "**CPU POWER STATE:**\n"
            result += f"• Current Frequency: {cpu_freq.current:.0f} MHz\n"
            if hasattr(cpu_freq, 'min') and cpu_freq.min > 0:
                result += f"• Minimum Frequency: {cpu_freq.min:.0f} MHz\n"
            if hasattr(cpu_freq, 'max') and cpu_freq.max > 0:
                result += f"• Maximum Frequency: {cpu_freq.max:.0f} MHz\n"
                
                # Power mode estimation
                if cpu_freq.current < cpu_freq.max * 0.5:
                    result += "• Mode: 🔋 Power Saver\n"
                elif cpu_freq.current > cpu_freq.max * 0.9:
                    result += "• Mode: ⚡ High Performance\n"
                else:
                    result += "• Mode: ⚖️ Balanced\n"
            result += "\n"
        
        # OS-specific power settings info
        if OS_INFO['system'] == "Windows":
            result += "**WINDOWS POWER MANAGEMENT:**\n"
            result += "• Access: Settings → System → Power & battery\n"
            result += "• Or: Control Panel → Power Options\n"
            result += "• Common plans: Balanced, Power saver, High performance\n"
            result += "• Adjust screen timeout and sleep settings\n\n"
            
            result += "**POWER TIPS FOR WINDOWS:**\n"
            result += "• Enable Battery Saver when unplugged\n"
            result += "• Reduce screen brightness\n"
            result += "• Adjust 'When plugged in, turn off screen after'\n"
            result += "• Use 'Power Throttling' for background apps\n"
            
        elif OS_INFO['system'] == "Darwin":
            result += "**macOS POWER MANAGEMENT:**\n"
            result += "• Access: System Preferences → Battery\n"
            result += "• Or: System Settings → Battery\n"
            result += "• View energy usage by app\n"
            result += "• Enable 'Low Power Mode' to extend battery\n\n"
            
            result += "**POWER TIPS FOR macOS:**\n"
            result += "• Enable 'Low Power Mode' on battery\n"
            result += "• Reduce display brightness\n"
            result += "• Close unused apps (check Activity Monitor)\n"
            result += "• Disable Bluetooth/Wi-Fi when not needed\n"
            
        else:  # Linux
            result += "**LINUX POWER MANAGEMENT:**\n"
            result += "• Check power profiles: powerprofilesctl list\n"
            result += "• Or use TLP for laptop power management\n"
            result += "• Monitor: powertop or cat /sys/class/power_supply/BAT*/uevent\n"
            result += "• Desktop environment may have power settings\n\n"
            
            result += "**POWER TIPS FOR LINUX:**\n"
            result += "• Install TLP: sudo apt install tlp\n"
            result += "• Use powertop to identify power-hungry processes\n"
            result += "• Adjust CPU governor: cpupower frequency-set\n"
            result += "• Reduce screen brightness\n"
        
        result += "\n**🔋 GENERAL POWER SAVING TIPS:**\n"
        result += "• Reduce screen brightness (biggest battery drain)\n"
        result += "• Close unnecessary applications\n"
        result += "• Disable keyboard backlight\n"
        result += "• Turn off Bluetooth/Wi-Fi when not in use\n"
        result += "• Use dark mode to save OLED screen power\n"
        result += "• Keep your system updated for power optimizations\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting power settings: {str(e)}"


def main():
    try:
        logger.info("Starting SystemMind MCP server...")
        logger.info("=" * 60)
        logger.info("Available tools:")
        logger.info("  - initialize_os_connection: Initialize and detect OS, set config")
        logger.info("  - get_running_processes: Top processes with CPU/RAM and categories")
        logger.info("  - get_system_overview: CPU/RAM/Storage/Uptime snapshot")
        logger.info("  - get_network_info: Interfaces, IPs, speeds, active connections")
        logger.info("  - get_disk_usage: Partitions, capacities, usage, disk I/O")
        logger.info("  - get_performance_summary: Health score + quick fixes")
        logger.info("  - get_temperature_info: Sensor temperatures and thresholds")
        logger.info("  - get_battery_info: Battery %, charge state, time left/full")
        logger.info("  - check_startup_programs: Boot-time apps and impact")
        logger.info("  - get_user_info: Current user, sessions, env basics")
        logger.info("  - find_large_files: Scan for large files (bounded depth)")
        logger.info("  - get_installed_software: OS-aware apps/packages overview")
        logger.info("  - clean_temp_files: Enumerate/clean temp files (dry-run by default)")
        logger.info("  - get_system_services: OS services hints + common daemons")
        logger.info("  - check_security_status: AV/firewall hints, uptime, score")
        logger.info("  - get_resource_monitor: Short live monitor with trends")
        logger.info("  - diagnose_slow_performance: Multi-area diagnosis & fixes")
        logger.info("  - get_power_settings: Battery/AC state, CPU freq, power tips")
        logger.info("Server starting on http://127.0.0.1:9090")
        logger.info("=" * 60)
        
        mcp.run(transport="streamable-http", host="127.0.0.1", port=9090)
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("Server stopped by user")
        logger.info("=" * 60)
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"❌ Server error: {str(e)}")
        logger.error("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
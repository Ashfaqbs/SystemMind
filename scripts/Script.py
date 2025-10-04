#!/usr/bin/env python3
"""
System Health Check (friendly report for non-tech users)

Usage:
  python sys_health_check.py --top 25 --save

Dependencies:
  pip install psutil gputil
"""
import argparse
import csv
import json
import os
import platform
import shutil
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

# Third-party (install via pip)
try:
    import psutil
except ImportError:
    print("psutil is required. Install it with: pip install psutil")
    sys.exit(1)

# Optional GPU info
try:
    import GPUtil  # pip install gputil
    HAS_GPU = True
except Exception:
    HAS_GPU = False


def human_bytes(num: float) -> str:
    """Convert bytes to a friendly size (e.g., 1.2 GB)."""
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} EB"


def uptime_str(boot_ts: float) -> str:
    secs = max(0, int(time.time() - boot_ts))
    days, rem = divmod(secs, 86400)
    hrs, rem = divmod(rem, 3600)
    mins, _ = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hrs: parts.append(f"{hrs}h")
    if mins: parts.append(f"{mins}m")
    return " ".join(parts) or "0m"


def basic_system_info():
    uname = platform.uname()
    info = {
        "Hostname": uname.node,
        "OS": f"{uname.system} {uname.release} ({uname.version})",
        "Machine": uname.machine,
        "Processor": uname.processor or platform.platform(),
        "Python": platform.python_version(),
    }
    return info


def cpu_info():
    try:
        freq = psutil.cpu_freq()
        freq_str = f"{freq.current/1000:.2f} GHz" if freq else "N/A"
    except Exception:
        freq_str = "N/A"

    logical = psutil.cpu_count(logical=True) or 0
    physical = psutil.cpu_count(logical=False) or logical

    per_core = psutil.cpu_percent(interval=0.5, percpu=True)
    overall = sum(per_core) / max(1, len(per_core)) if per_core else psutil.cpu_percent(interval=0.5)

    load_avg = {}
    try:
        la1, la5, la15 = os.getloadavg()  # Unix
        load_avg = {"1min": round(la1, 2), "5min": round(la5, 2), "15min": round(la15, 2)}
    except Exception:
        # Not available on Windows
        load_avg = {}

    return {
        "Logical Cores": logical,
        "Physical Cores": physical,
        "CPU Frequency": freq_str,
        "CPU Usage Overall %": round(overall, 1) if isinstance(overall, (int, float)) else overall,
        "CPU Usage per Core %": [round(x, 1) for x in per_core],
        "Load Average": load_avg or "N/A",
    }


def memory_info():
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    return {
        "RAM Total": human_bytes(vm.total),
        "RAM Used": human_bytes(vm.used),
        "RAM Free": human_bytes(vm.available),
        "RAM Usage %": vm.percent,
        "Swap Total": human_bytes(sm.total),
        "Swap Used": human_bytes(sm.used),
        "Swap Usage %": sm.percent,
    }


def storage_info():
    disks = []
    seen = set()
    for part in psutil.disk_partitions(all=False):
        # Avoid duplicates/mount quirks
        if part.mountpoint in seen:
            continue
        seen.add(part.mountpoint)
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        disks.append({
            "Device/Mount": f"{part.device} → {part.mountpoint}",
            "Filesystem": part.fstype or "N/A",
            "Total": human_bytes(usage.total),
            "Used": human_bytes(usage.used),
            "Free": human_bytes(usage.free),
            "Usage %": usage.percent,
        })
    # Root path (cross-check)
    try:
        total, used, free = shutil.disk_usage(Path.home().anchor or "/")
        disks.insert(0, {
            "Device/Mount": "System Drive",
            "Filesystem": "N/A",
            "Total": human_bytes(total),
            "Used": human_bytes(used),
            "Free": human_bytes(free),
            "Usage %": round(used * 100 / total, 1) if total else 0,
        })
    except Exception:
        pass
    return disks


def network_info():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    traffic = psutil.net_io_counters(pernic=True)
    data = []
    for name, addr_list in addrs.items():
        ips = []
        for a in addr_list:
            if a.family == socket.AF_INET:
                ips.append(a.address)
            # Skip IPv6/MAC in the simple view for non-tech users
        st = stats.get(name)
        tr = traffic.get(name)
        data.append({
            "Interface": name,
            "Up": bool(st.isup) if st else None,
            "Speed (Mbps)": getattr(st, "speed", None) if st else None,
            "IP(s)": ", ".join(ips) if ips else "—",
            "Sent": human_bytes(tr.bytes_sent) if tr else "—",
            "Received": human_bytes(tr.bytes_recv) if tr else "—",
        })
    # Default hostname/IP summary
    try:
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
    except Exception:
        host, ip = platform.node(), "N/A"
    return {"Hostname": host, "Primary IP": ip, "Interfaces": data}


def battery_info():
    try:
        b = psutil.sensors_battery()
        if not b:
            return {"Battery": "Not detected"}
        plugged = "Charging" if b.power_plugged else "On Battery"
        eta = "Calculating"
        if not b.power_plugged and b.secsleft and b.secsleft > 0:
            hrs, rem = divmod(b.secsleft, 3600)
            mins = rem // 60
            eta = f"~{int(hrs)}h {int(mins)}m remaining"
        return {
            "Battery %": int(b.percent),
            "State": plugged,
            "Estimate": eta
        }
    except Exception:
        return {"Battery": "Unavailable"}


def gpu_info():
    if not HAS_GPU:
        return {"GPU": "No NVIDIA GPU module detected"}
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"GPU": "No NVIDIA GPU found"}
        rows = []
        for g in gpus:
            rows.append({
                "Name": g.name,
                "Load %": int(g.load * 100),
                "Memory Used": human_bytes(g.memoryUsed * 1024**2),
                "Memory Total": human_bytes(g.memoryTotal * 1024**2),
                "Temperature °C": int(g.temperature),
                "UUID": g.uuid,
            })
        return {"GPUs": rows}
    except Exception:
        return {"GPU": "Unavailable"}


def list_processes(limit: int = 25):
    procs = []
    for p in psutil.process_iter(attrs=[
        "pid", "name", "username", "status", "cpu_percent", "memory_percent", "create_time"
    ]):
        try:
            info = p.info
            # psutil requires two samples to get meaningful cpu_percent; call once quickly:
            if info.get("cpu_percent") is None or info["cpu_percent"] == 0.0:
                p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Allow CPU usage to accumulate briefly
    time.sleep(0.3)
    for p in psutil.process_iter(attrs=[
        "pid", "name", "username", "status", "cpu_percent", "memory_percent", "create_time"
    ]):
        try:
            info = p.info
            procs.append({
                "PID": info["pid"],
                "Name": (info["name"] or "")[:60],
                "User": (info.get("username") or "").split("\\")[-1],
                "Status": info.get("status"),
                "CPU %": round(p.cpu_percent(interval=None), 1),
                "Mem %": round(info.get("memory_percent") or 0.0, 2),
                "Started": datetime.fromtimestamp(info["create_time"]).strftime("%Y-%m-%d %H:%M:%S"),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            continue

    # Sort by CPU then memory
    procs.sort(key=lambda x: (x["CPU %"], x["Mem %"]), reverse=True)
    return procs, len(procs), procs[:max(1, limit)]


def health_tips(mem, disks):
    """Simple flags for non-tech users (plain language)."""
    tips = []

    # RAM pressure
    try:
        if mem.get("RAM Usage %", 0) >= 85:
            tips.append("RAM usage is high (≥85%). Closing unused apps can speed things up.")
    except Exception:
        pass

    # Disk space low
    try:
        for d in disks:
            if isinstance(d.get("Usage %"), (int, float)) and d["Usage %"] >= 90:
                tips.append(f"Low free space on {d.get('Device/Mount')}. Consider deleting large files or emptying recycle bin.")
                break
    except Exception:
        pass

    # Uptime suggestion
    try:
        boot = psutil.boot_time()
        if (time.time() - boot) > 14 * 86400:
            tips.append("System has been running for over 2 weeks. A restart can refresh performance.")
    except Exception:
        pass

    # Updates hint
    if platform.system() == "Windows":
        tips.append("Check Windows Update for security and driver updates.")
    elif platform.system() == "Darwin":
        tips.append("Check System Settings → General → Software Update for macOS updates.")
    else:
        tips.append("Apply OS updates via your distro’s updater (e.g., apt, dnf, pacman).")

    if not tips:
        tips.append("Everything looks normal. No urgent action needed.")
    return tips


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Friendly OS / Machine health report")
    parser.add_argument("--top", type=int, default=25, help="How many processes to show")
    parser.add_argument("--save", action="store_true", help="Save JSON report and CSV of processes")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "Generated At": datetime.now().isoformat(timespec="seconds"),
        "System": basic_system_info(),
        "Uptime": {
            "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "Uptime": uptime_str(psutil.boot_time()),
        },
        "CPU": cpu_info(),
        "Memory": memory_info(),
        "Storage": storage_info(),
        "Network": network_info(),
        "Battery": battery_info(),
        "GPU": gpu_info(),
    }

    # Processes
    processes, total_count, topN = list_processes(limit=args.top)
    report["Processes Summary"] = {
        "Total Running Processes": total_count,
        "Top by CPU/Mem (first N)": args.top
    }
    report["Processes TopN"] = topN  # compact view

    # Print human-readable report
    print_section("SYSTEM SUMMARY")
    for k, v in report["System"].items():
        print(f"{k:18}: {v}")

    print_section("UPTIME")
    for k, v in report["Uptime"].items():
        print(f"{k:18}: {v}")

    print_section("CPU")
    for k, v in report["CPU"].items():
        if isinstance(v, list):
            print(f"{k:18}: {', '.join(map(str, v))}")
        elif isinstance(v, dict):
            print(f"{k:18}: " + ", ".join(f"{ik}={iv}" for ik, iv in v.items()))
        else:
            print(f"{k:18}: {v}")

    print_section("MEMORY (RAM)")
    for k, v in report["Memory"].items():
        print(f"{k:18}: {v}")

    print_section("STORAGE (DISKS)")
    for d in report["Storage"]:
        print(f"- {d['Device/Mount']}")
        print(f"  Filesystem     : {d['Filesystem']}")
        print(f"  Total / Used   : {d['Total']} / {d['Used']} ({d['Usage %']}%)")
        print(f"  Free           : {d['Free']}")

    print_section("NETWORK")
    net = report["Network"]
    print(f"Hostname         : {net.get('Hostname')}")
    print(f"Primary IP       : {net.get('Primary IP')}")
    for iface in net.get("Interfaces", []):
        print(f"- {iface['Interface']}: Up={iface['Up']} Speed={iface['Speed (Mbps)']}Mbps IPs={iface['IP(s)']} Sent={iface['Sent']} Received={iface['Received']}")

    print_section("BATTERY")
    for k, v in report["Battery"].items():
        print(f"{k:18}: {v}")

    print_section("GPU")
    for k, v in report["GPU"].items():
        if isinstance(v, list):
            for idx, row in enumerate(v):
                print(f"- GPU {idx}:")
                for rk, rv in row.items():
                    print(f"  {rk:16}: {rv}")
        else:
            print(f"{k:18}: {v}")

    print_section(f"PROCESSES (Top {args.top})")
    print(f"Total running processes: {total_count}")
    header = ["PID", "Name", "User", "Status", "CPU %", "Mem %", "Started"]
    print(" | ".join(f"{h:>8}" if h in ['PID', 'CPU %', 'Mem %'] else f"{h:<20}" for h in header))
    print("-" * 80)
    for p in report["Processes TopN"]:
        print(f"{p['PID']:>8} | {p['Name']:<20.20} | {p['User']:<20.20} | {p['Status']:<10} | {p['CPU %']:>6.1f} | {p['Mem %']:>6.2f} | {p['Started']}")

    # Simple health tips
    tips = health_tips(report["Memory"], report["Storage"])
    print_section("QUICK TIPS (Plain Language)")
    for t in tips:
        print(f"- {t}")

    # Optional saves
    if args.save:
        # Save JSON report (full)
        json_path = Path(f"system_report_{timestamp}.json")
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        # Save CSV for all processes
        csv_path = Path(f"processes_{timestamp}.csv")
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for row in processes:
                writer.writerow(row)
        print_section("FILES SAVED")
        print(f"JSON report : {json_path.resolve()}")
        print(f"CSV (procs) : {csv_path.resolve()}")


if __name__ == "__main__":
    main()

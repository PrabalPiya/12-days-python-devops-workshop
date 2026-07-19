import json
import socket
from datetime import datetime
from pathlib import Path
import psutil

CPU_LIMIT = 80
MEMORY_LIMIT = 80
DISK_LIMIT = 80

def convert_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("/")

warnings = []

if cpu > CPU_LIMIT:
    warnings.append(f"CPU usage is high: {cpu}%")
    
if memory.percent > MEMORY_LIMIT:
    warnings.append(f"Memory usage is high: {memory.percent}%")
    
if disk.percent > DISK_LIMIT:
    warnings.append(f"Disk usage is high: {disk.percent}%")
    
report = {
    "timestamp": datetime.now().isoformat(),
    "hostname": socket.gethostname(),
    "cpu_percent": cpu,
    "memory_percent": memory.percent,
    "disk_percent": disk.percent,
    "memory_total_gb": convert_to_gb(memory.total),
    "disk_total_gb": convert_to_gb(disk.total),
    "process_count": len(psutil.pids()),
    "warnings": warnings,
    "healthy": len(warnings) == 0,
}

with open("server_health.json", "w") as file:
    json.dump(report, file, indent=2)
    
print(f"Hostname: {report['hostname']}")
print(f"CPU: {cpu}%")
print(f"Memory: {memory.percent}%")
print(f"Disk: {disk.percent}%")

if warnings:
    for warning in warnings:
        print(f"[WARNING] {warning}")

    raise SystemExit(1)

print("[OK] System health is normal")
print(f"System health report saved to server_health.json")


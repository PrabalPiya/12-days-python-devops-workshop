import getpass
import os
import platform
import socket
import sys

username = getpass.getuser()
hostname = socket.gethostname()
operating_system = platform.system()
python_version = platform.python_version()
machine_architecture = platform.machine()
current_directory = os.getcwd()
processor = os.cpu_count()
home = os.path.expanduser("~")

print("=" * 40)
print("DEVOPS ENVIRONMENT REPORT")
print("=" * 40)
print(f"Username: {username}")
print(f"Hostname: {hostname}")
print(f"Operating System: {operating_system}")
print(f"Python Version: {python_version}")
print(f"Machine Architecture: {machine_architecture}")
print(f"Current Directory: {current_directory}")
print(f"Processor Count: {processor}")
print(f"Home Directory: {home}")
print(f"Python Executable: {sys.executable}")


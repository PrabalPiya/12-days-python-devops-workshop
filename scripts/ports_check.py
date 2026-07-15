import argparse
import socket

def check_port(host:str, port:int, timeout:float=3.0) -> bool:

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, type=str)
    parser.add_argument("--port", required=True,  type=int, nargs="+")
    parser.add_argument("--timeout", type=float, default=3.0,)
    return parser.parse_args()

def main() -> int:
    args = parse_arguments()
    failed_count = 0
    
    print(f"\nChecking ports on {args.host}:\n")
    
    for port in args.port:
        if check_port(args.host, port, args.timeout):
            print(f"[OK] {args.host}:{port} is reachable.")
        else:
            print(f"[ERROR] {args.host}:{port} is unreachable.")
            failed_count += 1
        
    print("\nCheck completed.")
   
    if failed_count > 0:
        return 1 
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
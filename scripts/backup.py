import argparse
import shutil
from datetime import datetime
from pathlib import Path

def create_backup(source: Path, destination: Path) -> Path:
    
    if not source.exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")
    
    destination.mkdir(parents=True, exist_ok=True)
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = destination / f"{source.name}_{datetime_str}"
    
    archive_path = shutil.make_archive(base_name=str(archive_name), format='zip', root_dir=str(source))
    return Path(archive_path)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    return parser.parse_args()

def main() -> int:
    args = parse_arguments()
    
    try:
        backup_path= create_backup(args.source, args.destination)
        print(f"Backup created at: {backup_path}")
        return 0
    
    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")
        return 1
    
if __name__ == "__main__":
    raise SystemExit(main())
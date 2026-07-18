import argparse
import csv
import json
import os
import time
from datetime import datetime
import requests
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="../config/services.yaml")
parser.add_argument("--retries", type=int, default=2)
parser.add_argument("--delay", type=int, default=2)
parser.add_argument("--fail-on-unhealthy", action="store_true")
args = parser.parse_args()

with open(args.config, "r") as file:
    config = yaml.safe_load(file)

services = config["services"]

token = os.getenv("API_TOKEN")
results = []
unhealthy_count = 0

for service in services:
    name = service["name"]
    url = service["url"]
    expected_status = service.get("expected_status", 200)
    
    headers = {
        "User-Agent": "Health-Checker"
    }

    if service.get("use_token") and token:
        headers["Authorization"] = f"Bearer {token}"
    
    healthy = False
    error_message = ""
    status_code = None
    response_time = None
    
    for attempt in range(args.retries + 1):
        try:
            start_time = time.time()

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response_time = round(
                time.time() - start_time, 2
            )

            status_code = response.status_code

            if status_code == expected_status:
                healthy = True
                break

        except requests.RequestException as error:
            error_message = str(error)

        if attempt < args.retries:
            print(f"Retrying {name}...")
            time.sleep(args.delay)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "url": url,
        "status": status_code,
        "response_time": response_time,
        "healthy": healthy,
        "error": error_message
    }

    results.append(result)

    if healthy:
        print(f"[OK] {name} is healthy")

        if response_time > 2:
            print(f"[WARNING] {name} is slow")
    else:
        print(f"[ERROR] {name} is unhealthy")
        unhealthy_count += 1

with open("health_report.json", "w") as file:
    json.dump(results, file, indent=2)

with open("health_report.csv", "w", newline="") as file:
    columns = results[0].keys()

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)


print("\nReports created:")
print("health_report.json")
print("health_report.csv")

if args.fail_on_unhealthy and unhealthy_count > 0:
    raise SystemExit(1)
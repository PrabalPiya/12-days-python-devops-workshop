servers = [ { 
                "name": "frontend-01",
                "ip": "10.0.1.10",
                "environment": "production",
                "status": "running", 
                
            },
            {   "name": "backend-01",
                "ip": "10.0.2.10",
                "environment": "production",
                "status": "stopped",
            }, 
            { 
                "name": "database-01",
                "ip": "10.0.3.10",
                "environment": "development",
                "status": "running",
             },
            { 
                "ip": "10.0.1.10",
            },
          ]

running_count = 0
stopped_count = 0
production_count = 0
development_count = 0

print("\nStatus:")
for server in servers:
    name = server.get("name", "unknown server")
    status = server.get("status", "unknown")
    
    if status == "running":
        running_count += 1
        print(f"[OK] {name} is running.")
        
    elif status == "stopped":
        stopped_count += 1
        print(f"[WARNING] {name} is {status}.")
        
    else:
        print(f"[ERROR] {name} has an unknown status.")

print("\nServers:")
for server in servers:
    name = server.get("name", "unknown server")
    environment = server.get("environment", "unknown")
    status = server.get("status", "unknown")
    
    if environment == "production" and status == "running":
        production_count += 1
        print(f"{name} is in {environment}.")
        
    elif environment == "production" and status == "stopped":
        production_count += 1
        print(f"[WARNING] {name} is in {environment} but is {status}.")
        
    elif environment == "development":
        development_count += 1
        print(f"{name} is in {environment}.")
    
    else:
        print(f"[ERROR] {name} has an {environment} environment.")


        
print("\nSummary:")
print(f"Running servers: {running_count}")
print(f"Stopped servers: {stopped_count}")
print(f"Production servers: {production_count}")
print(f"Development servers: {development_count}")
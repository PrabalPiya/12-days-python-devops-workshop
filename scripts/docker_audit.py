import argparse
import docker

def show_containers(client, unhealthy_only=False):
    containers = client.containers.list(all=True)
    
    for container in containers:
        health = (
            container.attrs
            .get("State", {})
            .get("Health", {})
            .get("Status", "not-configured")
        )

        problem = container.status != "running" or health == "unhealthy"

        if unhealthy_only and not problem:
            continue

        print(container.name, container.status, health)
        
def show_images(client):
    images = client.images.list()
    for image in images:
        print(image.short_id, image.tags or ["<none>"])
        
def cleanup(client, execute):
    stopped = client.containers.list(
        all=True,
        filters={"status": "exited"},
    )

    dangling_images = client.images.list(
        filters={"dangling": True},
    )

    unused_networks = []
    networks = client.networks.list()
    for network in networks:
        if (
            network.name not in ["bridge", "host", "none"]
            and not network.attrs.get("Containers")
        ):
            unused_networks.append(network)

    print("\nStopped containers:")
    for container in stopped:
        print(container.name)

    print("\nDangling images:")
    for image in dangling_images:
        print(image.short_id)

    print("\nUnused networks:")
    for network in unused_networks:
        print(network.name)

    if not execute:
        print("\n[DRY RUN] Nothing deleted.")
        return

    for container in stopped:
        container.remove()

    for image in dangling_images:
        client.images.remove(image.id)

    for network in unused_networks:
        network.remove()

    print("\nCleanup complete.")
    
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=["list", "unhealthy", "images", "cleanup"],
    )

    parser.add_argument(
        "--execute",
        action="store_true",
    )

    args = parser.parse_args()

    try:
        client = docker.from_env()
        client.ping()
        
    except Exception as error:
        print(f"[ERROR] {error}")
        return 1

    if args.command == "list":
        show_containers(client)

    elif args.command == "unhealthy":
        show_containers(client, unhealthy_only=True)

    elif args.command == "images":
        show_images(client)

    elif args.command == "cleanup":
        cleanup(client, args.execute)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
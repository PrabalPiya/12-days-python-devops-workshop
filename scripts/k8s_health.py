import argparse

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException


parser = argparse.ArgumentParser(
    description="Check the health of Kubernetes pods."
)

parser.add_argument(
    "--namespace",
    default="default",
    help="Kubernetes namespace to check.",
)

args = parser.parse_args()

try:
    config.load_kube_config()
    api = client.CoreV1Api()

    pods = api.list_namespaced_pod(
        namespace=args.namespace
    )

except ConfigException as error:
    print(f"[ERROR] Could not load kubeconfig: {error}")
    raise SystemExit(1)

except ApiException as error:
    print(f"[ERROR] Kubernetes API error: {error.reason}")
    raise SystemExit(1)

except Exception as error:
    print(f"[ERROR] Cannot connect to Kubernetes: {error}")
    raise SystemExit(1)


if not pods.items:
    print(f"[INFO] No pods found in namespace '{args.namespace}'")
    raise SystemExit(0)


for pod in pods.items:
    name = pod.metadata.name
    phase = pod.status.phase
    containers = pod.status.container_statuses or []

    ready = bool(containers) and all(
        container.ready
        for container in containers
    )

    restarts = sum(
        container.restart_count
        for container in containers
    )

    if phase == "Running" and ready and restarts < 3:
        print(
            f"[OK] {name} | "
            f"status={phase} | "
            f"ready={ready} | "
            f"restarts={restarts}"
        )
    else:
        print(
            f"[WARNING] {name} | "
            f"status={phase} | "
            f"ready={ready} | "
            f"restarts={restarts}"
        )
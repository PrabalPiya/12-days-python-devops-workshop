import shutil
import subprocess
import logging
from pathlib import Path

log_file = Path(__file__).parent / "deployment_precheck.log"

logging.basicConfig(
    
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="a"),
        logging.StreamHandler()
    ]
)

def run_command(command):
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        output = result.stdout.strip() or result.stderr.strip()

        if result.returncode == 0:
            return True, output

        return False, output

    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    
def check_installation(tool_name, command):
    
    if shutil.which(tool_name) is None:
        logging.warning(f"{tool_name} is not installed")
        return False

    success, output = run_command(command)

    if success:
        first_line = output.splitlines()[0]
        logging.info(f"{tool_name} installed: {first_line}")
        return True

    logging.error(f"Could not check {tool_name}: {output}")
    return False

def main():
    logging.info("Starting deployment pre-check")

    failed_checks = []

    git_available = check_installation(
        "git",
        ["git", "--version"],
    )

    if not git_available:
        failed_checks.append("Git installation")


    docker_available = check_installation(
        "docker",
        ["docker", "--version"],
    )

    if not docker_available:
        failed_checks.append("Docker installation")

    if docker_available:
        success, output = run_command(["docker", "info"])

        if success:
            logging.info("Docker daemon is running")
        else:
            logging.warning("Docker is installed, but the Docker daemon is not running")
            failed_checks.append("Docker daemon")

    kubectl_available = check_installation(
        "kubectl",
        ["kubectl", "version", "--client"],
    )

    if not kubectl_available:
        failed_checks.append("Kubectl installation")

    if kubectl_available:
        success, output = run_command(
            ["kubectl", "config", "current-context"]
        )

        if success:
            logging.info(f"Current Kubernetes context: {output}")
        else:
            logging.warning("No Kubernetes context is currently selected")
            failed_checks.append("Kubernetes context")

    terraform_available = check_installation(
        "terraform",
        ["terraform", "version"],
    )

    if not terraform_available:
        failed_checks.append("Terraform installation")

    aws_available = check_installation(
        "aws",
        ["aws", "--version"],
    )

    if not aws_available:
        failed_checks.append("AWS CLI installation")

    if aws_available:
        success, output = run_command(
            ["aws", "sts", "get-caller-identity"]
        )

        if success:
            logging.info(f"AWS identity found:\n{output}")
        else:
            logging.warning(
                "AWS CLI is installed, but AWS credentials are not configured"
            )
            failed_checks.append("AWS identity")

    total, used, free = shutil.disk_usage("/")

    free_space_gb = free / (1024 ** 3)

    logging.info(f"Available disk space: {free_space_gb:.2f} GB")

    if free_space_gb < 5:
        logging.warning("Less than 5 GB of disk space is available")
        failed_checks.append("Disk space")

    if failed_checks:
        logging.warning("Some deployment checks failed:")

        for check in failed_checks:
            logging.warning(f"- {check}")

        return 1

    logging.info("All deployment pre-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
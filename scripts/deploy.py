import requests
import sys
import os


def deploy(environment):
    url = f"https://listener.papyr-app.xyz/webhook/{environment}"
    token = os.getenv('SECRET_TOKEN')

    if not token:
        print("Secret token not found in environment variables")
        sys.exit(1)

    response = requests.post(f"{url}?token={token}")

    if response.status_code not in [200, 202]:
        print(f"Deployment failed with status code {response.status_code}")
        sys.exit(1)

    print("Deployment successful")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["test", "prod"]:
        print("Usage: deploy_script.py <test|prod>")
        sys.exit(1)

    environment = sys.argv[1]
    deploy(environment)

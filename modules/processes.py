import requests
from tabulate import tabulate
from datetime import datetime, timezone



def table_process(data):
    env_keys_to_include = [
        "PATH", "CRIBL_GROUP_ID", "SYSTEMD_EXEC_PID",
        "AWS_DEFAULT_REGION", "TENANT_ID", "DEPLOYMENT_NAME"
    ]

    flattened = []
    for item in data.get("items", []):
        env = item.get("env", {})
        # Convert startTime (Unix timestamp) to ISO format
        timestamp = item.get("startTime", 0)
        start_time_str  = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat() if isinstance(timestamp, (int, float)) else ""

        flat = {
            "id": item.get("id", ""),
            "type": item.get("type", ""),
            "pid": item.get("pid", ""),
            "startTime": start_time_str,
            "restarts": item.get("restarts", ""),
            "restartOnExit": item.get("restartOnExit", "")
        }
        for key in env_keys_to_include:
            flat[key] = env.get(key, "")
        flattened.append(flat)

    if not flattened:
        print("No data to display.")
        return

    print(tabulate(flattened, headers="keys", tablefmt="github"))



def get_processes(url, headers):
    url = f"{url}/system/processes"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        table_process(data)
    else:
        print(response.status_code)




def get_list_upgrades(url, headers):
    url = f"{url}/system/settings/upgrade"
    response = requests.get(url, headers=headers)
    data = response.json()
    item = data.get("items", [])[0]  # Assume only one item for now

    if not item.get("canUpgrade", False):
        print("No upgrade available.")
        return

    available_versions = item.get("availableVersions", [])
    if not available_versions:
        print("Upgrade available, but no version details provided.")
        return
    table_data = []
    for version in available_versions:
        table_data.append({
            "fullVersion": version.get("fullVersion", ""),
            "major": version.get("major", ""),
            "minor": version.get("minor", ""),
            "point": version.get("point", ""),
            "preRelease": version.get("preRelease", ""),
            "build": version.get("build", ""),
            "platform": version.get("platform", ""),
            "architecture": version.get("architecture", "")
        })

    print(tabulate(table_data, headers="keys", tablefmt="github"))
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(response.status_code)




def restart_cribl(url,headers):
    url=f"{url}/system/settings/restart"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Cribl server restarted with success!")
    else:
        print(response.status_code)


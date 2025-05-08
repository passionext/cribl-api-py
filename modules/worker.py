import requests
from tabulate import tabulate
from urllib.parse import urlencode


def build_url(base_url, path, filter_expr=None):
    """Constructs a URL with optional filter expression."""
    url = f"{base_url}{path}"
    if filter_expr:
        query = urlencode({"filterExp": filter_expr})
        return f"{url}?{query}"
    return url


def get_filter_input():
    """Prompts user for an optional filter expression."""
    return input("Insert a filter expression (leave blank for no filter): ").strip()


def fetch_data(url, headers):
    """Makes a GET request and returns JSON data or raises an exception."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def worker_count(base_url, headers):
    """Fetches and prints worker count summary (raw)."""
    filter_expr = get_filter_input()
    url = build_url(base_url, "/master/summary/workers", filter_expr)
    data = fetch_data(url, headers)
    if data:
        print("\n[Worker Summary]")
        print(data)


def extract_worker_info(item):
    """Extracts key fields from a single worker node."""
    info = item.get("info", {})
    cribl_info = info.get("cribl", {})
    return {
        "ID": item.get("id"),
        "Status": item.get("status"),
        "Hostname": info.get("hostname"),
        "Platform": info.get("platform"),
        "Arch": info.get("architecture"),
        "CPUs": info.get("cpus"),
        "Memory (GB)": round(info.get("totalmem", 0) / 1e9, 2),
        "Disk Free (GB)": round(info.get("freeDiskSpace", 0) / 1e9, 2),
        "Node Version": info.get("node"),
        "Cribl Version": cribl_info.get("version"),
        "Conn IP": info.get("conn_ip"),
        "Group": item.get("group")
    }


def worker_info(base_url, headers):
    """Fetches and prints worker node information in tabular form."""
    filter_expr = get_filter_input()
    url = build_url(base_url, "/master/workers", filter_expr)
    data = fetch_data(url, headers)
    if data and "items" in data:
        rows = [extract_worker_info(item) for item in data["items"]]
        print("\n[Worker Node Info]")
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    elif data is not None:
        print("No worker node data found.")

def restart_workers(base_url, headers):
    """Sends a PATCH request to restart worker nodes."""
    url = f"{base_url}/master/workers/restart"

    try:
        response = requests.patch(url, headers=headers)
        response.raise_for_status()
        print("[SUCCESS] Workers restart initiated.")
        if response.text:
            print("Response:", response.json())
    except requests.RequestException as e:
        print(f"[ERROR] Failed to restart workers: {e}")
import requests
from tabulate import tabulate

def fetch_config_groups(url, headers):
    """Fetch and display all config groups or a specific one based on user input."""
    group_id = input("Insert the ID of the group to retrieve (press Enter for all): ")

    try:
        if group_id:
            target_url = f"{url}/master/groups/{group_id}"
        else:
            target_url = f"{url}/products/stream/groups"

        response = requests.get(target_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        groups = data["items"] if "items" in data else [data]
        if not groups:
            print("No configuration groups found.")
            return

        table_data = []
        for group in groups:
            table_data.append({
                "ID": group.get("id", "N/A"),
                "Name": group.get("name", "N/A"),
                "Version": group.get("configVersion", "N/A"),
                "On-Prem": group.get("onPrem", "N/A"),
                "Provisioned": group.get("provisioned", "N/A"),
                "Cloud": f"{group.get('cloud', {}).get('provider', 'On-Prem')} / {group.get('cloud', {}).get('region', '')}",
                "Description": group.get("description", "N/A")
            })

        print(tabulate(table_data, headers="keys", tablefmt="github"))

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    # Generic exception
    except Exception as e:
        print(f"Unexpected error: {e}")

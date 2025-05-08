import requests
import os
from tabulate import tabulate


def upload_lookup(url, headers, filepath=None, lookup_id=None):
    while not filepath or not os.path.isfile(filepath):
        filepath = input("Enter path to CSV file: ").strip()
        filepath = os.path.normpath(filepath)
        if os.path.isfile(filepath):
            print(f"File found: {filepath}")
        else:
            print("Invalid file path. Please try again.")

    filename = os.path.basename(filepath)
    upload_url = f"{url}/system/lookups?filename={filename}"
    upload_headers = headers.copy()
    upload_headers['Content-Type'] = 'text/csv'

    try:
        with open(filepath, 'rb') as f:
            print("Uploading file...")
            response = requests.put(upload_url, headers=upload_headers, data=f, timeout=15)
            response.raise_for_status()
        print(f"Upload successful: {response.status_code}")
        file_info = response.json()
        uploaded_filename = file_info.get("filename", filename)
    except (requests.RequestException, ValueError) as e:
        print(f"Upload failed: {e}")
        return

    if not lookup_id:
        lookup_id = input("Enter lookup ID: ").strip()

    post_headers = headers.copy()
    post_headers['Content-Type'] = 'application/json'
    post_data = {
        "id": lookup_id,
        "fileInfo": {"filename": uploaded_filename}
    }

    try:
        response = requests.post(upload_url, headers=post_headers, json=post_data)
        response.raise_for_status()
        print(f"Lookup registered: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to register lookup: {e} - {response.text}")


def get_lookup(url, headers):
    lookup_id = input("Enter lookup ID (leave blank for all): ").strip()
    lookup_url = f"{url}/system/lookups" + (f"/{lookup_id}" if lookup_id else "")

    try:
        response = requests.get(lookup_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        items = data['items'] if isinstance(data, dict) and 'items' in data else [data]

        table_data = [
            {
                'ID': item.get('id', ''),
                'Size': item.get('size', ''),
                'Version': item.get('version', '')
            }
            for item in items
        ]
        print(tabulate(table_data, headers='keys', tablefmt='github'))

    except requests.RequestException as e:
        print(f"Failed to retrieve lookup(s): {e}")


def remove_lookup(url, headers):
    lookup_id = input("Enter lookup ID to delete: ").strip()
    if not lookup_id:
        print("Lookup ID is required.")
        return

    delete_url = f"{url}/system/lookups/{lookup_id}"

    try:
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()
        print("Lookup removed successfully.")
    except requests.RequestException as e:
        print(f"Failed to remove lookup: {e}")

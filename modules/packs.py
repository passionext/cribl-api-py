import requests
import json
from tabulate import tabulate

PACKS = []


def packs_info(url, headers):
    try:
        # Make the GET request to retrieve info on packs
        response = requests.get(url + "/packs", headers=headers)

        # Check if the response status is successful
        if response.status_code == 200:
            data = response.json()
            packs = data.get("items", [])

            # Prepare the table data by iterating through each pack
            table_data = []
            for pack in packs:
                table_data.append([
                    pack['displayName'],  # Pack name
                    pack['version'],  # Pack version
                    pack.get('author', 'N/A'),  # Pack author (default to 'N/A' if not found)
                    pack['id'],  # Pack ID
                    pack['source'],  # Pack source
                    pack.get('description', 'N/A')  # Pack description (default to 'N/A' if not found)
                ])

            # Print the table using tabulate for a formatted output
            headers = ["Name", "Version", "Author", "ID", "Source", "Description"]
            print("\nAvailable Packs:\n")
            print(tabulate(table_data, headers=headers, tablefmt='github'))

        else:
            # Handle unsuccessful response (non-200 status code)
            print(f"Failed to retrieve packs info: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error occurred while fetching pack info: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")


def packs_install(url, headers):
    try:
        # Ask the user for the pack ID to install
        pack_id = input("Enter the pack ID to install: ").strip()

        # Make the POST request to install the pack
        data = {
            "id": pack_id,  # ID of the pack to install
        }
        response = requests.post(url + "/packs", json=data, headers=headers)

        # Check if the pack was installed successfully
        if response.status_code == 200:
            print(f"Pack {pack_id} installed successfully.")
        else:
            # Handle unsuccessful response (non-200 status code)
            print(f"Failed to install pack {pack_id}: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error occurred while installing the pack: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")

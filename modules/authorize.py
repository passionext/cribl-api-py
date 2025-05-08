from tabulate import tabulate
import requests

def get_auth_policy(base_url, headers):
    """Fetch and display the client's authorization policy as a table."""
    # Generate the URL for the authorization policy endpoint.
    url = f"{base_url}/authorize/policy"
    # Make the GET request to fetch the authorization policy. No body is needed for this request.
    response = requests.get(url, headers=headers)
    # Check if the response status code is 200 (OK).
    if response.status_code == 200:
        data = response.json()
        # Make sure 'items' exists in the response
        if "items" not in data:
            print("Unexpected response format: 'items' key not found.")
            return
        # Build table rows
        rows = [[item["object"], ", ".join(item["actions"])] for item in data["items"]]
        # Display table
        print(tabulate(rows, headers=["Object", "Actions"], tablefmt="grid"))
    else:
        print(f"Failed to get auth policy: {response.status_code} - {response.text}")



    
def get_roles(base_url, headers):
    """Fetch and display the client's roles as a table."""
    # Generate the URL for the roles endpoint.
    url = f"{base_url}/authorize/roles"
    # Make the GET request to fetch the client's roles. No body is needed for this request.
    response = requests.get(url, headers=headers)
    # Check if the response status code is 200 (OK).
    if response.status_code == 200:
        data = response.json()
        # Create a list of lists, where each item is a row.
        rows = [[item] for item in data["items"]]
        # Print using tabulate for a clean output
        print(tabulate(rows, headers=["Roles"], tablefmt="grid"))
    else:
        print(f"Failed to get auth policy: {response.status_code} - {response.text}")


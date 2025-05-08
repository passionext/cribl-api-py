import requests
import json
import tabulate


VALID_TYPES = {
    "string",
    "number",
    "encrypted string",
    "boolean",
    "array",
    "object",
    "expression",
    "any"
}


def is_number(value):
    """Check if the value is a number."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_boolean(value):
    """Check if the value is a boolean."""
    return str(value).lower() in {"true", "false"}


def is_array(value):
    """Check if the value is an array (better known as list)."""
    try:
        val = json.loads(value)
        return isinstance(val, list)
    except (json.JSONDecodeError, TypeError):
        return False


def is_object(value):
    """Check if the value is an object"""
    try:
        val = json.loads(value)
        return isinstance(val, dict)
    except (json.JSONDecodeError, TypeError):
        return False


def table_generator(data):
     # Table headers
        headers = [ "Type", "Library", "Value", "Description", "Tags", "ID"]
            
        # Create table data with the items from the response
        table_data = [
            [item['type'], item['lib'], item.get('value', 'N/A'), item.get('description', 'N/A'), item.get('tags', 'N/A'),item['id']]
            for item in data['items']
        ]
            
        # Generating and printing the table
        print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=50))


def create_global_variable(url,headers):
    """This function creates a global variable in Cribl Stream."""
    # Generate a variable to check if the type is valid.
    is_valid_type = False
    is_valid_value = False
    is_pack_decided = False
    while not is_pack_decided:
        ans = input("Is this variable in a pack? (Y/N): ").strip().lower()
        if ans == 'y':
            pack = input("Enter pack name: ").strip()
            url = f"{url}/p/{pack}/lib/vars"
            is_pack_decided = True
        elif ans == 'n':
            url = f"{url}/lib/vars"
            is_pack_decided = True
        else:
            print("Please enter 'Y' or 'N'.")
    # Generate the URL for creating a global variable.

    # Set the values of the body's request.
    id = input("Enter variable ID: ").strip()
    description = input("Enter variable description (optional): ")
    # This loop will continue until a valid type is entered.
    while not is_valid_type:
        var_type = input("Enter a variable type: ").strip().lower()
        if var_type in VALID_TYPES:
            print(f"'{var_type}' is a valid type.")
            is_valid_type = True
        else:
            print(f"'{var_type}' is not valid. Please choose from: {', '.join(VALID_TYPES)}")
    while not is_valid_value:
        value = input("Enter variable value: ").strip()
        if var_type == "number":
            if is_number(value):
                print(f"'{value}' is a valid number.")
                is_valid_value = True
            else:
                print(f"'{value}' is not a valid number.")
        elif var_type == "boolean":
            if is_boolean(value):
                print(f"'{value}' is a valid boolean.")
                is_valid_value = True
            else:
                print(f"'{value}' is not a valid boolean.")
        elif var_type == "array":
            if is_array(value):
                print(f"'{value}' is a valid array.")
                is_valid_value = True
            else:
                print(f"'{value}' is not a valid array.")
        elif var_type == "object":
            if is_object(value):
                print(f"'{value}' is a valid object.")
                is_valid_value = True
            else:
                print(f"'{value}' is not a valid object.")
        else:
            print(f"'{value}' is a valid value.")
            is_valid_value = True

    tags = input("Enter variable tag (optional): ").strip()

    # Create the body of the request.
    data = {
        "id": id,
        "lib": "custom",
        "description": description,
        "type": var_type,
        "value": value,
        "tags": tags,
    }

    # Send the request to the Cribl Stream API. Save the response Ojbect in <response>.
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful (status code 200).
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create variable: {response.status_code}, {response.text}")

def get_variables(url, headers):
    """This function retrieves global variables from Cribl Stream."""
    # Generate the URL for retrieving global variables.
    is_pack_decided = False
    while not is_pack_decided:
        ans = input("Is this variable in a pack? (Y/N): ").strip().lower()
        if ans == 'y':
            pack = input("Enter pack name: ").strip()
            url = f"{url}/p/{pack}/lib/vars"
            is_pack_decided = True
        elif ans == 'n':
            url = f"{url}/lib/vars"
            is_pack_decided = True
        else:
            print("Please enter 'Y' or 'N'.")
    # Send the request to the Cribl Stream API. Save the response Ojbect in <response>.
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        table_generator(data)
        
    else:
        raise Exception(f"Failed to retrieve variables: {response.status_code}, {response.text}")
    # Check if the request was successful (status code 200).
    if response.status_code == 200:
        pass
        #print(response.json())
    else:
        raise Exception(f"Failed to create variable: {response.status_code}, {response.text}")
    

def get_variable_byId(url, headers):
    """This function retrieves a global variable by ID from Cribl Stream."""
    # Insert the ID of the variable you want to retrieve.
    id = input("Enter variable ID: ").strip()
    # Ask if it's part of a pack
    is_pack_decided = False

    while not is_pack_decided:
        ans = input("Is this variable in a pack? (Y/N): ").strip().lower()
        if ans == 'y':
            pack = input("Enter pack name: ").strip()
            url = f"{url}/p/{pack}/lib/vars/{id}"
            is_pack_decided = True
        elif ans == 'n':
            url = f"{url}/lib/vars/{id}"
            is_pack_decided = True
        else:
            print("Please enter 'Y' or 'N'.")
    
    # Send the request to the Cribl Stream API. Save the response Ojbect in <response>.
    response = requests.get(url, headers=headers)
    data = response.json()
    # Check if the request was successful (status code 200).
    if response.status_code == 200:
        table_generator(data) 
    else:
        raise Exception(f"Failed to create variable: {response.status_code}, {response.text}")
    
def delete_variable(url, headers):
    # Insert the ID of the variable you want to delete.
    id = input("Enter variable ID: ").strip()
    # Ask if it's part of a pack
    is_pack_decided = False
    while not is_pack_decided:
        ans = input("Is this variable in a pack? (Y/N): ").strip().lower()
        if ans == 'y':
            pack = input("Enter pack name: ").strip()
            url = f"{url}/p/{pack}/lib/vars/{id}"
            is_pack_decided = True
        elif ans == 'n':
            url = f"{url}/lib/vars/{id}"
            is_pack_decided = True
        else:
            print("Please enter 'Y' or 'N'.")

    # Send the request to the Cribl Stream API. Save the response Ojbect in <response>.
    response = requests.delete(url, headers=headers)
    # Check if the request was successful (status code 200).
    if response.status_code == 200:
        print(f"Variable with ID {id} deleted successfully.")
    else:
        raise Exception(f"Failed to delete variable: {response.status_code}, {response.text}")
    
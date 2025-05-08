import requests
from tabulate import tabulate


def has_slashes(path: str) -> bool:
    return path.startswith("/") and path.endswith("/")

def regex_table(data):
    table_data = [
        [item['id'], item['description'], item.get('tags', ''), item['regex']]
        for item in data['items']
    ]

    # Define headers
    headers = ["ID", "Description", "Tags", "Regex"]

    # Print table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
def create_regex(url,headers):
    url=f"{url}/lib/regex"
    is_slashed = False
    reg_id = input("Enter regex ID: ")
    description = input("Enter regex (optional): ")
    while not is_slashed:
        regex = input("Enter regex pattern (remember to use the / at the beginning and the end of the expression) : ")
        if has_slashes(regex):
            is_slashed = True
        else:
            print("Invalid regex. Put the \"/\" at the beginning and the end of the expression.")
    sampleData = input("Enter regex sample data (optional): ")
    tags = input("Enter regex tags (optional): ")

    data = {
        "id": reg_id,
        "lib": "custom",
        "description": description,
        "regex": regex,
        "sampleData": sampleData,
        "tags": tags
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully created regex")
    else:
        print(response.text)

def update_regex(url,headers):

    is_slashed = False
    reg_id = input("Enter regex ID: ")
    url = f"{url}/lib/regex/{reg_id}"
    description = input("Enter regex (optional): ")
    while not is_slashed:
        regex = input("Enter regex pattern (remember to use the / at the beginning and the end of the expression) : ")
        if has_slashes(regex):
            is_slashed = True
        else:
            print("Invalid regex. Put the \"/\" at the beginning and the end of the expression.")
    sampleData = input("Enter regex sample data (optional): ")
    tags = input("Enter regex tags (optional): ")

    data = {
        "id": reg_id,
        "lib": "custom",
        "description": description,
        "regex": regex,
        "sampleData": sampleData,
        "tags": tags
    }

    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully created regex")
    else:
        print(response.text)

def delete_regex(url,headers):
    reg_id = input("Insert the regex ID that you need to remove: ")
    url = f"{url}/lib/regex/{reg_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("Successfully created regex")
    else:
        print(response.text)

def get_regex(url,headers):
    reg_id = input("Insert the regex ID. If you want to retrieve them all, press Enter without any choice: ")
    if not reg_id:
        url=f"{url}/lib/regex"
    else:
        url=f"{url}/lib/regex/{reg_id}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        regex_table(data)
    else:
        print(response.text)

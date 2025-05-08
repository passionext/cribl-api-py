import requests
from InquirerPy import inquirer
from InquirerPy.separator import Separator

# Internal modules
from modules import certificates, processes, packs, groups, lookups, auth, authorize, globalVariables, worker, regex
from config.config import API_BASE_URL,  API_GROUP_URL

headers = {
    "Content-Type": "application/json"
}


def health():
    url = f"{API_BASE_URL}/health"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("✅ Health check successful:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return None


# Mapping category choices to their corresponding functions
main_menu = {
    "Worker": {
        "Worker Count": lambda: worker.worker_count(API_BASE_URL, headers),
        "Worker Info": lambda: worker.worker_info(API_BASE_URL, headers),
        "Restart Workers": lambda: worker.restart_workers(API_BASE_URL, headers),
    },
    "Processes": {
        "Get Processes": lambda: processes.get_processes(API_BASE_URL, headers),
        "List Upgrades": lambda: processes.get_list_upgrades(API_BASE_URL, headers),
        "Restart Cribl": lambda: processes.restart_cribl(API_BASE_URL, headers),
    },
    "Lookups": {
        "Upload Lookup": lambda: lookups.upload_lookup(API_GROUP_URL, headers),
        "Get Lookup": lambda: lookups.get_lookup(API_GROUP_URL, headers),
        "Remove Lookup": lambda: lookups.remove_lookup(API_GROUP_URL, headers),
    },
    "Regex": {
        "Create Regex": lambda: regex.create_regex(API_GROUP_URL, headers),
        "Update Regex": lambda: regex.update_regex(API_GROUP_URL, headers),
        "Get Regex": lambda: regex.get_regex(API_BASE_URL, headers),
        "Delete Regex": lambda: regex.delete_regex(API_GROUP_URL, headers),
    },
    "Certificates": {
        "Get Certificates": lambda: certificates.get_certificates(API_BASE_URL, headers)
    },
    "Packs": {
        "List Packs": lambda: packs.packs_info(API_GROUP_URL, headers),
        "Install Pack": lambda: packs.packs_install(API_GROUP_URL, headers),
    },
    "Groups": {
        "Fetch Config Groups": lambda: groups.fetch_config_groups(API_BASE_URL, headers),
    },
    "Global Variables": {
        "Get Variables": lambda: globalVariables.get_variables(API_GROUP_URL, headers),
        "Create Variable": lambda: globalVariables.create_global_variable(API_GROUP_URL, headers),
        "Get Variable by ID": lambda: globalVariables.get_variable_byId(API_GROUP_URL, headers),
    },
    "Authorization": {
        "Get Auth Policies": lambda: authorize.get_auth_policy(API_BASE_URL, headers),
        "Get Roles": lambda: authorize.get_roles(API_BASE_URL, headers),
    },
    "System": {
        "Health Check": health,
    }
}


def run_cli():
    while True:
        main_choice = inquirer.select(
            message="Select a module:",
            choices=list(main_menu.keys()) + [Separator(), "Exit"],
        ).execute()

        if main_choice == "Exit":
            print("Exiting.")
            break

        actions = main_menu[main_choice]
        action_choice = inquirer.select(
            message=f"Select an action for {main_choice}:",
            choices=list(actions.keys()) + [Separator(), "Back"],
        ).execute()

        if action_choice == "Back":
            continue

        try:
            print(f"\n▶ Executing: {action_choice}\n")
            actions[action_choice]()  # Run the selected function
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Authenticating...")

    try:
        token = auth.get_token()
        headers.update({"Authorization": f"Bearer {token}"})
        print("Token retrieved.")
        run_cli()
    except auth.AuthError as e:
        print(f"Authentication failed: {e}")

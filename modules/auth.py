import requests
from config import USER, PASSWORD, API_AUTH_URL

class AuthError(Exception):
    """Custom exception for authentication errors."""
    def __init__(self, message, status_code=None, response_text=None):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)

def get_token():
    """Get authentication token from Cribl API"""

    # Create the headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    # Create the data payload for the request
    data = {
        "grant_type": "client_credentials",
        "client_id": USER,
        "client_secret": PASSWORD,
        "audience": "https://api.cribl.cloud"  # Incorrect URL to simulate failure
    }

    try:
        response = requests.post(API_AUTH_URL, headers=headers, json=data)
        response.raise_for_status()  # This checks for 4xx/5xx errors automatically

        # Try to get the access token from the response (this might raise a JSONDecodeError if the response is not valid JSON)
        data = response.json()
        token = data.get("access_token")

        if not token:
            raise AuthError("Token not found in response", response.status_code, response.text)

        return token


    except requests.exceptions.RequestException as req_err:
        # Any connection errors (timeouts, DNS issues, etc.)
        raise AuthError(f"Request error occurred: {req_err}", None, str(req_err))
    
    except ValueError as val_err:
        # If response cannot be parsed as JSON
        raise AuthError(f"Failed to parse response: {val_err}", response.status_code, response.text)




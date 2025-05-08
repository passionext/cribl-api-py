import requests

def display_certificates(data):
    """Print full certificates including the cert (which includes private key) and CA."""
    certs = data.get("items") if isinstance(data, dict) and "items" in data else [data]

    for idx, cert in enumerate(certs):
        print(f"\n=== Certificate [{idx}] ===")
        print(f"certPath: {cert.get('certPath', 'N/A')}\n")

        print("----- BEGIN FULL CERTIFICATE (incl. Private Key) -----")
        print(cert.get("cert", "N/A"))
        print("----- END FULL CERTIFICATE -----\n")

        print("----- BEGIN CA CERTIFICATE -----")
        print(cert.get("ca", "N/A"))
        print("----- END CA CERTIFICATE -----\n")


def get_certificates(url, headers):
    """Fetch and display all certificates from the server."""
    cert_id = input("Insert the ID of the certificate to retrieve (press Enter for all): ")

    target_url = f"{url}/system/certificates"
    if cert_id:
        target_url += f"/{cert_id}"

    try:
        response = requests.get(target_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        display_certificates(data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError:
        print("Failed to parse JSON response.")

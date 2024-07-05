import requests
import platform
import json
import os

def get_system_info():
    system_info = {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine()
    }
    return system_info

## get virtualization info (none, docker, proxmox)
## @TODO

def send_system_info(url, token):
    system_info = get_system_info()
    try:
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        response = requests.post(url, json=system_info, headers=headers, verify=False)  # Verify SSL certificate
        if response.status_code == 200:
            print("System info sent successfully!")
        else:
            print("Failed to send system info. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error sending system info:", e)

def get_token(url, username, password):
    try:
        response = requests.post(url, auth=(username, password), verify=False)  # Verify SSL certificate
        if response.status_code == 200:
            token = json.loads(response.text)['token']
            return token
        else:
            print("Failed to get token. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error getting token:", e)
        return None

if __name__ == "__main__":
    SERVER_URL = os.getenv('SERVER_URL')
    # server_url = "http://localhost:8000/add"
    AUTH_URL = os.getenv('SERVER_URL')
    # auth_url = "http://localhost:8000/login"
    # username = "username"
    # password = "password"

    token = get_token(auth_url, username, password)
    if token:
        send_system_info(server_url, token)

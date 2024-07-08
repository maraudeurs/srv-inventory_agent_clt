import requests
import json
import os
import logging

from utils.logger_config import setup_logging
from system_info.virtualization_discover import check_virtualization

def send_system_info(url, token, system_info):
    try:
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        response = requests.post(url, json=system_info, headers=headers, verify=False)
        if response.status_code == 200:
            print("System info sent successfully!")
        else:
            print("Failed to send system info. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error sending system info:", e)

def get_token(url, username, password):
    try:
        response = requests.post(url, auth=(username, password), verify=False)
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

    ## Manage logging
    setup_logging()
    logger = logging.getLogger(__name__)

    ## Get virtualization info
    system_virtualization_installed = check_virtualization()
    logger.debug(system_virtualization_installed)

    ## Get system info

    # SERVER_URL = os.getenv('SERVER_URL')
    # # server_url = "http://localhost:8000/add"
    # AUTH_URL = os.getenv('SERVER_URL')
    # # auth_url = "http://localhost:8000/login"
    # # username = "username"
    # # password = "password"

    # token = get_token(auth_url, username, password)
    # if token:
    #     system_info = get_system_info()
    #     send_system_info(server_url, token; system_info)

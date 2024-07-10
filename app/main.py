import requests
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from utils.logger_config import setup_logging
from system_info.system_info import get_system_info
from system_info.virtualization_discover import check_virtualization

def send_system_info(url, discovery_generic_user, discovery_generic_password, system_info):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=system_info, headers=headers, verify=False, auth=(discovery_generic_user, discovery_generic_password))
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.warning(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
    except requests.exceptions.RequestException as req_err:
        logger.warning(f"Request error occurred: {req_err}")
    except Exception as err:
        logger.warning(f"Other error occurred: {err}")


if __name__ == "__main__":

    ## get inventory_agent-srv parameters
    load_dotenv()
    server_url = os.getenv('SERVER_URL')
    discovery_generic_user = os.getenv('DISCOVERY_GENERIC_USER')
    discovery_generic_password = os.getenv('DISCOVERY_GENERIC_PASSWORD')
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_output = os.getenv("LOG_OUTPUT", "stdout")
    log_file = os.getenv("LOG_FILE", "/var/log/srv_inventory_clt.log")

    ## Manage logging
    setup_logging(log_level, log_output, log_file)
    logger = logging.getLogger(__name__)

    ## Get virtualization info
    system_virtualization_installed = check_virtualization(logger)
    logger.debug(system_virtualization_installed)

    ## Get system info
    system_info_data = get_system_info()

    ## Send system info
    system_info = {
        "name": system_info_data['hostname'],
        "description": "test",
        "main_ipv4" : system_info_data['system_main_ipv4'],
        "ip_v4_list" : system_info_data['system_ipv4_list'],
        "ip_v6_list" : system_info_data['system_ipv6_list'],
        "status" : "active",
        "inventory_source_method" : "inventory_agent_clt",
        "system_os" : system_info_data['system'],
        "system_release" : system_info_data['release'],
        "system_architecture" : system_info_data['architecture'],
        "hostname" : system_info_data['hostname'],
        "python_version" : system_info_data['python_version'],
        "virtualization_method" : system_virtualization_installed,
        "update_date" : datetime.now().isoformat(),
    }
    send_system_info(server_url, discovery_generic_user, discovery_generic_password, system_info)

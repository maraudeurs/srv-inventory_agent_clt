import platform
import psutil
import socket
import requests

def get_system_info() -> dict:
    """
    Get information about the system (hostname, system, release, architecture, python version)

    Returns:
        dict: dict named "system_info" that contain system data
    """
    system_info = {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "system_main_ipv4" : get_main_ipv4_address(),
        "system_ipv4_list": get_ipv4_addresses(),
        "system_ipv6_list": get_ipv6_addresses()
    }
    return system_info

def get_main_ipv4_address() -> str:
    """
    Get the main (public) ipv4 for the system

    Returns:
        string: main/public ipv4 string adress
    """
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()['ip']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def get_ipv4_addresses() -> list:
    """
    Get all ipv4 from all network interfaces on the system

    Returns:
        list: list of ipv4 string adresses
    """
    ipv4_addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_addresses.append(addr.address)
    return ipv4_addresses

def get_ipv6_addresses() -> list:
    """
    Get all ipv6 from all network interfaces on the system

    Returns:
        list: list of ipv6 string adresses
    """
    ipv6_addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET6:
                ipv6_addresses.append(addr.address)
    return ipv6_addresses
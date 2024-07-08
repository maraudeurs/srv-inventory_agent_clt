import platform
import psutil

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
        "python_version": plateform.python_version(),
        "system_ipv4_list": get_ipv4_addresses(),
        "system_ipv6_list": get_ipv6_addresses()
    }
    return system_info

def get_ipv4_addresses() -> list:
    """
    Get all ipv4 from all network interfaces on the system

    Returns:
        list: list of ipv4 string adresses
    """
    ipv4_addresses = {}
    for interface, addrs in psutil.net_if_addrs().items():
        ipv4_addresses[interface] = []
        for addr in addrs:
            if addr.family == psutil.AF_INET:
                ipv4_addresses[interface].append(addr.address)
    return ipv4_addresses

def get_ipv6_addresses() -> list:
    """
    Get all ipv6 from all network interfaces on the system

    Returns:
        list: list of ipv6 string adresses
    """
    ipv6_addresses = {}
    for interface, addrs in psutil.net_if_addrs().items():
        ipv6_addresses[interface] = []
        for addr in addrs:
            if addr.family == psutil.AF_INET6:
                ipv6_addresses[interface].append(addr.address)
    return ipv6_addresses
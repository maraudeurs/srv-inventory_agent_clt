import subprocess
import logging
from utils.logger_config import setup_logging

## Manage logging
setup_logging()
logger = logging.getLogger('__name__')

def check_command(command: str) -> str:
    """
    Utility function to check if a command exists and run it.

    Args:
        command : linux command string

    Returns:
        str : command output result or None if error
    """
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        logger.debug(f"Command '{' '.join(command)}' failed: {e}")
        return None
    except FileNotFoundError:
        logger.debug(f"Command '{' '.join(command)}' not found.")
        return None

def check_service(service_name: str) -> bool:
    """
    Check if a system service is active.

    Args:
        service_name : systemctl service name as string

    Returns:
        bool: return True if service is active else return False
    """
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.debug(result.stdout.decode().strip() == 'active')
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        logger.debug("Systemctl command not found.")
        return False

def check_docker() -> bool:
    """
    Check if Docker is installed and running.

    Returns:
        bool: return True if docker is installed and active else return False
    """
    logger.debug("Checking for Docker...")
    docker_version = check_command(['docker', '--version'])
    if docker_version:
        logger.debug(f"Docker is installed: {docker_version}")
        if check_service('docker'):
            logger.debug("Docker service is active.")
            return True
        else:
            logger.debug("Docker service is not active.")
            return False
    else:
        logger.debug("Docker is not installed.")
        return False

def check_proxmox() -> bool:
    """
    Check if Proxmox VE is installed and running.

    Returns:
        bool: return True if Proxmox is installed and active else return False
    """
    logger.debug("Checking for Proxmox VE...")
    proxmox_version = check_command(['pveversion'])
    if proxmox_version:
        logger.debug(f"Proxmox VE is installed: {proxmox_version}")
        if check_service('pvedaemon'):
            logger.debug("Proxmox VE service is active.")
            return True
        else:
            logger.debug("Proxmox VE service is not active.")
            return False
    else:
        logger.debug("Proxmox VE is not installed.")
        return False

def check_lxc() -> bool:
    """
    Check if LXC is installed and running.

    Returns:
        bool: return True if LXC is installed and active else return False
    """
    logger.debug("Checking for LXC...")
    lxc_config = check_command(['lxc-checkconfig'])
    if lxc_config:
        logger.debug("LXC is installed.")
        if check_service('lxc'):
            logger.debug("LXC service is active.")
            return True
        else:
            logger.debug("LXC service is not active.")
            return False
    else:
        logger.debug("LXC is not installed.")
        return False

def check_qemu() -> bool:
    """
    Check if QEMU is installed and running.

    Returns:
        bool: return True if QEMU is installed and active else return False
    """
    logger.debug("Checking for QEMU...")
    qemu_version = check_command(['qemu-system-x86_64', '--version'])
    if qemu_version:
        logger.debug(f"QEMU is installed: {qemu_version}")
        return True
    else:
        logger.debug("QEMU is not installed.")
        return False

def check_kvm() -> bool:
    """
    Check if KVM is installed and running.

    Returns:
        bool: return True if KVM is installed and active else return False
    """
    logger.debug("Checking for KVM...")
    kvm_version = check_command(['kvm', '--version'])
    if kvm_version:
        logger.debug(f"KVM is installed: {kvm_version}")
        return True
    else:
        logger.debug("KVM is not installed.")
        return False

def check_virtualization() -> list:
    """
    Check on system if any of virtualization method in :
        - docker
        - proxmox
        - lxc
        - quemu
        - kvm
    exist.

    Returns:
        list: list of virtualization method on the system
    """
    system_virtualization_installed = []
    try:
        if check_docker():
            system_virtualization_installed.append("docker")
    except Exception as e:
        logger.debug(f"Error checking Docker: {e}")

    try:
        if check_proxmox():
            system_virtualization_installed.append("proxmox")
    except Exception as e:
        logger.debug(f"Error checking Proxmox VE: {e}")

    try:
        if check_lxc():
            system_virtualization_installed.append("lxc")
    except Exception as e:
        logger.debug(f"Error checking LXC: {e}")

    try:
        if check_qemu():
            system_virtualization_installed.append("qemu")
    except Exception as e:
        logger.debug(f"Error checking QEMU: {e}")

    try:
        if check_kvm():
            system_virtualization_installed.append("kvm")
    except Exception as e:
        logger.debug(f"Error checking KVM: {e}")

    return system_virtualization_installed
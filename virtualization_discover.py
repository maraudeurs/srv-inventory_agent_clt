import subprocess

def check_command(command):
    """Utility function to check if a command exists and run it."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError:
        return None

def check_service(service_name):
    """Check if a system service is active."""
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip() == 'active'
    except subprocess.CalledProcessError:
        return False

def check_docker():
    """Check if Docker is installed and running."""

    docker_version = check_command(['docker', '--version'])
    if docker_version:
        print(f"Docker is installed: {docker_version}")
        if check_service('docker'):
            print("Docker service is active.")
        else:
            print("Docker service is not active.")
    else:
        print("Docker is not installed.")

def check_proxmox():
    """Check if Proxmox VE is installed and running."""
    print("Checking for Proxmox VE...")
    proxmox_version = check_command(['pveversion'])
    if proxmox_version:
        print(f"Proxmox VE is installed: {proxmox_version}")
        if check_service('pvedaemon'):
            print("Proxmox VE service is active.")
        else:
            print("Proxmox VE service is not active.")
    else:
        print("Proxmox VE is not installed.")

def check_lxc():
    """Check if LXC is installed and running."""
    print("Checking for LXC...")
    lxc_config = check_command(['lxc-checkconfig'])
    if lxc_config:
        print("LXC is installed.")
        if check_service('lxc'):
            print("LXC service is active.")
        else:
            print("LXC service is not active.")
    else:
        print("LXC is not installed.")

def check_qemu_kvm():
    """Check if QEMU/KVM is installed and running."""
    print("Checking for QEMU/KVM...")
    kvm_version = check_command(['kvm', '--version'])
    qemu_version = check_command(['qemu-system-x86_64', '--version'])
    if kvm_version:
        print(f"KVM is installed: {kvm_version}")
    elif qemu_version:
        print(f"QEMU is installed: {qemu_version}")
    else:
        print("QEMU/KVM is not installed.")

    if check_service('libvirtd'):
        print("libvirtd service is active.")
    else:
        print("libvirtd service is not active.")

def main():
    check_docker()
    check_proxmox()
    check_lxc()
    check_qemu_kvm()

if __name__ == "__main__":
    main()

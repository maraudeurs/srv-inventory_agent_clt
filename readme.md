# srv-inventory_agent_clt

## Description

A simple inventory agent that send data to a server through REST HTTP request.

Current supported inventory data :
- name
- description
- main_ipv4
- ip_v4_list
- ip_v6_list
- status
- inventory_source_method"
- system_os
- system_release
- system_architecture
- hostname
- python_version
- virtualization_method: docker, kvm, proxmox, quemu
- update_date

### technical data

- python version : 3.11
- pip packages : see [requirements file](./requirements.txt)

## Usage

### classic python script

```
python -m venv venv
source /venv/bin/activate
python -m pip install -r requirements.txt
python app/main.py
```


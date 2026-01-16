import argparse
import os.path
import pprint
import urllib.request
import yaml

INVENTORY_FILE = 'inventory.yaml'
PRIV_INVENTORY_FILE = 'inventory.private.yaml'
ENV_FILE = 'config/shell/env.sh'
HOSTS_FILE = 'config/os/hosts'
ANSIBLE_INV_FILE = 'config/ansible/inventory.yaml'
KEY_PATH_FMT = os.path.abspath('config/ssh/{key_name}')
LEAD_MARKER = '### BEGIN INVUTIL CONTENT'
TAIL_MARKER = '### END INVUTIL CONTENT'

ANSIBLE_SKEL = 'config/ansible/inventory.skel'
ANSIBLE_HOST = 'ansible_host'
ANSIBLE_KEY = 'ansible_ssh_private_key_file'
ANSIBLE_USER = 'ansible_user'
ANSIBLE_MACHINE_GROUP = 'machines'
ANSIBLE_VM_GROUP = 'vms'
ANSIBLE_NETDEV_GROUP = 'network_devices'

def loadYaml(filename) -> dict:
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def openForWrite(path):
    print(f" - Creating file: {path}")
    if not os.path.exists(path):
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    return open(path, 'w')

def mergeInventories(base_inv, priv_inv):
    for cat_name,category in base_inv.items():
        if cat_name not in priv_inv:
            continue
        for entry_name,entry in category.items():
            if entry_name in priv_inv[cat_name]:
                for key in priv_inv[cat_name][entry_name].keys():
                    entry[key] = priv_inv[cat_name][entry_name][key]
    return base_inv

def hasValidPrimaryIP(entry):
    return entry.get('primary_ip', None) and entry['primary_ip'].lower() != 'dhcp'

def writeKubeConfig(inventory, env_file):
    primary = inventory['kubernetes']['primary']
    env_file.write('# Kubernetes\n')
    env_file.write(f"export KUBECONFIG={primary['kubeconfig']}\n")
    env_file.write("# Talos Configuration\n")
    env_file.write(f"export TALOSCONFIG={primary['talos_config']}\n")
    env_file.write(f"export talos_config_dir={primary['config_dir']}\n")
    env_file.write(f"export talos_cp_ip={primary['control_plane']['primary_ip']}\n")
    env_file.write(f"export talos_w1_ip={primary['workers'][0]['primary_ip']}\n")
    env_file.write(f"export talos_w2_ip={primary['workers'][1]['primary_ip']}\n")

def writeGenericConfigs(entry, env_file, hosts_file, ansible_inv, group_name):
    record = {}
    if hasValidPrimaryIP(entry):
        hosts_file.write(f"{entry['primary_ip']}\t{entry['name']}\n")
        record[ANSIBLE_HOST] = entry['primary_ip']
    if entry.get('key', None):
        key_file = KEY_PATH_FMT.format(key_name=entry['key'])
        env_file.write(f"ssh-add {key_file}\n")
        record[ANSIBLE_KEY] = key_file
    if entry.get('user', None):
        record[ANSIBLE_USER] = entry['user']
    if record != {}:
        ansible_inv[group_name]['hosts'][entry['name']] = record

def writeHostConfigs(inventory, env_file, hosts_file, ansible_inv):
    hosts = inventory.get('hosts', None)
    if not hosts:
        return
    env_file.write('# Hosts\n')
    hosts_file.write('# Hosts\n')
    for host in hosts.values():
        writeGenericConfigs(host, env_file, hosts_file, ansible_inv, ANSIBLE_MACHINE_GROUP)

def writeVMConfigs(inventory, env_file, hosts_file, ansible_inv):
    vms = inventory.get('vms', None)
    if not vms:
        return
    hosts_file.write('# VMs\n')
    for vm in vms.values():
        writeGenericConfigs(vm, env_file, hosts_file, ansible_inv, ANSIBLE_VM_GROUP)

def writeNetworkDeviceConfigs(inventory, hosts_file, ansible_inv):
    devices = inventory.get('network_devices', None)
    if not devices:
        return
    hosts_file.write('# Network Devices\n')
    for device in devices.values():
        writeGenericConfigs(device, None, hosts_file, ansible_inv, ANSIBLE_NETDEV_GROUP)

def createEnvFiles(inventory):
    ansible_inv = loadYaml(ANSIBLE_SKEL)
    with openForWrite(ENV_FILE) as env_file, openForWrite(HOSTS_FILE) as hosts_file:
        hosts_file.write(LEAD_MARKER + '\n')
        writeKubeConfig(inventory, env_file)
        writeHostConfigs(inventory, env_file, hosts_file, ansible_inv)
        writeNetworkDeviceConfigs(inventory, hosts_file, ansible_inv)
        writeVMConfigs(inventory, env_file, hosts_file, ansible_inv)
        hosts_file.write(TAIL_MARKER + '\n')

    with openForWrite(ANSIBLE_INV_FILE) as ansible_file:
        ansible_file.write(yaml.dump(ansible_inv))

def pullImages(inventory):
    try:
        os.mkdir('images')
    except FileExistsError:
        pass
    for key in inventory['images']:
        entry = inventory['images'][key]
        image = entry.get('image', "")
        output = entry.get('file', "")
        if output and os.path.exists(output):
            print(f"Image already exists, skipping: entry={key}file={output}")
            continue
        if not image:
            print(f"No image URL found, skipping: entry={key}")
            continue
        print(f"Pulling image: {image}")
        urllib.request.urlretrieve(image, output)
            
def main():
    parser = argparse.ArgumentParser(description='Lab inventory helper tool')
    parser.add_argument('--pull-private', help='Pull private files from remote', action='store_true')
    parser.add_argument('--env', help='Populate various environment files from the inventory', action='store_true')
    parser.add_argument('--pull-images', help='Pull images defined in the inventory', action='store_true')

    args = parser.parse_args()
    inventory = loadYaml(INVENTORY_FILE)
    priv_inventory = loadYaml(PRIV_INVENTORY_FILE)
    merged_inventory = mergeInventories(inventory, priv_inventory)
    if args.env:
        print("Creating environment files...")
        createEnvFiles(merged_inventory)
    if args.pull_images:
        print("Pulling images...")
        pullImages(merged_inventory)

if __name__ == "__main__":
    main()
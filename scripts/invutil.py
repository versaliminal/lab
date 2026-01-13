import argparse
import os.path
import urllib.request
import yaml

INVENTORY_FILE = 'inventory.yaml'
ENV_FILE = 'env.sh'
HOSTS_FILE = 'hosts'
LEAD_MARKER = '### BEGIN INVUTIL CONTENT'
TAIL_MARKER = '### END INVUTIL CONTENT'

def loadInventory():
    with open(INVENTORY_FILE, 'r') as file:
        inventory = yaml.safe_load(file)
        return inventory

def writeKubeConfig(inventory, env_file):
    primary = inventory['kubernetes']['primary']
    env_file.write('# Kubernetes\n')
    env_file.write(f"export KUBECONFIG={primary['kubeconfig']}\n")
    env_file.write("# Talos Configuration\n")
    env_file.write(f"export TALOSCONFIG={primary['talos_config']}\n")
    env_file.write(f"export talos_config_dir={primary['config_dir']}\n")
    env_file.write(f"export talos_cp_ip={primary['control_plane']['ip']}\n")
    env_file.write(f"export talos_w1_ip={primary['workers'][0]['ip']}\n")
    env_file.write(f"export talos_w2_ip={primary['workers'][1]['ip']}\n")

def writeHostConfigs(inventory, env_file, hosts_file):
    hosts = inventory['hosts']
    env_file.write('# Hosts\n')
    for host in hosts:
        hosts_file.write(f"{host['ip']}\t{host['name']}\n")
        if host.get('key', None):
            env_file.write(f"ssh-add {host['key']}\n")

def writeVMConfigs(inventory, env_file, hosts_file):
    vms = inventory['vms']
    hosts_file.write('# VMs\n')
    for vm in vms:
        if vm.get('ip', None) and vm['ip'].lower() != 'dhcp':
            hosts_file.write(f"{vm['ip']}\t{vm['name']}\n")
        if vm.get('key', None):
            env_file.write(f"ssh-add {vm['key']}\n")

def writeNetworkDeviceConfigs(inventory, hosts_file):
    devices = inventory.get('network_devices', [])
    hosts_file.write('# Network Devices\n')
    for device in devices:
        hosts_file.write(f"{device['ip']}\t{device['name']}\n")

def createEnvFiles(inventory):
    with open(ENV_FILE, 'w') as env_file, open(HOSTS_FILE, 'w') as hosts_file:
        hosts_file.write(LEAD_MARKER + '\n')
        writeKubeConfig(inventory, env_file)
        writeHostConfigs(inventory, env_file, hosts_file)
        writeNetworkDeviceConfigs(inventory, hosts_file)
        writeVMConfigs(inventory, env_file, hosts_file)
        hosts_file.write(TAIL_MARKER + '\n')

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
    parser.add_argument('--env', help='Create an environment file', action='store_true')
    parser.add_argument('--pull', help='Pull images', action='store_true')

    args = parser.parse_args()
    inventory = loadInventory()
    if args.env:
        print("Creating env.sh and hosts file...")
        createEnvFiles(inventory)
    if args.pull:
        print("Pulling images...")
        pullImages(inventory)

if __name__ == "__main__":
    main()
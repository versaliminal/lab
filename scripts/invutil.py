import argparse
import os.path
import urllib.request
import yaml

INVENTORY_FILE = 'inventory.yaml'
ENV_FILE = 'env.sh'

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

def writeHostConfigs(inventory, env_file):
    hosts = inventory['hosts']
    env_file.write('# Hosts\n')
    for host in hosts:
        env_file.write(f"export {host['name']}_ip={host['ip']}\n")
        if host['key']:
            env_file.write(f"ssh-add {host['key']}\n")

def writeVMConfigs(inventory, env_file):
    vms = inventory['vms']
    env_file.write('# VMs\n')
    for vm in vms:
        env_file.write(f"export {vm['name']}_ip={vm['ip']}\n")

def writeNetworkDeviceConfigs(inventory, env_file):
    devices = inventory.get('network_devices', [])
    env_file.write('# Network Devices\n')
    for device in devices:
        env_file.write(f"export {device['name']}_ip={device['ip']}\n")

def createEnvFile(inventory):
    with open(ENV_FILE, 'w') as env_file:
        writeKubeConfig(inventory, env_file)
        writeHostConfigs(inventory, env_file)
        writeVMConfigs(inventory, env_file)
        writeNetworkDeviceConfigs(inventory, env_file)

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
        print("Creating environment file...")
        createEnvFile(inventory)
    if args.pull:
        print("Pulling images...")
        pullImages(inventory)

if __name__ == "__main__":
    main()
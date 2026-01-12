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

def main():
    inventory = loadInventory()
    with open(ENV_FILE, 'w') as env_file:
        writeKubeConfig(inventory, env_file)
        writeHostConfigs(inventory, env_file)
        writeVMConfigs(inventory, env_file)
        writeNetworkDeviceConfigs(inventory, env_file)

if __name__ == "__main__":
    main()
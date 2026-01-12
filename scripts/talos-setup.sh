#!/bin/bash
source config/talos/vars.sh
talosctl gen config talos-primary https://$talos_cp_ip:6443 --output-dir $talos_config_dir
talosctl apply-config --insecure --nodes $talos_cp_ip --file $talos_config_dir/controlplane.yaml
read -p "Press enter to apply to control-plane configs"
talosctl config endpoint $talos_cp_ip
talosctl config node $talos_cp_ip
read -p "Press enter to bootstrap when control plane node is ready"
talosctl bootstrap

read -p "Press enter to apply to worker configs, when control-plane is bootstrapped"
talosctl apply-config --insecure --nodes $talos_w1_ip --file $talos_config_dir/worker.yaml
talosctl apply-config --insecure --nodes $talos_w2_ip --file $talos_config_dir/worker.yaml

read -p "Press enter when all nodes are ready"
mkdir -p kubeconfig
talosctl kubeconfig kubeconfig/talos-primary
#!/bin/bash
source config/talos/vars.sh
talosctl gen config talos-primary https://$CONTROL_PLANE_IP:6443 --output-dir $CONFIG_DIR
talosctl apply-config --insecure --nodes $CONTROL_PLANE_IP --file $CONFIG_DIR/controlplane.yaml
read -p "Press enter to apply to control-plane configs"
export TALOSCONFIG=$CONFIG_DIR/talosconfig
talosctl config endpoint $CONTROL_PLANE_IP
talosctl config node $CONTROL_PLANE_IP
read -p "Press enter to bootstrap when control plane node is ready"
talosctl bootstrap

read -p "Press enter to apply to worker configs, when control-plane is bootstrapped"
talosctl apply-config --insecure --nodes $WORKER_NODE_1_IP --file $CONFIG_DIR/worker.yaml
talosctl apply-config --insecure --nodes $WORKER_NODE_2_IP --file $CONFIG_DIR/worker.yaml

read -p "Press enter when all nodes are ready"
mkdir -p kubeconfig
talosctl kubeconfig kubeconfig/talos-primary
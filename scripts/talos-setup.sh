#!/bin/bash
source config/talos/vars.sh
talosctl gen config talos-primary https://$TALOS_CP_IP:6443 --output-dir $TALOS_CFG_DIR
talosctl apply-config --insecure --nodes $TALOS_CP_IP --file $TALOS_CFG_DIR/controlplane.yaml
read -p "Press enter to apply to control-plane configs"
export TALOSCONFIG=$TALOS_CFG_DIR/talosconfig
talosctl config endpoint $TALOS_CP_IP
talosctl config node $TALOS_CP_IP
read -p "Press enter to bootstrap when control plane node is ready"
talosctl bootstrap

read -p "Press enter to apply to worker configs, when control-plane is bootstrapped"
talosctl apply-config --insecure --nodes $TALOS_N1_IP --file $TALOS_CFG_DIR/worker.yaml
talosctl apply-config --insecure --nodes $TALOS_N2_IP --file $TALOS_CFG_DIR/worker.yaml

read -p "Press enter when all nodes are ready"
mkdir -p kubeconfig
talosctl kubeconfig kubeconfig/talos-primary
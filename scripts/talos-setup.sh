#!/bin/bash
source config/talos/vars.sh
talosctl gen config talos-proxmox-cluster https://$CONTROL_PLANE_IP:6443 --output-dir config/talos
talosctl apply-config --insecure --nodes $CONTROL_PLANE_IP --file config/talos/controlplane.yaml
talosctl apply-config --insecure --nodes $WORKER_NODE_1_IP --file config/talos/worker.yaml
talosctl apply-config --insecure --nodes $WORKER_NODE_2_IP --file config/talos/worker.yaml

export TALOSCONFIG=config/talos/talosconfig
talosctl config endpoint $CONTROL_PLANE_IP
talosctl config node $CONTROL_PLANE_IP
talosctl bootstrap

talosctl kubeconfig .


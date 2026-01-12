#!/bin/bash
echo "# hosts" > env.sh
for mapping in $(yq '.hosts[] | .name + "_ip=" + .ip' inventory.yaml); do
    echo "export $mapping" >> env.sh
done

echo "# vms" >> env.sh
for mapping in $(yq '.vms[] | .name + "_ip=" + .ip' inventory.yaml); do
    echo "export $mapping" >> env.sh
done

echo "# k8s" >> env.sh
conf_dir=$(yq '.kubernetes[0].config_dir' inventory.yaml)
echo "export talos_config_dir=$(pwd)/$conf_dir/" >> env.sh
kconf=$(yq '.kubernetes[0].kubeconfig' inventory.yaml)
echo "export KUBECONFIG=$(pwd)/$kconf" >> env.sh
tconf=$(yq '.kubernetes[0].talos_config' inventory.yaml)
echo "export TALOSCONFIG=$(pwd)/$tconf" >> env.sh
cp_ip=$(yq '.kubernetes[0].control_plane | "talos_cp_ip=" + .ip' inventory.yaml);
echo "export $cp_ip" >> env.sh
w1_ip=$(yq 'explode(.) | .kubernetes[0].workers[0] | "talos_w1_ip=" + .ip' inventory.yaml)
echo "export $w1_ip" >> env.sh
w2_ip=$(yq 'explode(.) | .kubernetes[0].workers[1] | "talos_w2_ip=" + .ip' inventory.yaml)
echo "export $w2_ip" >> env.sh

echo "# Keys" >> env.sh
for key in $(yq '.hosts[] | .key' inventory.yaml); do
    echo "ssh-add $key" >> env.sh
done
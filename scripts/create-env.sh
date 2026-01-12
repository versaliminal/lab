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
kconf=$(yq '.kubernetes[0].kubeconfig' inventory.yaml)
echo "export KUBECONFIG=$(pwd)/$kconf" >> env.sh

echo "# Keys" >> env.sh
for key in $(yq '.hosts[] | .key' inventory.yaml); do
    echo "ssh-add $key" >> env.sh
done
#/bin/bash
echo -e "\nCreating private lab files archive..."
echo "--------------------------------"
TAR_FILE="lab-private.tar.zst"
echo -e "\nCompressing private lab files..."
echo "--------------------------------"
tar --zstd -vf ${TAR_FILE} -c config/ssh config/talos/ inventory.private.yaml
echo -e "\nEncrypting private lab files..."
echo "--------------------------------"
gpg --symmetric --cipher-algo AES256 ${TAR_FILE}
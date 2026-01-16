#!/bin/bash
echo -e "\nDecrypting private lab files..."
echo "--------------------------------"
gpg -o lab-private.tar.zst -d lab-private.tar.zst.gpg
echo -e "\nExtracting private lab files..."
echo "--------------------------------"
tar --zstd -xvf lab-private.tar.zst
echo -e "\nRunning inventory utility environment population..."
echo "--------------------------------"
python scripts/invutil.py --env
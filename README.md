# VERSALIMINAL LAB Overview

## High-Level Diagram
![diagram](docs/diagram.png)

## Inventory
Defined in the [inventory](inventory.yaml) file.

## Physical Setup
![lab](docs/lab.jpg)

# Working with the lab

## Inventory
- The primary inventory is defined in inventory.yaml
- Sensitive inventory data is defined in inventory.private.yaml (provided in private archive)

## Getting Started
1. Request Tailscale access
2. Request private archive access and download it to the root directory (you will also need the gpg passcode)
3. Setup a python virtual environment
    1. Run `python3 -m venv .venv`
    2. Run `source .venv/bin/activate`
    3. run `pip install -r scripts/requirements.txt`
4. run `scripts/init.sh` and enter the private archive password when prompted

At this point you should have a fully up-to-date environment for the lab to start with. To integrate the environment, do the following:

1. Copy the contents of config/os/hosts into your system hosts file
2. Source the shell environment: `source config/shell/env.sh`
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
3. Install [taskfile](https://taskfile.dev/docs/installation) and [python](https://www.python.org/downloads/)g if not already installed
4. Run `task init`

At this point you should have a fully up-to-date environment for the lab to start with. To integrate the environment, do the following:

1. Copy the contents of config/os/hosts into your system hosts file if desired
2. Source the shell environment: `source config/shell/env.sh` if desiredt
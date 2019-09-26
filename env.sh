#! /bin/sh
#
# env.sh
# Copyright (C) 2019 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.
#

export PROXMOX_USERNAME='ansible@pve'
export PROXMOX_URL='https://brie.opchee.se:8006'
echo -n 'Enter Proxmox password:'
read -s PROXMOX_PASSWORD
echo ''
export PROXMOX_PASSWORD
echo -n 'Enter Vault passphrase:'
read -s ANSIBLE_VAULT_PASSWORD
echo ''
export ANSIBLE_VAULT_PASSWORD
export ANSIBLE_VAULT_PASSWORD_FILE=./vault-env

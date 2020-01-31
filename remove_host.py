#! /usr/bin/env python3
import sys
import os
import json

import ansible_vault


def main():
    ctid = json.loads(sys.argv[1])

    vault = ansible_vault.Vault(os.environ.get('ANSIBLE_VAULT_PASSWORD'))
    with open('group_vars/all/vault.yml') as fd:
       vault_data = vault.load(fd.read())
    del vault_data['zfs_volumes'][int(ctid)]
    with open('group_vars/all/vault.yml', 'wb') as fd:
        vault.dump(vault_data, fd)


if __name__ == '__main__':
    # main()
    print('This script is obsolete', file=sys.stdout)
    os.exit(1)

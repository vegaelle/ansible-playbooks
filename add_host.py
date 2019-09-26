#! /usr/bin/env python3
import sys
import os
import json

import ansible_vault


def main():
    host_vars = json.loads(sys.argv[1])
    vlan = host_vars['vlan']
    ctid = host_vars['ctid']
    volume_data = {
        'pool': host_vars['zfs_pool'],
        'domains': host_vars['domains'].split(','),
        'vlan': vlan,
        'passphrase': host_vars['zfs_volume_passphrase'],
        'backup_passphrase': host_vars['backup_passphrase'],
        'containers': [
            {'ctid': int(ctid),
             'volumes': host_vars['zfs_volumes']}
        ]
    }

    vault = ansible_vault.Vault(os.environ.get('ANSIBLE_VAULT_PASSWORD'))
    with open('group_vars/all/vault.yml') as fd:
       vault_data = vault.load(fd.read())
    vault_data['zfs_volumes'][int(ctid)] = volume_data
    if 'http' in host_vars['groups']:
        vault_data['reverse_proxy'] = {'ctid': int(host_vars['ctid']),
                                       'ip': f'10.0.{vlan}.{ctid}'}
    if 'miab' in host_vars['groups']:
        vault_data['mailinabox'] = {'ctid': int(host_vars['ctid']),
                                    'ip': f'10.0.{vlan}.{ctid}'}
    with open('group_vars/all/vault.yml', 'wb') as fd:
        vault.dump(vault_data, fd)

    with open('backups.yml') as fd:
       vault_data = vault.load(fd.read())
    vault_data[int(ctid)] = host_vars['backup_passphrase']
    with open('backups.yml', 'wb') as fd:
        vault.dump(vault_data, fd)


if __name__ == '__main__':
    main()

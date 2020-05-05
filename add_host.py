#! /usr/bin/env python3
import sys
import os
import json
import argparse

import ansible_vault


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', action='store', dest='host')
    parser.add_argument('vars', type=json.loads)
    args = parser.parse_args()
    host = args.host
    host_vars = args.vars
    domain = host_vars['domain']
    volume_data = {
        'ctid': host_vars['ctid'],
        'pool': host_vars['zfs_pool'],
        'domain': domain,
        'passphrase': host_vars['zfs_volume_passphrase'],
        'backup_passphrase': host_vars['backup_passphrase'],
        'mail_account_passphrase': host_vars['mail_account_passphrase'],
        'vlan': host_vars['vlan'],
    }

    vault = ansible_vault.Vault(os.environ.get('ANSIBLE_VAULT_PASSWORD'))
    if not os.path.isdir(f'host_vars/{host}'):
        os.mkdir(f'host_vars/{host}')
    try:
        with open(f'host_vars/{host}/vault.yml') as fd:
            vault_data = vault.load(fd.read())
    except FileNotFoundError:
        vault_data = {}
    vault_data.update(volume_data)
    # if 'http' in host_vars['groups']:
    #     vault_data['reverse_proxy'] = {'ctid': int(host_vars['ctid']),
    #                                    'ip': f'10.0.{vlan}.{ctid}'}
    # if 'miab' in host_vars['groups']:
    #     vault_data['mailinabox'] = {'ctid': int(host_vars['ctid']),
    #                                 'ip': f'10.0.{vlan}.{ctid}'}
    with open(f'host_vars/{host}/vault.yml', 'wb') as fd:
        vault.dump(vault_data, fd)

    with open('backups.yml') as fd:
        vault_data = vault.load(fd.read())
        if vault_data is None:
            vault_data = {}
    vault_data[host] = host_vars['backup_passphrase']
    with open('backups.yml', 'wb') as fd:
        vault.dump(vault_data, fd)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List

MOUNT_DIR = Path('/mnt/binds')
FRONT_CTID = "{{ reverse_proxy_ctid }}"
MIAB_CTID = "{{ miab_ctid }}"
FW_CTID = "{{ firewall_ctid }}"

HOSTNAMES = {
{% for item in groups['containers'] %}
{% if hostvars[item].role not in ('firewall', 'http') %}
    '{{ hostvars[item].ctid }}': '{{ item }}',
{% endif %}
{% endfor %}
}


def get_running_containers() -> List[str]:
    res = subprocess.run(
        'ps aux | grep lxc-start | grep -v grep | awk \'{ print $14 }\'',
        shell=True, capture_output=True, encoding='utf-8')
    return sorted(res.stdout.split())


def mount(ctid: str, src:str='/srv/public',
          dest:str='/var/www/vhosts/{hostname}', verbose:bool=False):
    if verbose:
        dest_with_hostname = dest.format(hostname=HOSTNAMES[ctid])
        print(f'Mounting {ctid}:{src} to {dest_with_hostname}')
    src_id = src[1:].replace('/', '-')
    src = (Path('/') / src.format(hostname=HOSTNAMES[ctid])).resolve()
    src_path = Path('/') / 'rpool' / 'data' / f'encrypted-{ctid}' / \
        f'subvol-{ctid}-disk-0' / src.relative_to('/')
    dest = (Path('/') / dest.format(hostname=HOSTNAMES[ctid])).resolve()
    dest_path = Path('/') / 'rpool' / 'data' / f'encrypted-{FRONT_CTID}' / \
        f'subvol-{FRONT_CTID}-disk-0' / dest.relative_to('/')
    if not dest_path.exists():
        dest_path.mkdir()
    if len(list(dest_path.iterdir())):
        raise OSError(f'Path {dest_path} not empty')
    tmp_mountpoint = '{ctid}-{path}'.format(ctid=ctid, path=src_id)
    mount_point = MOUNT_DIR / tmp_mountpoint
    if not mount_point.exists():
        mount_point.mkdir()
    res = subprocess.run(['mount', '-o', 'bind,ro', src_path,  mount_point],
                         capture_output=True)
    if res.returncode == 0:
        res = subprocess.run(['mount', '-o', 'bind,ro', mount_point, dest_path],
                             capture_output=True)
        if res.returncode != 0:
            raise OSError(f'Error while mounting {mount_point} to {dest_path}: {res.stderr}')
    else:
        raise OSError(f'Error while mounting {src_path} to {mount_point}: {res.stderr}')


def umount(ctid: str, src:str='/srv/public',
           dest:str='/var/www/vhosts2/{hostname}', verbose:bool=False):
    if verbose:
        dest_with_hostname = dest.format(hostname=HOSTNAMES[ctid])
        print(f'Unmounting {ctid}:{src} from {dest_with_hostname}')
    src_id = src[1:].replace('/', '-')
    src = (Path('/') / src.format(hostname=HOSTNAMES[ctid])).resolve()
    src_path = Path('/') / 'rpool' / 'data' / f'encrypted-{ctid}' / \
        f'subvol-{ctid}-disk-0' / src.relative_to('/')
    dest = (Path('/') / dest.format(hostname=HOSTNAMES[ctid])).resolve()
    dest_path = Path('/') / 'rpool' / 'data' / f'encrypted-{FRONT_CTID}' / \
        f'subvol-{FRONT_CTID}-disk-0' / dest.relative_to('/')
    if not dest_path.exists():
        raise OSError(f'Path {dest_path} does not exist')
    tmp_mountpoint = '{ctid}-{path}'.format(ctid=ctid, path=src_id)
    mount_point = MOUNT_DIR / tmp_mountpoint
    if not mount_point.exists():
        raise OSError(f'Mount point {mount_point} does not exist')
    res = subprocess.run(['umount', dest_path],
                         capture_output=True)
    res2 = subprocess.run(['umount', mount_point],
                          capture_output=True)
    if res.returncode != 0:
        raise OSError(f'Error while unmounting {dest}: {res.stderr}')
    if res2.returncode != 0:
        raise OSError(f'Error while unmounting {mount_point}: {res.stderr}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('ctid', type=str)
    parser.add_argument('phase',
                        choices=('pre-start',
                                 'post-start',
                                 'pre-stop',
                                 'post-stop'))
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()


    if args.ctid != FW_CTID:  # no dir to mount
        # get running containers
        ctid = args.ctid
        running = get_running_containers()
        if args.phase == 'post-start':
            if ctid == FRONT_CTID:
                # mounting all started containers
                for ct in running:
                    if ct not in (FW_CTID, FRONT_CTID):
                        mount(ct, verbose=args.verbose)
                        if ct == MIAB_CTID:
                            mount(ct, src='/home/user-data/ssl',
                                  dest='/home/user-data/ssl',
                                  verbose=args.verbose)
            else:
                # mounting public dir
                mount(ctid, verbose=args.verbose)
                if ctid == MIAB_CTID:
                    # mounting ssl dir
                    mount(ctid, src='/home/user-data/ssl',
                          dest='/home/user-data/ssl',
                          verbose=args.verbose)
        elif args.phase == 'pre-stop':
            if ctid == FRONT_CTID:
                # unmounting all containers
                for ct in running:
                    try:
                        if ct not in (FW_CTID, FRONT_CTID):
                            umount(ct, verbose=args.verbose)
                            if ct == MIAB_CTID:
                                # unmounting ssl dir
                                umount(ct, src='/home/user-data/ssl',
                                       dest='/home/user-data/ssl',
                                       verbose=args.verbose)
                    except OSError as e:
                        print(f'Got error: {e}. Passing...')
            else:
                # unmounting public dir
                umount(ctid, verbose=args.verbose)
                if ctid == MIAB_CTID:
                    # unmounting ssl dir
                    umount(ctid, src='/home/user-data/ssl',
                           dest='/home/user-data/ssl',
                           verbose=args.verbose)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f'{type(e).__name__}: {e}', file=sys.stderr)
        sys.exit(1)


import os
from subprocess import PIPE, Popen, run

import requests

from versions import Version, get_python_last_versions
from versions.exeptions import VersionStringError

from .utils import send_error_report

REQUIRED_SPACE = 3000  # Required space for building packages, MBytes


def check_free_space():
    out = run('df --output=avail --block-size=1048576 /tmp'.split(),
              stdout=PIPE, stderr=PIPE, encoding='utf-8')
    free_space = int(out.stdout.splitlines()[1])
    if free_space < REQUIRED_SPACE:
        send_error_report(
            f'To build packages, you need at least {REQUIRED_SPACE} MBytes '
            'of free space in the file system of the "/tmp" directory!'
        )


def check_version_str(version_str: str) -> Version:
    try:
        version = Version.from_version_str(version_str)
    except VersionStringError as error:
        send_error_report(f'{error}')
    if version < Version(3, 2, 1):
        send_error_report('Versions earlier than 3.2.1 are not supported!')
    last_versions = get_python_last_versions()
    last_version = last_versions['last_version']
    if version > last_version:
        send_error_report(f'Last available version is {last_version}')
    major_middle_version = version.get_major_middle_version()
    if version > last_versions[major_middle_version]:
        send_error_report(f'Last version of Python {major_middle_version} '
                          f'is {last_versions[major_middle_version]}')
    head = requests.head('https://www.python.org/ftp/python/'
                         f'{version}/Python-{version}.tar.xz')
    if not head.ok:
        send_error_report(f'Source package <Python-{version}.tar.xz> '
                          f'not found on python.org!')
    return version


def check_hashman_group():
    groups = Popen(['groups'], stdout=PIPE, encoding='utf-8')
    out = run('grep hashman'.split(),
              stdin=groups.stdout, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    if out.returncode:
        send_error_report('Before starting the build, run the command: '
                          '`hasher-useradd $USER` and log in again.')


def check_distributor():
    lsb_release = Popen('lsb_release --id --short'.split(),
                        stdout=PIPE, encoding='utf-8')
    out = run('grep -e ^ALT$'.split(),
              stdin=lsb_release.stdout, stdout=PIPE, stderr=PIPE,
              encoding='utf-8')
    build_script = os.getenv('PYTHON_MANAGER_BUILD_SCRIPT')
    if not build_script:
        if out.returncode:
            send_error_report('This is not ALT Linux. '
                              'You can write your own build script for '
                              'your linux distribution. '
                              'See section "configuration" '
                              'in `python-manager --help`.')
        check_hashman_group()
        check_free_space()

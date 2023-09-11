import os
from subprocess import run

from versions import (Version, get_python_exec_last_versions,
                      get_python_exec_outdated_versions)

from .utils import get_python_exec_files

ALT_BUILD_SCRIPT = (os.path.dirname(__file__)
                    + '/../altlinux/python3-build.altlinux.sh')


def show_python_exec_versions():
    python_exec_files = get_python_exec_files()
    python_versions = get_python_exec_last_versions(python_exec_files)
    python_statuses = dict()
    for python_name, versions in python_versions.items():
        if versions['current_version'] == versions['last_version']:
            python_statuses[python_name] = 'ACTUAL\t\t'
        elif versions['current_version'] > versions['last_version']:
            python_statuses[python_name] = 'WONDER\t\t'
        else:
            python_statuses[python_name] = 'OUTDATED\t'
        python_statuses[python_name] += (
            f'[current_version == {versions["current_version"]}, '
            f'last_version == {versions["last_version"]}]'
        )
    for python_name, status in python_statuses.items():
        print(f'{python_name}\t{status}')


def build(version: Version, install=False) -> str:
    print(ALT_BUILD_SCRIPT)
    packages_dir = os.getenv('PYTHON_MANAGER_PACKAGES_DIR')
    build_script = os.getenv('PYTHON_MANAGER_BUILD_SCRIPT')
    if not packages_dir:
        packages_dir = os.getcwd()
    if not build_script:
        build_script = ALT_BUILD_SCRIPT
    package_name = f'python{version.major}{version.middle}'
    out = run(
        f'{build_script} {package_name} {version} '
        f'{packages_dir} {install}'.split(), encoding='utf-8'
    )
    build_status = f'Python {version}\t:\t'
    if out.returncode:
        return build_status + (f'ERROR: {build_script} '
                               f'return code {out.returncode}')
    return build_status + f'COMPILED (package saved in {packages_dir})'


def build_outdated(install=False) -> list:
    outdated = get_python_exec_outdated_versions(get_python_exec_files())
    build_statuses = list()
    for _, versions in outdated.items():
        build_statuses.append(build(versions.get('last_version'), install))
    return build_statuses

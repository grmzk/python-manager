#!/usr/bin/python3

import argparse
import os
import sys
import textwrap

from dotenv import load_dotenv

from actions import build, build_outdated, show_python_exec_versions
from checkers import check_distributor, check_version_str

CONFIG_PATH = os.getenv('HOME') + '/.config/python-manager.conf'

load_dotenv(dotenv_path=CONFIG_PATH)


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python-manager',
        description='Manager for installing or updating different versions '
                    'of the python interpreters on the same computer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
configuration:
  By default, the assembled package is saved in the current directory.
  To change this, you can define the environment variable
  <PYTHON_MANAGER_PACKAGES_DIR> in the configuration file
  "$HOME/.config/python-manager.conf".
  Example: PYTHON_MANAGER_PACKAGES_DIR="${HOME}/python_packages".

  By default, if your distribution is ALT Linux, `python-manager` uses
  its own bash script to create packages.
  If you are using another distribution, you can use your own script,
  to do this, define the environment variable <PYTHON_MANAGER_BUILD_SCRIPT>
  in "<$HOME/.config/python-manager.conf>".
  Example: PYTHON_MANAGER_BUILD_SCRIPT="path_to_your_build_script.sh".

  For writing own build script consider that `package-manager` pass to build
  script 4 positional arguments. Example for Python 3.10.13:
    $1 - "python310" (package name)
    $2 - "3.10.13" (version)
    $3 - "/path/to/packages/dir" (packages directory)
    $4 - "False" (install package after building? "True" or "False")
  Important: use `make altinstall` instead of `make install` when building
  python from source code!
               ''')
    )
    group_build = parser.add_mutually_exclusive_group()
    group_build.add_argument(
        '--build', type=str, metavar='<version>',
        help='Building a python interpreter from source code. '
             'Example: python-manager --build 3.10.13'
    )
    group_build.add_argument(
        '--build-outdated', action='store_true',
        help='Building all outdated python interpreters from source code.'
    )
    parser.add_argument(
        '--install', action='store_true',
        help='Install the package after the build. '
             'Used only together with '
             '`--build <version>` or `--build-outdated`. '
             'Example: python-manager --build 3.10.13 --install'
    )
    parser.add_argument(
        '--python-versions', action='store_true',
        help='Show versions of installed python interpreters '
             'and versions on python.org'
    )
    return parser


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args(sys.argv[1:])
    if args.build:
        check_distributor()
        version = check_version_str(args.build)
        build_status = build(version, args.install)
        print(build_status)
    elif args.build_outdated:
        check_distributor()
        build_statuses = build_outdated(args.install)
        for build_status in build_statuses:
            print(build_status)
    elif args.python_versions:
        show_python_exec_versions()
    else:
        parser.print_help()

# Python Manager

## Description

Manager for installing or updating different versions 
of the python interpreters on the same computer

## Requires

- [Python 3](https://www.python.org/)
- [Requests](https://github.com/psf/requests)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [GNU Bash](https://www.gnu.org/software/bash/)

## Installation

#### For ALT Linux

Pre-built rpm-packages available on 
[releases](https://github.com/grmzk/python-manager/releases) page.

#### For other Linux Distributions

Download the sources
```
git clone https://github.com/grmzk/python-manager.git
```
Go to sources directory
```
cd python-manager
```
Create symlink
```
sudo ln -sv $PWD/main.py /usr/local/bin/python-manager
```

## Usage

```
usage: python-manager [-h] [--build <version> | --build-outdated] [--install] [--python-versions]

Manager for installing or updating different versions of the python interpreters on the same computer

optional arguments:
  -h, --help         show this help message and exit
  --build <version>  Building a python interpreter from source code. Example: python-manager --build 3.10.13
  --build-outdated   Building all outdated python interpreters from source code.
  --install          Install the package after the build. Used only together with `--build <version>` or `--build-outdated`. Example: python-manager --build 3.10.13 --install
  --python-versions  Show versions of installed python interpreters and versions on python.org

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
  in "$HOME/.config/python-manager.conf".
  Example: PYTHON_MANAGER_BUILD_SCRIPT="path_to_your_build_script.sh".

  For writing own build script consider that `package-manager` pass to build
  script 4 positional arguments. Example for Python 3.10.13:
    $1 - "python310" (package name)
    $2 - "3.10.13" (version)
    $3 - "/path/to/packages/dir" (packages directory)
    $4 - "False" (install package after building? "True" or "False")
  Important: use `make altinstall` instead of `make install` when building
  python from source code!
```

## Author
- Igor Muzyka [mailto:muzyka-iv@yandex.ru]

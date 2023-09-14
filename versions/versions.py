import re
from html.parser import HTMLParser
from subprocess import PIPE, run

import requests

from .exeptions import (PythonParserError, RunPythonVError, VersionInitError,
                        VersionStringError)


class Version:
    def __init__(self, major: int, middle: int, minor: int):
        for arg in [major, middle, minor]:
            if arg.__class__ != int:
                raise VersionInitError(
                    "Version's initialized arguments must be int"
                )
        self.major = major
        self. middle = middle
        self.minor = minor

    @classmethod
    def from_version_str(cls, version_str: str):
        pattern = re.compile(r'^3\.\d\d?\.\d\d?$')
        if not pattern.match(version_str):
            raise VersionStringError(
                'Argument <version_str> must match '
                'pattern r"^3\\.\\d\\d?\\.\\d\\d?$". '
                'Example: 3.7.17'
            )
        return cls(*map(int, version_str.split('.')))

    def get_major_middle_version(self) -> str:
        return f'{self.major}.{self.middle}'

    def __gt__(self, other):
        return ((self.major, self.middle, self.minor)
                > (other.major, other.middle, other.minor))

    def __ge__(self, other):
        return ((self.major, self.middle, self.minor)
                >= (other.major, other.middle, other.minor))

    def __lt__(self, other):
        return ((self.major, self.middle, self.minor)
                < (other.major, other.middle, other.minor))

    def __le__(self, other):
        return ((self.major, self.middle, self.minor)
                <= (other.major, other.middle, other.minor))

    def __eq__(self, other):
        return ((self.major, self.middle, self.minor)
                == (other.major, other.middle, other.minor))

    def __str__(self):
        return f'{self.major}.{self.middle}.{self.minor}'


class PythonParser(HTMLParser):
    last_versions = dict()
    last_version = Version(0, 0, 0)

    def handle_data(self, data):
        pattern = re.compile(r'^3\.\d\d?\.\d\d?/$')
        if pattern.match(data):
            version = Version.from_version_str(data[:-1])
            major_middle_version = version.get_major_middle_version()
            last_version = self.last_versions.get(major_middle_version)
            if not last_version or last_version < version:
                self.last_versions[major_middle_version] = version
                if self.last_version < version:
                    self.last_version = version

    def get_last_version(self, major_middle_version: str) -> Version:
        pattern = re.compile(r'^3\.\d\d?$')
        if not pattern.match(major_middle_version):
            raise PythonParserError('Argument <major_middle_version> '
                                    'must match pattern '
                                    'r"^3\\.\\d\\d?$"')
        last_version = self.last_versions.get(major_middle_version)
        if not last_version:
            raise PythonParserError('Argument <major_middle_version> '
                                    'not exists in last_versions')
        return self.last_versions[major_middle_version]

    def get_last_versions(self):
        last_versions = self.last_versions.copy()
        last_version = self.last_version
        head = requests.head('https://www.python.org/ftp/python/'
                             f'{last_version}/Python-{last_version}.tar.xz')
        if not head.ok:
            del last_versions[last_version.get_major_middle_version()]
            last_version.middle -= 1
            last_version = last_versions.get(
                last_version.get_major_middle_version()
            )
        last_versions['last_version'] = last_version
        return last_versions


def get_python_parser():
    request = requests.get('https://www.python.org/ftp/python/')
    parser = PythonParser()
    parser.feed(request.text)
    return parser


def get_python_last_versions():
    parser = get_python_parser()
    return parser.get_last_versions()


def get_python_exec_last_versions(python_exec_names: list):
    python_versions = dict()
    for python_name in python_exec_names:
        current_version_out = run(f'{python_name} -V'.split(),
                                  stdout=PIPE, stderr=PIPE, encoding='utf-8')
        current_version: Version
        if current_version_out.returncode:
            raise RunPythonVError(current_version_out.stderr)
        current_version = Version.from_version_str(
            current_version_out.stdout.split(' ')[1][:-1]
        )
        versions = {
            'current_version': current_version,
            'last_version': Version(0, 0, 0)
        }
        python_versions[python_name] = versions
    parser = get_python_parser()
    for python_name in python_exec_names:
        current_version = python_versions[python_name]['current_version']
        last_version = parser.get_last_version(
            current_version.get_major_middle_version()
        )
        python_versions[python_name]['last_version'] = last_version
    return python_versions


def get_python_exec_outdated_versions(python_exec_names: list):
    python_versions = get_python_exec_last_versions(python_exec_names)
    outdated = dict()
    for python_name, versions in python_versions.items():
        if versions['current_version'] < versions['last_version']:
            outdated[python_name] = versions
    return outdated

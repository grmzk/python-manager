from subprocess import PIPE, run


def get_python_exec_files() -> list:
    find_python_out = run(
        r'find /usr/local/bin -regex ^/usr.*/bin/python3\.[0-9]*$'.split(),
        stdout=PIPE, stderr=PIPE, encoding='utf-8'
    )
    python_exec_files = find_python_out.stdout.splitlines()
    python_exec_files.sort(key=lambda file: int(file.split('python3.')[1]))
    return python_exec_files

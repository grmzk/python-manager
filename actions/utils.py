from subprocess import PIPE, run


def get_python_exec_files() -> list:
    find_python_out = run(
        r'find /usr/local/bin -regex ^/usr.*/bin/python3\.[0-9]*$'.split(),
        stdout=PIPE, stderr=PIPE, encoding='utf-8'
    )
    python_exec_files = find_python_out.stdout.splitlines()
    python_exec_files.sort(key=lambda file: int(file.split('python3.')[1]))
    find_system_python_out = run(
        r'find /usr/bin -regex ^/usr/bin/python3$'.split(),
        stdout=PIPE, stderr=PIPE, encoding='utf-8'
    )
    if find_system_python_out.stdout:
        python_exec_files = ([find_system_python_out.stdout.splitlines()[0]]
                             + python_exec_files)
    return python_exec_files

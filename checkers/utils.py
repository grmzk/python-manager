from sys import stderr


def send_error_report(error: str):
    stderr.write(f'ERROR: {error}\n')
    exit(-1)

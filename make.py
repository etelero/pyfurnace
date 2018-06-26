import os
import subprocess
import fire

testdir = './tests/'
tests = [testdir + i for i in os.listdir(testdir) if i.endswith('.py')]

modify = {
    'dev': '/dev/ttyUSB0',
    'files': tests,
}

# Filesystem test
ampy_ls = 'ampy -p {mod[dev]} ls'
ampy_put = 'ampy -p {mod[dev]} put {file}'
ampy_put_all = 'ampy -p {mod[dev]} put {mod[files]}'
ampy_rm = 'ampy -p {mod[dev]} rm {mod[files]}'
ampy_run = 'ampy -p {mod[dev]} run {f}'


def run_ampy_cmd(command: str, **kwargs) -> bytes:
    cmd = command.format(**kwargs, mod=modify)
    res = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    return res.stdout


def run_tests():
    for i in tests:
        print(run_ampy_cmd(ampy_run, f=i).decode('utf-8'))


if __name__ == '__main__':
    fire.Fire({
        'test': run_tests,
    })

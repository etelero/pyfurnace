import os
import subprocess
import fire

testdir = './tests/'
tests = [testdir + i for i in os.listdir(testdir) if i.endswith('.py')]

modify = {
    'dev': '/dev/ttyUSB0',
    'files': tests,
}
path = './core/'
files = [
    'boot.py',
    'main.py',
    'lcd_api.py',
    'i2c_lcd.py',
    'pcf8574.py',
    'keypad.py',
]

# Filesystem test
ampy_ls = 'ampy -p {mod[dev]} ls'
ampy_put = 'ampy -p {mod[dev]} put {f}'
ampy_put_all = 'ampy -p {mod[dev]} put {mod[files]}'
ampy_rm = 'ampy -p {mod[dev]} rm {f}'
ampy_run = 'ampy -p {mod[dev]} run {f}'


def run_ampy_cmd(command: str, **kwargs) -> str:
    cmd = command.format(**kwargs, mod=modify)
    res = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    return res.stdout.decode('utf-8')


def upload():
    for filen in files:
        if filen in run_ampy_cmd(ampy_ls).split('\n'):
            run_ampy_cmd(ampy_rm, f=filen)
        run_ampy_cmd(ampy_put, f=(path + filen))


def run_tests():
    for i in tests:
        print(run_ampy_cmd(ampy_run, f=i))


if __name__ == '__main__':
    fire.Fire({
        'upload': upload,
        'test': run_tests,
    })

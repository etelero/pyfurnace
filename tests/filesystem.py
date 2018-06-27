import os

err, ok = '[ERROR] ', '[OK] '
errno = {
    'interrupt': 1
}

fn = 'filesystem_test'
testf_lines = [
    'Aname,123,123',
    'Bname,456,456',
    'Dname,789,789',
]


def write():
    f = open(fn, 'w')
    if not f:
        print(err + 'Could not open file for writing')
        return(errno['interrupt'])

    for i in testf_lines:
        f.write(i + '\n')
    f.close()

    f = open(fn, 'r')
    for i in testf_lines:
        line = f.readline()[:-1]
        if i != line:
            print((err + 'Line missmatch: "{}" must be "{}"').format(line, i))
            return(errno['interrupt'])
    print(ok + 'File written succesfully')
    f.close()


def remove():
    os.remove(fn)
    try:
        found = 1
        f = open(fn, 'r')
    except OSError:
        found = 0
    finally:
        if found:
            print(err + 'File deletion failed')
            f.close()
        else:
            print(ok + 'File removed succesfully')


defs = [
    write,
    remove,
]


res = 0
for i in defs:
    if res != 1:  # iterrupt
        res = i()
    else:
        print('Interrupting test execution')

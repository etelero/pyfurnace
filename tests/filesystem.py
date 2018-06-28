import os
from boot import Storrage

err, ok = '[ERROR] ', '[OK] '

fn = 'filesystem_test'
testf_lines = [
    'Aname,123,123',
    'Bname,456,456',
    'Cname1,456,456',
    'Cname1_1,456,456',
    'Cname200,456,457',
    'Dname,789,789',
]
searches = {
    'Cname,456,456': 3,
    'Cname111,456,456': 4,
    'Cname2000,456,457': 6,
    'Cname2_1,456,456': 6,
}

S = Storrage(fn)


def write() -> int:
    f = open(fn, 'w')
    if not f:
        print(err + 'Could not open file for writing')
        return 0

    for i in testf_lines:
        f.write(i + '\n')
    f.close()

    f = open(fn, 'r')
    for i in testf_lines:
        line = f.readline()[:-1]
        if i != line:
            print((err + 'Line missmatch: "{}" must be "{}"').format(line, i))
            return 0
    print(ok + 'File written succesfully')
    f.close()
    return 1


def search_alpha_pos() -> int:
    failed = 0
    for line in searches:
        pos = S.__search_alpha_pos(line)
        if pos != searches[line]:
            print(
                err
                + 'Line pos search result did not match assumed pos\n'
                'line \"{}\" should be at pos {} not {}'.format(
                    line, searches[line], pos
                )
            )
            failed += 1
    if not failed:
        print(ok + 'Alpha search succesful')
        return 1
    else:
        return 0


def remove() -> int:
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
    return 1


defs = [
    write,
    search_alpha_pos,
    remove,
]

if S.programs in os.listdir():
    os.remove(S.programs)

res = 1
for i in defs:
    if res:  # iterrupt check
        res = i()
    else:
        print('Interrupting test execution')

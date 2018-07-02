import os
from main import Storrage

err, ok = '[ERROR] ', '[OK] '

verbose = False
# verbose = True

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
    'Cname,456,456': 2,
    'Cname111,456,456': 3,
    'Cname2000,456,457': 5,
    'Cname2_1,456,456': 5,
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
        pos = S.__search_alpha_pos(line, S.programs)
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


def remove(filename=fn, active=1) -> int:
    if active:
        os.remove(filename)
    try:
        found = 1
        f = open(filename, 'r')
    except OSError:
        found = 0
    finally:
        if found:
            print(err + 'File deletion failed')
            f.close()
            return 0
        else:
            print(ok + 'File removed succesfully')
    return 1


def insert_delete_remove() -> int:
    progs = {
        '1name,324,345,342': 0,
        'Cname,456,456': 2,
        'Zname,324,345,342': 6,
    }
    failed = 0
    for prog in progs:
        pos = S.insert_prog(prog)
        if pos != progs[prog]:
            print(
                err + "Insertion at wrong pos."
                "Pos == {} expected {}".format(pos, progs[prog])
            )
            failed += 1
        if remove(fn + '_', 0):
            print(ok + "Directory is clean")
        else:
            print(err + "Directory is dirty")
            return 0

        if verbose:
            print('\nAfter insert:')
            f = open(fn, 'r')
            for l in f:
                print(l.strip('\n'))
            f.close()

        S.delete_prog(prog)
        if verbose:
            print('\nAfter del:')
            f = open(fn, 'r')
            for l in f:
                print(l.strip('\n'))
            f.close()

        f = open(fn, 'r')
        del_test_iter = 0
        for fline in f:
            try:
                if str(fline).strip('\n') != testf_lines[del_test_iter]:
                    print(err + "Deletion failed")
                    failed += 1
                    break
            except IndexError:
                print(err + 'File length missmatch')
                failed += 1
                break
            del_test_iter += 1

        f.close()

    if not failed:
        print(ok + "Inserted and deleted progs succesfully")


defs = [
    write,
    search_alpha_pos,
    insert_delete_remove,
]

res = 1
for i in defs:
    if res:  # iterrupt check
        res = i()
    else:
        print('Interrupting test execution')

if fn in os.listdir():
    os.remove(S.programs)

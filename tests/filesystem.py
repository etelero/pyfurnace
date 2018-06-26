import os

err, ok = '[ERROR] ', '[OK] '

fn = 'filesystem_test'
f = open(fn, 'w')
if not f:
    print('Could not open file for writing')

testf_lines = [
    'Aname,123,123',
    'Bname,456,456',
    'Dname,789,789',
]

for i in testf_lines:
    f.write(i + '\n')
f.close()

interrupt = 0
f = open(fn, 'r')
for i in testf_lines:
    line = f.readline()[:-1]
    if i != line:
        interrupt = 1
        print((err + 'Line missmatch: "{}" must be "{}"').format(line, i))
        break

if not interrupt:
    print(ok + 'File written succesfully')
    f.close()

    os.remove(fn)
    try:
        found = 1
        f = open(fn, 'r')
    except OSError:
        found = 0
    finally:
        if found:
            print(err + 'File deletion failed')
        else:
            print(ok + 'File removed succesfully')

# memory consumption based on:
# https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
import dnf
import os
import sys
_proc_status = '/proc/%d/status' % os.getpid()
last_mem = 0

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return int(_VmB('VmRSS:') - since)


# -- reproduce OOM bug ---
def get_base():
    global last_mem
    base = dnf.Base()
    base.conf.assumeyes = True
    base.read_all_repos()
    base.fill_sack(load_system_repo='auto')
    base.close()
    new_mem = _VmB('VmRSS:')
    str_format = '{:.0f} mb memory, delta: {:.0f} mb'
    delta = new_mem - last_mem
    print(str_format.format(new_mem / 1024 / 1024, delta / 1024 / 1024))
    last_mem = new_mem
    sys.stdout.flush()

print('starting endless loop')
sys.stdout.flush()
while True:
    get_base()

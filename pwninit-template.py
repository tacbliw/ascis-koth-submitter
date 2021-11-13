#!/usr/bin/env python3
from pwn import *
import argparse
import os
import requests

# alias "pwninit"="pwninit --template-path=~/tools/ctf/scripts/pwn/pwninit/base.py"

{bindings}
REMOTE_SERVER = ""
REMOTE_PORT = 1337

GDB_SCRIPT = """
handle SIGALRM ignore
"""

context.binary = exe
p = None

def get_process():
    if args.REMOTE:
        p = remote(REMOTE_SERVER, REMOTE_PORT)
    else:
        p = process({proc_args})
        os.system('pmap %d' % p.pid)
    return p

def attach_gdb(p):
    if not args.REMOTE:
        gdb.attach(p, gdbscript=GDB_SCRIPT)

def my_cyclic(n):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ''
    for i in range(n):
        result += alphabet[i // context.bytes]
    return result.encode()

def ss(s, v):
    success('%s @ 0x%x' % (s, v))

def ii(s, v):
    info('%s @ 0x%x' % (s, v))

def submit(flag_contain):
    requests.post('http://192.168.1.7:8000/', data=flag_contain, timeout=5)

def prod(exec_funcs):
    sleep_time = 60
    args.REMOTE = True
    while True:
        cnt = 0
        for f in exec_funcs:
            cnt += 1
            success('Running exploit ' + str(cnt))
            f()
        info('Sleeping for %ds ...' % sleep_time)
        sleep(sleep_time)

def exp1():
    pass

p = get_process()
attach_gdb(p)



p.interactive()

# prod([exp1])
from flask import Flask, request
import requests
import re
import urllib
import threading
import time
import urllib3

import outputhandler as o
import workerhandler as qt

url = 'https://ascis.1337.edu.vn'
urllib3.disable_warnings()

def submit(chall: str, flag: str) -> bool:
    flag = re.findall(r'(ASCIS{.*?})', flag)
    if flag:
        flag = flag[0]
    else:
        o.fail('No flag')
        return False
    try:
        headers = {
            # 'CSRF-Token': nonce
        }
        data = {
            'team': 'Pawsitive',
            'daemon': chall,
            'action': 'submit-flag',
            'flag': flag
        }
        _cookies = {
            'x_polaris_sd':'O7nWv6MdbYuxK68ZeEa7FYYM94b3ilTT|dT26FZ3JvK1yepW9f6y6EbF0la5SwQ4B7BgGOJxVAyRId4iW64JFWdEYHkbjjcen4jtVBYeKiHDFIB4A9B5TfuWPTsBAWDQDjkaGF!!',
            'x_polaris_sid':'B5dcBQwBCMXrFjWaV6klMBONZhkvF26CtksF',
            'session':'77ba6cbc-4871-43d4-b1f0-515733234f8b.eX8SyP4Poufyb7o5cIor3noKFUw'
        }
        r = requests.post(f"{url}/submitflag_API", cookies=_cookies, data=data,
                        headers=headers, verify=False)#, proxies={'https': 'https://localhost:8001'})
        if r.status_code == 200:
            # data = r.json()
            if "owner already updated !!!" in r.text or 'incorrect flag !!!' in r.text:
                return False
            elif 'rate limit exceeded !!!' in r.text:
                o.warning('rate limit exceeded !!!\n')
                return False
            return True
    except Exception as e:
        print(e)
        return False

# setup summiter threads
queue = qt.WildcatQueue()
thread_stop = False
threads = []
print_lock = threading.Lock()
ids = ['Crypto01', 'Pwn01', 'Pwn02', 'Pwn03', 'Web01', 'Web02'] # chall ids, should be gathered at the start

def runner(ident):
    while not thread_stop:
        data = queue.get(0)
        if data != 'Empty':
            flag = data[0]
            chall_id = data[1]
            if chall_id:
                result = submit(chall_id, flag)
                if result:
                    with print_lock:
                        o.success(flag)
                else:
                    with print_lock:
                        o.fail(flag)
            else:
                for i in ids: # try to submit the same flag on all the chall ids
                    result = submit(i, flag)
                    if result:
                        with print_lock:
                            o.success(flag)
                        break
                else:
                    with print_lock:
                        o.fail(flag)
            queue.task_done()
        else:
            time.sleep(2)
try:
    for ident in range(10): # 10 threads should be enough
        t = threading.Thread(target=runner, args=[ident])
        t.daemon = True
        threads.append(t)
    
    for t in threads:
        t.start()
except Exception as e:
    print(e)
    thread_stop = True
    exit(1)

# start app api
app = Flask('Submitter')

@app.route('/', methods=['GET', 'POST'])
def a():
    all_text = ' '.join([request.get_data().decode('ascii'), request.query_string.decode('ascii')])
    all_text = urllib.parse.unquote(all_text)
    flag = re.findall(r'{.*?}', all_text)
    if flag:
        chall_id = request.args.get('c')
        print(chall_id, end=': ')
        for f in flag:
            queue.put(('ASCIS' + f, chall_id))
        return 'Done'
    print('No flag')
    return 'No flag'

app.run('0.0.0.0', 8000)
thread_stop = True
o.info('Terminating all threads...')
qt.terminate_all_threads(threads)
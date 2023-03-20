import time
import datetime
import os
import psutil

import notification

def check(conf):
    print('[{}] Start checking processes.'.format(datetime.datetime.now()))

    proc_conf=conf['proc']

    pids=proc_conf['mon']

    if len(pids)>=1:
        print("There are processes to check.")
        not_running=[]
        for pid in pids:
            if not psutil.pid_exists(pid):
                not_running.append(pid)
        
        if len(not_running)>=1:        
            msg=dict()
            msg['title']="Process Ended"
            msg['content']=','.join([str(e) for e in not_running])
            msg['content']+=' is/are not running now.'
            notification.notify(conf,msg)



import yaml
import time
import datetime

import check_gpu
import check_proc
import notification

def seconds(hour,minutes,secs):
    return hour*3600+minutes*60+secs

def at_sleep_time(begin_hour,end_hour)->bool:
    nowtime= datetime.datetime.now()
    return nowtime.hour>begin_hour and nowtime.hour<end_hour

with open('conf.yaml', 'r') as f:
    conf = yaml.safe_load(f)
    print(conf)

while True:
    print("Running checks")

    with open('conf.yaml', 'r') as f:
        conf = yaml.safe_load(f)
        
    conf=conf['config']

    check_proc.check(conf)
    check_gpu.check(conf)

    if at_sleep_time(conf['sleep']['begin'],conf['sleep']['end']):
        time.sleep(seconds(2,0,0))
    else:
        time.sleep(seconds(0,40,0))


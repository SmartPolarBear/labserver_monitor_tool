import yaml
import time
import datetime

import check_gpu
import check_proc
import notification

from utils import seconds,at_sleep_time

with open('conf.yaml', 'r') as f:
    conf = yaml.safe_load(f)
    print(conf)

while True:
    print("Running checks")

    with open('conf.yaml', 'r') as f:
        conf = yaml.safe_load(f)
        
    conf=conf['config']

    try:
        check_proc.check(conf)
    except:
        print('Fail to check proc.')

    try:
        check_gpu.check(conf)
    except:
        print('Fail to check GPU')

    if at_sleep_time(conf['sleep']['begin'],conf['sleep']['end']):
        time.sleep(seconds(2,0,0))
    else:
        time.sleep(seconds(0,40,0))


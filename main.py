import yaml
import time

import check_gpu
import check_proc
import notification

with open('conf.yaml', 'r') as f:
    conf = yaml.safe_load(f)

print(conf)

conf=conf['config']

while True:

    check_proc.check(conf)
    check_gpu.check(conf)

    time.sleep(5)


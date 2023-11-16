import yaml
import time
import datetime

import check_gpu
import check_proc
import check_fs
import notification

from utils import seconds, at_sleep_time

with open("conf.yaml", "r") as f:
    conf = yaml.safe_load(f)
    print(conf)

counter = 0
while True:
    counter += 1
    if counter > 100:
        counter = 0

    print("Running checks")

    with open("conf.yaml", "r") as f:
        conf = yaml.safe_load(f)

    conf = conf["config"]

    try:
        check_gpu.check(conf)
    except Exception as e:
        print("Fail to check GPU", str(e))

    if True:
        try:
            check_proc.check(conf)
        except  Exception as e:
            print('Fail to check proc.',str(e))

        try:
            check_fs.check(conf)
        except  Exception as e:
            print('Fail to check fs.',str(e))

    if at_sleep_time(conf["sleep"]["begin"], conf["sleep"]["end"]):
        time.sleep(seconds(2, 0, 0))
    else:
        time.sleep(seconds(0, 40, 0))

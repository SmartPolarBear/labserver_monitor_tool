import datetime
import os

import notification

def check_mem(cuda_device):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().strip().split("\n")
    total, used = devices_info[int(cuda_device)].split(',')
    return total, used

def check(conf):
    print('[{}] Start checking GPU.'.format(datetime.datetime.now()))
    gpu_conf=conf['gpu']
    thres=int(gpu_conf['threshold'])
    gpus=gpu_conf['mon']

    free=[]
    for gpu in gpus:
        tot,used=check_mem(gpu)
        if int(used)<=thres:
            free.append(gpu)

    if len(free)<1:
        return

    msg=dict()
    msg['title']="Free GPU Available"
    msg['content']=','.join([str(f) for f in free])
    notification.notify(conf,msg)



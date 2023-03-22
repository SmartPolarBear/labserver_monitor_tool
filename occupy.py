import torch
import yaml
import time
import datetime
import os

import notification

from utils import seconds,at_sleep_time

def check_mem(cuda_device):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().strip().split("\n")
    total, used = devices_info[int(cuda_device)].split(',')
    return total, used

def prepare_tensor(cuda_device):
    os.environ["CUDA_VISIBLE_DEVICES"] = cuda_device
    total, used = check_mem(cuda_device)
    total = int(total)
    used = int(used)
    max_mem = int(total * 0.8)
    block_mem = max_mem - used
    x = torch.cuda.FloatTensor(256,1024,block_mem)
    del x
    print('Prepare the tensor cache')

while True:
    print('[{}] Start checking GPU.'.format(datetime.datetime.now()))

    with open('conf.yaml', 'r') as f:
        conf = yaml.safe_load(f)
        conf = conf['config']

    gpu_conf=conf['gpu']
    thres=int(gpu_conf['threshold'])
    gpus=gpu_conf['mon']
    exclude=gpu_conf['occupy_exclude']

    for gpu in gpus:
        tot,used=check_mem(gpu)
        if int(used)<=thres:
            if gpu in exclude:
                print("Found! but {} should be exclude".format(gpu))
            else:
                print('Occupy!')
                msg=dict()
                msg['title']="I have occupied GPU"
                msg['content']='{} is occupied now.'.format(gpu)
                notification.notify(conf,msg)
                while True:
                    try:
                        prepare_tensor(gpu)
                    except Exception as e:
                        print(str(e))
                        continue

    time.sleep(seconds(0,3,0))

    

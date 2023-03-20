import datetime
import os
import pwd

import notification

def get_proc_user_name(pid):
    proc_stat_file = os.stat("/proc/{}".format(str(pid).strip()))
    # get UID via stat call
    uid = proc_stat_file.st_uid
    # look up the username from uid
    username = pwd.getpwuid(uid)[0]
    return username

def check_mem(cuda_device):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().strip().split("\n")
    total, used = devices_info[int(cuda_device)].split(',')
    return total, used
    
def query_users(gpu):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=gpu_uuid --format=csv,nounits,noheader').read().strip().split("\n")
    
    uuid=devices_info[int(gpu)]

    pids=[]

    proceses= os.popen(
        '"/usr/bin/nvidia-smi" --query-compute-apps=gpu_uuid,pid --format=csv,noheader').read().strip().split("\n")
    for proc in proceses:
        gpuid,pid=proc.split(',')
        if gpuid==uuid:
            pids.append(pid)

    usernames=map(lambda pid:get_proc_user_name(pid),pids)
    return list(usernames)


def check(conf):
    print('[{}] Start checking GPU.'.format(datetime.datetime.now()))
    gpu_conf=conf['gpu']
    thres=int(gpu_conf['threshold'])
    
    gpus=gpu_conf['mon']
    if len(gpus)>=1:
        print("There are GPUS to check availability!")
        free=[]
        for gpu in gpus:
            tot,used=check_mem(gpu)
            if int(used)<=thres:
                free.append(gpu)

        if len(free)>=1:
            msg=dict()
            msg['title']="Free GPU Available"
            msg['content']=','.join([str(f) for f in free])
            msg['content']+=' is/are available now.'
            notification.notify(conf,msg)

    mon_user_gpus=gpu_conf['mon_user']
    if len(mon_user_gpus)>=1:
        print("There are GPUs to check users.")
        msg=dict()
        msg['title']="GPU Users Report"
        msg['content'] = "Here's gpu user report.\n"
        for gpu in mon_user_gpus:
            users = query_users(gpu)
            if len(users)>=2:
                msg['content']+=','.join([str(f) for f in users])
                msg['content']+=' is/are using gpu {} now.\n'.format(gpu)
        notification.notify(conf,msg)

if __name__=="__main__":
    print("query_users",query_users(0))
    print("check_mem",check_mem(0))

import datetime
import os
import pwd

import notification

def get_proc_user_name(pid):
    try:
        proc_stat_file = os.stat("/proc/{}".format(str(pid).strip()))
        # get UID via stat call
        uid = proc_stat_file.st_uid
        # look up the username from uid
        username = pwd.getpwuid(uid)[0]
        return username
    except:
        return "<unknown user>"

def check_mem(cuda_device,gpus=None):
    cmd = '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader'
    if gpus is not None:
        cmd += ' -i {}'.format(','.join(map(str,gpus)))
    devices_info = os.popen(cmd).read().strip().split("\n")
    di_map = dict(zip(map(str,gpus),devices_info))
    total, used = di_map[str(cuda_device)].split(',')
    return total, used
    
def query_users(gpu,gpus=None):
    gpus_postfix = ""
    if gpus is not None:
        gpus_postfix += ' -i {}'.format(','.join(map(str,gpus)))

    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=gpu_uuid --format=csv,nounits,noheader'+gpus_postfix).read().strip().split("\n")
    di_map = dict(zip(map(str,gpus),devices_info))
    uuid=di_map[str(gpu)]

    pids=[]

    proceses= os.popen(
        '"/usr/bin/nvidia-smi" --query-compute-apps=gpu_uuid,pid --format=csv,noheader'+gpus_postfix).read().strip().split("\n")
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
        print("There are GPUS to check availability:",gpus)
        free=[]
        for gpu in gpus:
            tot,used=check_mem(gpu,gpus=gpus)
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
        print("There are GPUs to check users:",mon_user_gpus)
        msg=dict()
        msg['title']="GPU Users Report"
        msg['content'] = "Here's gpu user report for gpu {}:\n".format(','.join(map(str,mon_user_gpus)))
        count=0
        for gpu in mon_user_gpus:
            try:
                users = list(set(query_users(gpu,gpus=mon_user_gpus)))
                if len(users)>=1:
                    count += 1
                    msg['content']+=','.join([str(f) for f in users])
                    msg['content']+=' is/are using gpu {} now.\n'.format(gpu)
            except:
                msg['content']+='{} cannot be monitored.\n'.format(gpu)
        if count != 0:
            notification.notify(conf,msg)
        else:
            print("No gpu checked for user")

if __name__=="__main__":
    print("query_users",query_users(0))
    print("check_mem",check_mem(0))

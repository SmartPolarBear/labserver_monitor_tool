import torch
import os
import argparse

def check_mem(cuda_device):
    devices_info = os.popen(
        '"/usr/bin/nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().strip().split("\n")
    total, used = devices_info[int(cuda_device)].split(',')
    return total, used

def prepare_tensor(cuda_device,factor):
    total, used = check_mem(cuda_device)
    total = int(total)
    used = int(used)
    max_mem = int(total * factor)
    block_mem = max_mem - used
    x = torch.cuda.FloatTensor(256,1024,block_mem)
    del x
    print('Prepare the tensor cache')


if __name__=='__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('--gpu',type=int)
    parser.add_argument('--ratio',type=float)

    args=parser.parse_args()
    while True:
        try:
            prepare_tensor(args.gpu,args.ratio)
        except:
            continue
    


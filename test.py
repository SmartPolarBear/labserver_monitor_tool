import torch

def proxy_empty_cuda():
    print('Proxy called')
    return

torch.cuda.empty_cache = proxy_empty_cuda

torch.cuda.empty_cache()
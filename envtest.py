import sys
import os
import subprocess
# 输出python版本
print("python版本信息：")
print(sys.version)

# 输出GPU信息
print("GPU信息：")
os.system("nvidia-smi")

# 输出CUDA版本
print("CUDA版本：")
os.system("nvcc --version")

# 输出pip包信息
print("pip包信息：")
piplist = subprocess.check_output(["pip", "list"], text=True)
print(piplist)

# 如果存在torch包，则输出torch版本、cuda是否可用，以及torch的cuda构建版本
if "torch" in piplist:
    import torch
    print("torch版本：", torch.__version__,"\n")
    print("CUDA是否可用：", torch.cuda.is_available(),"\n")
    print("torch的cuda构建版本：", torch.version.cuda,"\n")
    print("torch的cuDNN版本：", torch.backends.cudnn.version(),"\n")
    print("torch的cuDNN是否可用：", torch.backends.cudnn.is_available(),"\n")
else:
    print("torch包不存在\n")

# 输出numpy信息
if "numpy" in piplist:
    import numpy as np
    print("numpy版本：", np.__version__,"\n")
else:
    print("numpy包不存在\n")

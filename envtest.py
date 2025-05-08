import sys
import os
import subprocess
import argparse

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="获取系统信息并将pip包列表输出到文件")
parser.add_argument('--pipoutput', '-o', type=str, nargs='?', default='LocalEnvList.txt', const='LocalEnvList.txt', help='指定pip list输出的文件名，默认值为LocalEnvList.txt')
args = parser.parse_args()

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

# 如果提供了pipoutput参数或使用了默认值，则获取pip包信息，并将其写入到指定的文件中
if args.pipoutput:
    print(f"pip包信息输出到文件: {args.pipoutput}")
    with open(args.pipoutput, "w") as f:
        subprocess.run(["pip", "list"], stdout=f, text=True)
else:
    # 这个分支实际上不会被执行，因为即使没有提供参数，也会使用默认值
    piplist = subprocess.run(["pip", "list"])


# 获取pip包信息的文本内容用于后续检查
piplist_output = subprocess.run(["pip", "list"], capture_output=True, text=True)
piplist = piplist_output.stdout

print("科学计算相关库：")
# 如果存在torch包，则输出torch版本、cuda是否可用，以及torch的cuda构建版本
if "torch" in piplist:
    import torch
    print("torch版本：", torch.__version__,"\n")
    print("CUDA是否可用：", torch.cuda.is_available(),"\n")
    print("torch的cuda构建版本：", torch.version.cuda,"\n")
    print("torch的cuDNN是否可用：", torch.backends.cudnn.is_available(),"\n")    
    print("torch的cuDNN版本：", torch.backends.cudnn.version(),"\n")
    if torch.backends.mps.is_available():
        print("torch的MPS是否可用：", torch.backends.mps.is_available(),"\n")
    if torch.cuda.is_available():
        print("torch的CUDA是否可用：", torch.cuda.is_available(),"\n")
        print("torch的GPU数量：", torch.cuda.device_count(),"\n")
    if torch.xpu.is_available():
        print("torch的XPU是否可用：", torch.xpu.is_available(),"\n")
        print("torch的XPU数量：", torch.xpu.device_count(),"\n")
else:
    print("torch包不存在\n")

# 输出torchvision信息
if "torchvision" in piplist:
    import torchvision
    print("torchvision版本：", torchvision.__version__,"\n")
else:
    print("torchvision包不存在\n")

# 输出torchaudio信息
if "torchaudio" in piplist:
    import torchaudio
    print("torchaudio版本：", torchaudio.__version__,"\n")
else:
    print("torchaudio包不存在\n")


# 输出numpy信息
if "numpy" in piplist:
    import numpy as np
    print("numpy版本：", np.__version__,"\n")
else:
    print("numpy包不存在\n")

# 输出pandas信息
if "pandas" in piplist:
    import pandas as pd
    print("pandas版本：", pd.__version__,"\n")
else:
    print("pandas包不存在\n")

print("构建工具相关库：")

# 检查setuptools包
if "setuptools" in piplist:
    import setuptools
    print("setuptools版本：", setuptools.__version__,"\n")
else:
    print("setuptools包不存在\n")

# 检查pip包
if "pip" in piplist:
    import pip
    print("pip版本：", pip.__version__,"\n")
else:
    print("pip包不存在\n")

# 输出ninja信息
if "ninja" in piplist:
    import ninja
    print("ninja版本：", ninja.__version__,"\n")
else:
    print("ninja包不存在\n")

# 输出cmake信息
if "cmake" in piplist:
    import cmake
    print("cmake版本：", cmake.__version__,"\n")
else:
    print("cmake包不存在\n")




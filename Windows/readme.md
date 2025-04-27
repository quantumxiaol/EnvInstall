# 在Windows上安装虚拟环境

# 环境变量

环境变量是将命令指向到其对应的路径下

例如，安装Python时，将命令指向到Python的安装路径下

此时执行python helloworld.py时，会自动调用Python解释器

即为 path/to/python/python.exe helloworld.py

这样输入命令时，操作系统知道要用什么软件来执行命令

# 安装anaconda

在官方网站上下载anaconda安装包，并安装
    https://www.anaconda.com/products/individual

或者在清华镜像站下载anaconda安装包，并安装
    https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

创建虚拟环境

打开Anaconda Prompt

    conda create -n myenv python=3.8
这将会创建一个名为myenv的虚拟环境，并安装Python 3.8版本

创建虚拟环境时不要开启VPN，否则可能会报SSL error。



# 安装Pytorch

pytorch有CPU版本、CUDA版本、MPS版本
在官网下载，选择下载的版本
    https://pytorch.org/

旧版本在
https://pytorch.org/get-started/previous-versions/
下载

例如

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
这将会安装基于CUDA11.8的PyTorch和依赖库

# pip和conda安装

pip（Pip Installs Packages）是 Python 官方推荐的包管理工具，主要用于从 Python Package Index (PyPI) 下载并安装 Python 包

conda 是一个开源的软件包管理和环境管理系统，最初为 Anaconda 发行版设计。它不仅可以管理 Python 包，还可以管理非 Python 软件包以及整个运行环境。

一些python包在conda上可能不全，或找不到对应的依赖。

# 源

## pip安装
使用pip安装某个包

    pip install PackageName
添加 `-i` 或 `--index-url` 选项指定镜像源

    pip install PackageName -i https://pypi.tuna.tsinghua.edu.cn/simple

## conda安装
使用conda安装某个包

    conda install PackageName
添加 `-c` 或 `--channel` 选项指定镜像源

    conda install PackageName -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

## 常见的源
### pip
清华源  https://pypi.tuna.tsinghua.edu.cn/simple

中科大源    https://pypi.mirrors.ustc.edu.cn/simple

阿里云源    https://mirrors.aliyun.com/pypi/simple/

### conda
defaults
这是 Conda 默认使用的通道集合，包括了 Anaconda 发行版中预安装的所有包。

https://repo.anaconda.com/pkgs/

conda-forge
一个由社区维护的通道，提供了大量额外的包，特别是那些不在 defaults 通道中的包。

https://conda.anaconda.org/conda-forge

bioconda
针对生物信息学领域特别定制的通道，包含了许多生物信息学工具和库。

https://conda.anaconda.org/bioconda

使用 bioconda 时通常还需要同时配置 conda-forge 和 defaults，以确保兼容性。

msys2
提供了 Windows 下的 Unix 工具链，适用于编译 C/C++ 等语言的项目。

https://conda.anaconda.org/msys2

pytorch
PyTorch 官方提供的通道，专门用于分发 PyTorch 及其相关库。

https://conda.anaconda.org/pytorch

清华大学 TUNA 镜像

https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

中国科学技术大学镜像

https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
https://mirrors.ustc.edu.cn/anaconda/pkgs/main/

阿里云镜像

https://mirrors.aliyun.com/anaconda/pkgs/free/
https://mirrors.aliyun.com/anaconda/pkgs/main/
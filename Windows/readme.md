# 在Windows上安装虚拟环境

## 环境变量

环境变量是将命令指向到其对应的路径下

例如，安装Python时，将命令指向到Python的安装路径下

此时执行python helloworld.py时，会自动调用Python解释器

即为 path/to/python/python.exe helloworld.py

这样输入命令时，操作系统知道要用什么软件来执行命令

## 安装anaconda

在官方网站上下载anaconda安装包，并安装[anaconda](https://www.anaconda.com/products/individual)

或者在清华镜像站下载anaconda安装包，并安装[tuna/anaconda](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

## 创建虚拟环境

打开Anaconda Prompt

    conda create -n myenv python=3.8
这将会创建一个名为myenv的虚拟环境，并安装Python 3.8版本

创建虚拟环境时不要开启VPN，否则可能会报SSL error。

## 安装Pytorch

pytorch有CPU版本、CUDA版本、MPS版本
在官网下载，选择下载的版本[pytorch](https://pytorch.org/)

旧版本在[pytorch/previous-versions](https://pytorch.org/get-started/previous-versions/)下载

例如

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
这将会安装基于CUDA11.8的PyTorch和依赖库

## pip和conda安装

pip（Pip Installs Packages）是 Python 官方推荐的包管理工具，主要用于从 Python Package Index (PyPI) 下载并安装 Python 包

conda 是一个开源的软件包管理和环境管理系统，最初为 Anaconda 发行版设计。它不仅可以管理 Python 包，还可以管理非 Python 软件包以及整个运行环境。

一些python包在conda上可能不全，或找不到对应的依赖。

### pip安装

使用pip安装某个包

    pip install PackageName
添加 `-i` 或 `--index-url` 选项指定镜像源

    pip install PackageName -i https://pypi.tuna.tsinghua.edu.cn/simple

### conda安装

使用conda安装某个包

    conda install PackageName
添加 `-c` 或 `--channel` 选项指定镜像源

    conda install PackageName -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

### 常见的源

#### pip

清华源  https://pypi.tuna.tsinghua.edu.cn/simple

中科大源    https://pypi.mirrors.ustc.edu.cn/simple

阿里云源    https://mirrors.aliyun.com/pypi/simple/

#### conda

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

## 包安装

### 工具链配置

安装Python时，通常会安装相应的工具链，如gcc、g++、clang、clang++等。

#### Visual Studio

从源码编译安装通常需要Microsoft Visual C++编译器（如cl.exe）工具链。
下载并安装Visual Studio Community，在安装过程中选择“使用C++的桌面开发”工作负载。

设置环境变量以指向正确的MSVC工具链路径。可以通过运行vcvarsall.bat脚本来自动设置这些变量。

运行`pip install -e .`为从本地源码安装包

默认情况下，pip 在安装包时会为构建过程创建一个隔离的环境（即子进程）。这可能导致子进程无法访问父进程中的依赖项（如 torch）。通过使用 `--no-build-isolation` 选项禁用构建隔离，可以让构建过程直接使用当前环境中的包。

#### pip升级

运行`python.exe -m pip install --upgrade pip`升级

pip是Python的包管理工具，用于安装、更新和卸载Python包。

#### ninja

ninja是一个构建系统，它使用一个简单的文本格式来描述构建规则，然后使用一个编译器来生成目标文件。

#### pybind11

是一个轻量级的头文件库，它主要用于将C++代码与Python进行绑定。

pybind11是一个C++11/14/17的Python绑定库，它允许C++代码与Python进行交互。它提供了一种简单的方法来将C++函数和类暴露给Python，使得Python程序员可以轻松地调用C++代码。

#### setuptools 和 wheel

这些是基本的打包工具，setuptools 用于构建扩展，而 wheel 支持创建预编译的二进制包（.whl 文件）。

## [报错](./error.md)

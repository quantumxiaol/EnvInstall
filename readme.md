# 安装虚拟环境的一些总结

## [Windows](./Windows/readme.md)

## [WSL](./WSL/readme.md)

安装CUDA的效果
<img src="./png/img_nvcc.png">
<img src="./png/img_nvidia.png">
安装Anaconda
<img src="./png/img_anaconda.png">


## [Linux](./Linux/readme.md)
Linux系统安装

## [Git](./Git/readme.md)
使用Git和GitHub

## [实例](./EnvInstallEg/readme.md) 
为一些项目安装环境

# 写在前面
## 环境变量
环境变量是一种动态的值，它可以在计算机的操作系统中为运行中的进程提供配置信息。简单来说，环境变量是一些键值对，它们存储了操作系统或用户定义的信息，这些信息可以被操作系统本身、应用程序或者脚本使用来调整其行为。

从结果看，环境变量就是在命令行输入一个命令，操作系统知道用什么工具来执行。如果没有环境变量，你可以直接使用对应的文件执行。

以windows为例，在cmd中输入  `python helloworld.py`
和输入 `/path/to/python.exe helloworld.py`
是一样的，后者可以直接找到python解释器，用解释器执行helloworld.py。设置python的环境变量，就是让windows知道如何执行python。


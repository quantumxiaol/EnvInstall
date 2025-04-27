# 配置linux的几种方法

## 1 WSL[文档](../WSL/readme.md)
在windows11后全面支持Windows Subsystem for Linux，使得在Windows系统下可以直接运行linux系统无需虚拟机。
在管理员模式下向powershell中输入

    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
安装WSL必备组件，并输入

    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart 
打开hyper-V虚拟化后即可在应用商店中下载linux系统。

如果出现参考的对象类型不支持尝试的操作，重置网络net winsock reset即可。
缺点是不原生支持GUI界面。

## 2 安装双系统
以ubuntu为例，在ubuntu官网中下载镜像，使用烧录软件烧录到U盘中制作安装系统的引导盘，在实体机中安装双系统。在重启电脑后进入bios，以引导盘作为优先启动项，在引导系统的指引下安装到硬盘的空闲位置。

也可以使用Ventoy烧录U盘，制作多个启动镜像，甚至可以直接在其中启动虚拟机。Ventoy中可以直接运行vhdx镜像文件，免去了安装虚拟机。

缺点是每次开机时要调整或选择启动项。

## 3 安装虚拟机
可以使用VMware或VirtualBox安装Linux系统，使用iso文件在虚拟机中安装ubuntu系统。接下来安装过程同在实体机过程基本一致。

特别的，由于hyper-V的存在，虚拟机和WSL（以及WSA）会冲突。

## 4 购买云服务器
可以在阿里云、腾讯云或华为云中购买云服务器（轻量应用服务器），选定linux系统，购买后，在防火墙中开启22端口后，在本地输入云服务器ip，使用VSCode或XShell等SSH连接到服务器，之后像本地操作一样使用linux系统。如过要GUI，可以开启VNC服务后在本地使用VNC viewer远程连接。使用Xftp或WinSCP上传下载文件。
缺点是带宽昂贵，默认为5M，上传下载文件不方便。~~而且这个服务器多半是跑不了深度学习的~~

特别的，选的GPU服务器时可以指定CUDA和其他环境，一般是默认装好的，开盖即用。


# Linux 系统安装
安装Ubuntu系统
## 制作启动盘
下载 Ubuntu 镜像
https://ubuntu.com/download/desktop

使用Rufus或Etcher将iso烧录到U盘

如果电脑是较新的 UEFI 系统，选择 GPT 分区方案。
如果电脑是旧的 BIOS 系统，选择 MBR 分区方案。

## 从U盘启动
进入 BIOS/UEFI 设置，开机时按下特定键（通常是 F2、F12、DEL 或 ESC，具体取决于主板型号）。

在 BIOS 设置中确认启动模式：UEFI 或 Legacy（BIOS）。将 U 盘设置为第一启动项。

保存更改后重启电脑，系统应该会从 U 盘启动。

按不出来可以在windows设置-更新和安全-恢复-高级启动 重启电脑，从USB设备恢复
## 安装Ubuntu
配置系统安装到什么磁盘的区域

# 配置虚拟环境[参照WSL](../WSL/readme.md)
安装CUDA和Anaconda

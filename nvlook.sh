# # 查看当前文件权限
# ls -l nvlook.sh
# # 添加执行权限
# chmod +x nvlook.sh
# # 再次查看权限，确认有 x（执行）权限
# ls -l nvlook.sh

#  查看 nvidia 模块
lsmod | grep nvidia
# 查看 nvidia 设备
ls -l /dev/nvidia*
# 查看 nvidia cuda 版本
nvcc --version
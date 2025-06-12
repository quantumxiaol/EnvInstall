# # 查看当前文件权限
# ls -l envlook.sh
# # 添加执行权限
# chmod +x envlook.sh
# # 再次查看权限，确认有 x（执行）权限
# ls -l envlook.sh

echo $CUDA_HOME
echo $CUDA_PATH
echo $LD_LIBRARY_PATH
# echo $PATH
# echo $PYTHONPATH

python --version
python -c "import torch; print(torch.__version__)"
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.version.cuda)"
nvcc --version
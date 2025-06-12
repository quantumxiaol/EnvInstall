# VideoAgent

[VideoAgent: A Memory-augmented Multimodal Agent for Video Understanding](https://arxiv.org/pdf/2403.11481)

[code](https://github.com/YueFan1014/VideoAgent)

[relay ENV](https://github.com/PKU-YuanGroup/Video-LLaVA)

## 安装过程

要求

- Python >= 3.10
- Pytorch == 2.0.1
- CUDA 版本 >= 11.7

安装所需的软件包：

    git clone https://github.com/PKU-YuanGroup/Video-LLaVA
    cd Video-LLaVA
    conda create -n videollava python=3.10 -y
    conda activate videollava
    pip install --upgrade pip  # enable PEP 660 support
    pip install -e .
    pip install -e ".[train]"
    pip install flash-attn --no-build-isolation
    pip install decord opencv-python git+https://github.com/facebookresearch/pytorchvideo.git@28fe037d212663c6a24f373b94cc5d478c8c1a1d

报错：
>flash-attn
  DEPRECATION: Building 'flash-attn' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce this behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'flash-attn'. Discussion can be found at https://github.com/pypa/pip/issues/6334
  Building wheel for flash-attn (setup.py) ... error
  error: subprocess-exited-with-error
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [303 lines of output]
      /home/lxl/anaconda3/envs/videollava/lib/python3.10/site-packages/torch/cuda/__init__.py:107: UserWarning: CUDA initialization: CUDA unknown error - this may be due to an incorrectly set up environment, e.g. changing env variable CUDA_VISIBLE_DEVICES after program start. Setting the available devices to be zero. (Triggered internally at ../c10/cuda/CUDAFunctions.cpp:109.)
        return torch._C._cuda_getDeviceCount() > 0
      No CUDA runtime is found, using CUDA_HOME='/usr/local/cuda'
      torch.__version__  = 2.0.1+cu117
      /home/lxl/anaconda3/envs/videollava/lib/python3.10/site-packages/setuptools/__init__.py:94: _DeprecatedInstaller: setuptools.installer and fetch_build_eggs are deprecated.
      RuntimeError: Error compiling objects for extension
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for flash-attn
  Running setup.py clean for flash-attn
Failed to build flash-attn
ERROR: Failed to build installable wheels for some pyproject.toml based projects (flash-attn)

>Key Error
/home/lxl/anaconda3/envs/videollava/lib/python3.10/site-packages/torch/cuda/__init__.py:107: UserWarning: CUDA initialization: CUDA unknown error - this may be due to an incorrectly set up environment, e.g. changing env variable CUDA_VISIBLE_DEVICES after program start. Setting the available devices to be zero. (Triggered internally at ../c10/cuda/CUDAFunctions.cpp:109.)
  return torch._C._cuda_getDeviceCount() > 0
False

>lsmod | grep nvidia
nvidia_uvm           2035712  2
nvidia_drm            135168  27
nvidia_modeset       1552384  103 nvidia_drm
nvidia              89993216  1434 nvidia_uvm,nvidia_modeset
drm_kms_helper        249856  3 nvidia_drm
drm                   696320  31 drm_kms_helper,nvidia,nvidia_drm
i2c_nvidia_gpu         16384  0
i2c_ccgx_ucsi          16384  1 i2c_nvidia_gpu
video                  73728  2 ideapad_laptop,nvidia_modeset

>ls -l /dev/nvidia*
crw-rw-rw- 1 root root 195,   0  6月  9 16:24 /dev/nvidia0
crw-rw-rw- 1 root root 195, 255  6月  9 16:24 /dev/nvidiactl
crw-rw-rw- 1 root root 195, 254  6月  9 16:24 /dev/nvidia-modeset
crw-rw-rw- 1 root root 510,   0  6月  9 16:24 /dev/nvidia-uvm
crw-rw-rw- 1 root root 510,   1  6月  9 16:24 /dev/nvidia-uvm-tools

sudo apt-get install nvidia-modprobe

似乎是系统suspended，重新启动后正常。

版本不匹配，到[flash_attn](https://github.com/Dao-AILab/flash-attention/releases)找存在cu117的版本，制定安装2.3.5。
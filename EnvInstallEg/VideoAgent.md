# VideoAgent

[VideoAgent: A Memory-augmented Multimodal Agent for Video Understanding](https://arxiv.org/pdf/2403.11481)

[code](https://github.com/YueFan1014/VideoAgent)

[relay ENV](https://github.com/PKU-YuanGroup/Video-LLaVA)[paper/Video-LLaVA](https://arxiv.org/pdf/2311.10122)

## 项目介绍

给定一个视频和一个问题，VideoAgent 有两个阶段：内存构建阶段和推理阶段。在内存构建阶段，从视频中提取结构化信息并存储在内存中。在推理阶段，系统会提示 LLM 使用一组与内存交互的工具来回答问题。

### VideoAgent的主要能力

视频理解：通过对视频内容进行结构化表示（包括时间和对象记忆），VideoAgent能够理解和回答关于视频内容的自由形式查询。

复杂问题解决：VideoAgent在多个视频理解基准上展示了其优越性能，如EgoSchema、Ego4D NLQ、WorldQA和NExT-QA等。

### 工具及其使用方法

VideoAgent提供了一套最小但必要的工具集，专注于查询记忆以简化推理过程并提高性能。

字幕检索（Caption Retrieval）

目标：从指定的视频片段中提取字幕。

使用方法：给定时间记忆MT以及开始和结束时间步骤tstart和tend作为参数，该工具直接从时间记忆中检索这些字幕。

解决的问题：帮助获取特定时间段内的事件描述，便于理解视频内容。

段落定位（Segment Localization）

目标：根据文本查询squery定位视频片段。

使用方法：将squery的文本特征与时间记忆MT中的视频特征进行比较，返回最相关的前5个视频片段。

解决的问题：允许用户通过自然语言查询来查找特定内容的视频片段。

视觉问答（Visual Question Answering）

目标：回答有关特定视频片段的问题，获取超出字幕或对象状态的信息。

使用方法：当调用visual_question_answering(·)时运行Video-LLaVA模型。

解决的问题：为用户提供关于特定视频内容的详细信息，增强对视频内容的理解。

对象记忆查询（Object Memory Querying）

目标：执行关于视频中出现的对象的复杂信息检索。

使用方法：首先从查询中提取相关对象描述，然后将这些描述的文本特征与对象记忆MO中的对象特征进行比较，最后由LLM编写SQL代码查询数据库并获取所需信息。

解决的问题：支持用户通过自由形式的语言查询搜索视频中的对象，例如“我从冰箱里拿出了多少红色杯子？”这样的复杂查询。

## 安装过程

### Video-LLaVA

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

版本不匹配，到[flash_attn](https://github.com/Dao-AILab/flash-attention/releases)找存在cu117的版本，指定安装2.3.5。

### Video Agent

运行`conda env create -f environment.yaml`创建名为videoagent的conda环境。

可以把environment.yaml中pip的部分移到requirements.txt中，然后
运行`pip install -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple`安装依赖。

安装gensim==3.8.3时报错。
>unicodeobject.h:446:26: note: declared here
        446 | static inline Py_ssize_t _PyUnicode_get_wstr_length(PyObject *op) {
            |                          ^~~~~~~~~~~~~~~~~~~~~~~~~~
      error: command '/usr/bin/gcc' failed with exit code 1
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for gensim
  Running setup.py clean for gensim
Successfully built clip nlg-eval
Failed to build gensim
ERROR: Could not build wheels for gensim, which is required to install pyproject.toml-based projects

似乎是gensim3.8.3不支持python3.9。

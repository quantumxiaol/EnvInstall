# 踩坑记录

## Windows
我在Windows上安装，踩了不少坑，最后也没有成功，最后是pyrep无法使用，我认为这个版本不是为windows设计的，所以安装会失败。~而且训练测试sh不能使用~

### 安装pytorch3d
>E:\py\ENV\pytorch3d-main\pytorch3d\csrc\./pulsar/pytorch/renderer.h(118): error C4430: 缺少类型说明符 - 假定为 int。注意: C++ 不支持默认 int
    E:\py\ENV\pytorch3d-main\pytorch3d\csrc\./pulsar/pytorch/renderer.h(118): error C2143: 语法错误: 缺少“,”(在“<”的前面)
    E:\py\ENV\pytorch3d-main\pytorch3d\csrc\ext.cpp(159): error C2039: "backward": 不是 "pulsar::pytorch::Renderer" 的成员
    E:\py\ENV\pytorch3d-main\pytorch3d\csrc\./pulsar/pytorch/renderer.h(18): note: 参见“pulsar::pytorch::Renderer”的声明
    E:\py\ENV\pytorch3d-main\pytorch3d\csrc\ext.cpp(108): error C2065: “backward”: 未声明的标识符
    error: command 'F:\\Visual Studio\\VC\\Tools\\MSVC\\14.29.30133\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2

这里pytorch3d时通过源码构建的，这个错误是说源文件的c++的语法有问题，但这不太可能。
是windows上需要配置VS工具链和cl.exe，在cmd中输出`cl`有输出说明cl.exe可用

### 安装PyRep
>(RLBench) E:\py\ENV\ManiGaussian\ManiGaussian-main\third_party\PyRep>pip install .
Processing e:\py\env\manigaussian\manigaussian-main\third_party\pyrep
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: PyRep
  Building wheel for PyRep (setup.py) ... error
  error: subprocess-exited-with-error
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [9 lines of output]
      creating symlink: C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\libcoppeliaSim.so.1 -> C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\libcoppeliaSim.so
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "E:\py\ENV\ManiGaussian\ManiGaussian-main\third_party\PyRep\setup.py", line 8, in <module>
          import cffi_build.cffi_build as cffi_build
        File "E:\py\ENV\ManiGaussian\ManiGaussian-main\third_party\PyRep\cffi_build\cffi_build.py", line 747, in <module>
          os.symlink(path, path + '.1')
      FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。: 'C:\\Program Files\\CoppeliaRobotics\\CoppeliaSimEdu\\libcoppeliaSim.so' -> 'C:\\Program Files\\CoppeliaRobotics\\CoppeliaSimEdu\\libcoppeliaSim.so.1'
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for PyRep
  Running setup.py clean for PyRep
  error: subprocess-exited-with-error
  × python setup.py clean did not run successfully.
  │ exit code: 1
  ╰─> [9 lines of output]
      creating symlink: C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\libcoppeliaSim.so.1 -> C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\libcoppeliaSim.so
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "E:\py\ENV\ManiGaussian\ManiGaussian-main\third_party\PyRep\setup.py", line 8, in <module>
          import cffi_build.cffi_build as cffi_build
        File "E:\py\ENV\ManiGaussian\ManiGaussian-main\third_party\PyRep\cffi_build\cffi_build.py", line 747, in <module>
          os.symlink(path, path + '.1')
      FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。: 'C:\\Program Files\\CoppeliaRobotics\\CoppeliaSimEdu\\libcoppeliaSim.so' -> 'C:\\Program Files\\CoppeliaRobotics\\CoppeliaSimEdu\\libcoppeliaSim.so.1'
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed cleaning build dir for PyRep
Failed to build PyRep
ERROR: Failed to build installable wheels for some pyproject.toml based projects (PyRep)

问题的核心是 os.symlink 在尝试创建符号链接时失败了，因为目标文件已经存在。我把这一行注释了，so是linux的文件链接，现在想来这就是项目无法在windows上跑的原因。这个包这个版本就不支持windows，pip安装这个包版本是3，源码构建版本是4。

>LINK : fatal error LNK1181: 无法打开输入文件“coppeliaSim.lib”

没有文件 windows上只有coppeliaSim.dll，没有对应的lib，dll是动态链接，lib是静态的。
自己用VS和gendef根据dll生成了一个对应的lib。

>无法导入_sim_cffi模块
from ._sim_cffi import ffi, lib

从_sim_cffi.cp39-win_amd64.pyd无法导入_sim_cffi模块，报错了（Windows，X86_64）
我用Depend查看依赖关系，发现Qt5core.dll爆红，但是对应的dll存在于path中。这可能是由于这个pyrep这个版本无法在windows中使用。


>E:\Anaconda3\envs\RLBench\lib\site-packages\setuptools\_distutils\_msvccompiler.py:12: UserWarning: _get_vc_env is private; find an alternative (pypa/distutils#340)
      warnings.warn(
    ninja: error: Stat(E:/py/ENV/ManiGaussian/ManiGaussian-main/third_party/ODISE/third_party/Mask2Former/build/temp.win-amd64-cpython-39/Release/py/ENV/ManiGaussian/ManiGaussian-main/third_party/ODISE/third_party/Mask2Former/mask2former/modeling/pixel_decoder/ops/src/cpu/ms_deform_attn_cpu.obj): Filename longer than 260 characters
    Traceback (most recent call last):
      File "E:\Anaconda3\envs\RLBench\lib\site-packages\torch\utils\cpp_extension.py", line 1893, in _run_ninja_build
        subprocess.run(
      File "E:\Anaconda3\envs\RLBench\lib\subprocess.py", line 528, in run
        raise CalledProcessError(retcode, process.args,
    subprocess.CalledProcessError: Command '['ninja', '-v']' returned non-zero exit status 1.

错误提示 Filename longer than 260 characters 表明 Windows 文件系统对路径长度的限制（默认最大为 260 个字符）导致了编译失败。

修改windows注册表，或者把它移到更短的路径

### 安装diff-gaussian-rasterization
>(RLBench) E:\py\ENV\diff-gaussian-rasterization>pip install -e .
Obtaining file:///E:/py/ENV/diff-gaussian-rasterization
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [12 lines of output]
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "E:\py\ENV\diff-gaussian-rasterization\setup.py", line 21, in <module>
          CUDAExtension(
        File "E:\Anaconda3\envs\RLBench\lib\site-packages\torch\utils\cpp_extension.py", line 1130, in CUDAExtension
          library_dirs += library_paths(device_type="cuda")
        File "E:\Anaconda3\envs\RLBench\lib\site-packages\torch\utils\cpp_extension.py", line 1271, in library_paths
          paths.append(_join_cuda_home(lib_dir))
        File "E:\Anaconda3\envs\RLBench\lib\site-packages\torch\utils\cpp_extension.py", line 2525, in _join_cuda_home
          raise OSError('CUDA_HOME environment variable is not set. '
      OSError: CUDA_HOME environment variable is not set. Please set it to your CUDA install root.
      [end of output]

这个报错看起来是找不到CUDA_HOME，但其实不是这样。安装脚本会自动读取CUDA_PATH和CUDA_HOME，按理说两个只要有一个就行。似乎Windows上用CUDA_PATH，Linux上用CUDA_HOME。

我在windows上指定CUDA_HOME，以及在安装脚本中显式指定CUDA_HOME均不能奏效。

windows使用pip安装时，似乎安装进程无法继承现有的环境，所以找不到torch，我是通过构建pyproject.toml解决的


## 使用WSL安装

### clone代码库
>$ git clone https://github.com/GuanxingLu/ManiGaussian.git
Cloning into 'ManiGaussian'...
remote: Enumerating objects: 10020, done.
remote: Counting objects: 100% (134/134), done.
remote: Compressing objects: 100% (104/104), done.
error: RPC failed; curl 92 HTTP/2 stream 0 was not closed cleanly: CANCEL (err 8)
error: 6389 bytes of body are still expected
fetch-pack: unexpected disconnect while reading sideband packet
fatal: early EOF
fatal: fetch-pack: invalid index-pack output

网络问题+增加 Git 的缓冲区大小

### 安装CLIP

>Obtaining file:///home/quantumxiaol/CLIP
  Preparing metadata (setup.py) ... done
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/ftfy/
Collecting ftfy (from clip==1.0)
  Downloading ftfy-6.3.1-py3-none-any.whl.metadata (7.3 kB)
INFO: pip is looking at multiple versions of clip to determine which version is compatible with other requirements. This could take a while.
ERROR: Could not find a version that satisfies the requirement packaging (from clip) (from versions: none)
ERROR: No matching distribution found for packaging

### 安装open-clip-torch

>WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ReadTimeoutError("HTTPSConnectionPool(host='pypi.org', port=443): Read timed out. (read timeout=15)")': /simple/open-clip-torch/
Collecting open-clip-torch
  Downloading open_clip_torch-2.32.0-py3-none-any.whl.metadata (31 kB)
  WARNING: Connection timed out while downloading.
error: incomplete-download
× Download failed because not enough bytes were received (0 bytes/31 kB)
╰─> URL: https://files.pythonhosted.org/packages/32/f9/0458745c1d299411161ee3b6c32228a3de0be1d8497d779fd7f17a8e96aa/open_clip_torch-2.32.0-py3-none-any.whl.metadata
note: This is an issue with network connectivity, not pip.
hint: Consider using --resume-retries to enable download resumption.

这两个都是网络问题，可能平时Windows上开代理感受不到，WSL一下就感受到了。使用`-i https://pypi.tuna.tsinghua.edu.cn/simple`

### 安装YARR

>Collecting omegaconf (from -r requirements.txt (line 7))
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/d0/eb/9d63ce09dd8aa85767c65668d5414958ea29648a0eec80a4a7d311ec2684/omegaconf-2.0.6-py3-none-any.whl (36 kB)
WARNING: Ignoring version 2.0.6 of omegaconf since it has invalid metadata:
Requested omegaconf from https://pypi.tuna.tsinghua.edu.cn/packages/d0/eb/9d63ce09dd8aa85767c65668d5414958ea29648a0eec80a4a7d311ec2684/omegaconf-2.0.6-py3-none-any.whl (from -r requirements.txt (line 7)) has invalid metadata: .* suffix can only be used with `==` or `!=` operators
    PyYAML (>=5.1.*)
            ~~~~~~^
Please use pip<24.1 if you need to use this version.
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/e5/f6/043b6d255dd6fbf2025110cea35b87f4c5100a181681d8eab496269f0d5b/omegaconf-2.0.5-py3-none-any.whl (36 kB)
WARNING: Ignoring version 2.0.5 of omegaconf since it has invalid metadata:
Requested omegaconf from https://pypi.tuna.tsinghua.edu.cn/packages/e5/f6/043b6d255dd6fbf2025110cea35b87f4c5100a181681d8eab496269f0d5b/omegaconf-2.0.5-py3-none-any.whl (from -r requirements.txt (line 7)) has invalid metadata: .* suffix can only be used with `==` or `!=` operators
    PyYAML (>=5.1.*)
            ~~~~~~^
Please use pip<24.1 if you need to use this version.
INFO: pip is looking at multiple versions of hydra-core to determine which version is compatible with other requirements. This could take a while.
ERROR: Cannot install -r requirements.txt (line 8) and omegaconf because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested omegaconf
    hydra-core 1.0.5 depends on omegaconf<2.1 and >=2.0.5
To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency conflict
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts

依赖冲突。具体来说，omegaconf 的版本与 hydra-core 所需的版本之间存在冲突。根据错误信息：hydra-core 1.0.5 需要 omegaconf 版本在 >=2.0.5 和 <2.1 之间。
同时尝试安装的 omegaconf 版本（可能是最新版或指定的某个版本）与 pip 的版本兼容性存在问题，提示有无效的元数据。

都删了，反正最后要安装hydra-core为1.1

### 安装odise
安装detectron2

>Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Obtaining file:///home/quantumxiaol/detectron2
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [43 lines of output]
      running egg_info
      creating /tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info
      writing /tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/PKG-INFO
      writing dependency_links to /tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/dependency_links.txt
      writing requirements to /tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/requires.txt
      writing top-level names to /tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/top_level.txt
      writing manifest file '/tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/SOURCES.txt'
      /home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/torch/utils/cpp_extension.py:476: UserWarning: Attempted to use ninja as the BuildExtension backend but we could not find ninja.. Falling back to using the slow distutils backend.
        warnings.warn(msg.format('we could not find ninja.'))
      reading manifest file '/tmp/pip-pip-egg-info-chb96f39/detectron2.egg-info/SOURCES.txt'
      adding license file 'LICENSE'
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 35, in <module>
        File "/home/quantumxiaol/detectron2/setup.py", line 151, in <module>
          setup(
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/__init__.py", line 117, in setup
          return distutils.core.setup(**attrs)
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_distutils/core.py", line 186, in setup
          return run_commands(dist)
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_distutils/core.py", line 202, in run_commands
          dist.run_commands()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_distutils/dist.py", line 1002, in run_commands
          self.run_command(cmd)
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/dist.py", line 1104, in run_command
          super().run_command(command)
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_distutils/dist.py", line 1021, in run_command
          cmd_obj.run()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/command/egg_info.py", line 312, in run
          self.find_sources()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/command/egg_info.py", line 320, in find_sources
          mm.run()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/command/egg_info.py", line 548, in run
          self.prune_file_list()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/command/sdist.py", line 162, in prune_file_list
          super().prune_file_list()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_distutils/command/sdist.py", line 386, in prune_file_list
          base_dir = self.distribution.get_fullname()
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_core_metadata.py", line 275, in get_fullname
          return _distribution_fullname(self.get_name(), self.get_version())
        File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/setuptools/_core_metadata.py", line 293, in _distribution_fullname
          canonicalize_version(version, strip_trailing_zero=False),
      TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> See above for output.
note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

由于 setuptools 版本与 Python 元数据（importlib.metadata 或 packaging）版本不兼容 导致的问题。
新版本的 setuptools（如 69.0+）中使用了新的内部 API。而环境中安装了旧版本的 packaging、importlib.metadata 或其他相关依赖。
在调用 canonicalize_version() 函数时，传入了一个新版本支持但旧版本没有的参数：strip_trailing_zero。

可以降级 setuptools 到 68.1.0 `pip install "setuptools<69"`


### 安装submodules/diff-gaussian-rasterization

>cuda_rasterizer/backward.h:19:10: fatal error: glm/glm.hpp: No such file or directory
   19 | #include <glm/glm.hpp>
      |          ^~~~~~~~~~~~~
compilation terminated.
error: command '/usr/local/cuda/bin/nvcc' failed with exit code 1

自己就没全，github里只有空文件，而正确的应该是一个引用其他仓库的文件夹

我不知道什么样的项目能够自己搞出冲突来：

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
mask2former 0.1 requires hydra-core==1.1.1, but you have hydra-core 1.1.0 which is incompatible.
moviepy 2.1.2 requires numpy>=1.25.0, but you have numpy 1.23.5 which is incompatible.

### 安装完成的[环境](./ManiGaussianEnvList.md)


### 生成示例
运行bash scripts/gen_demonstrations_all.sh

>###Generating demonstrations for task: close_jar
scripts/gen_demonstrations.sh: line 9: xvfb-run: command not found
scripts/gen_demonstrations.sh: line 17: xvfb-run: command not found

系统中缺少 xvfb-run 命令，这是 Xvfb（X Virtual Framebuffer） 的一部分，是一个虚拟显示服务器，常用于在没有图形界面的环境中运行需要 GUI 的程序（比如渲染器、机器人模拟器等）。

  sudo apt update
  sudo apt install -y xvfb

>###Generating demonstrations for task: close_jar
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, webgl, xcb.
Fatal Python error: Aborted
Current thread 0x0000710bc21e1640 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/backend/sim.py", line 46 in simExtLaunchUIThread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/pyrep.py", line 55 in _run_ui_thread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 917 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Thread 0x0000710c0ab76740 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/pyrep.py", line 101 in launch
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/environment.py", line 95 in launch
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 359 in run_all_variations
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 505 in main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 261 in _run_main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 316 in run
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 521 in <module>
Aborted (core dumped)
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, webgl, xcb.
Fatal Python error: Aborted
Current thread 0x0000782f8afe1640 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/backend/sim.py", line 46 in simExtLaunchUIThread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/pyrep.py", line 55 in _run_ui_thread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 917 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Thread 0x0000782fcb7d6740 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/pyrep.py", line 101 in launch
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/environment.py", line 95 in launch
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 345 in run_all_variations
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 445 in main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 261 in _run_main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 316 in run
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 461 in <module>
Aborted (core dumped)

Qt无法找到或初始化xcb平台插件

  sudo apt-get install -y libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-shape0 libxcb-sync1 libxkbcommon-x11-0 libglu1-mesa

>###Generating demonstrations for task: close_jar
[NeRFTaskRecorder] num_views: 50
  0%|                                                                                                                       | 0/200 [00:00<?, ?it/s]malloc(): unsorted double linked list corrupted
Fatal Python error: Aborted
Thread 0x000077cfd81ff640 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 316 in wait
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 581 in wait
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/tqdm/_monitor.py", line 60 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Current thread 0x000077cfcf1e1640 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/backend/sim.py", line 46 in simExtLaunchUIThread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/pyrep.py", line 55 in _run_ui_thread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 917 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Thread 0x000077d013abe740 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/backend/sim.py", line 245 in simHandleVisionSensor
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/pyrep/objects/vision_sensor.py", line 119 in handle_explicitly
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 228 in get_mask
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 254 in get_observation
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/task_environment.py", line 86 in reset
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 426 in run_all_variations
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 505 in main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 261 in _run_main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 316 in run
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 521 in <module>
Aborted (core dumped)
malloc(): unsorted double linked list corrupted
Fatal Python error: Aborted

问题可能与内存分配有关，特别是malloc(): unsorted double linked list corrupted这个错误提示表明在程序运行期间发生了堆损坏。这种情况通常由以下几种原因导致：

并发访问冲突：多个线程同时尝试访问或修改相同的内存区域，而没有适当的同步机制。
使用了已释放的内存：程序试图访问已经被释放的内存地址。
缓冲区溢出：数组越界写入或其他形式的缓冲区溢出。

### 测试训练

执行`bash scripts/train_and_eval_w_geo_sem_dyna.sh ManiGaussian_BC 0,1 12345 close_jar`
>(base) quantumxiaol@APL-Laptop:~/ManiGaussian$ conda activate manigaussian; CUDA_VISIBLE_DEVICES=0,1 python train.py method=ManiGaussian_BC rlbench.task_name=close_jar rlbench.demo_path=/home/quantumxiaol/ManiGaussian/data/train_data replay.path=/home/quantumxiaol/ManiGaussian/replay/close_jar framework.start_seed=0 framework.use_wandb=True method.use_wandb=True framework.wandb_group=close_jar framework.wandb_name=close_jar ddp.num_devices=2 replay.batch_size=1 ddp.master_port=12345 rlbench.tasks=[close_jar,open_drawer,sweep_to_dustpan_of_size,meat_off_grill,turn_tap,slide_block_to_color_target,put_item_in_drawer,reach_and_drag,push_buttons,stack_blocks] rlbench.demos=20 method.neural_renderer.render_freq=2000 method.neural_renderer.lambda_embed=0.01 method.neural_renderer.lambda_dyna=0.1 method.neural_renderer.lambda_reg=0.0 method.neural_renderer.foundation_model_name=diffusion method.neural_renderer.use_dynamic_field=True
Traceback (most recent call last):
  File "/home/quantumxiaol/ManiGaussian/train.py", line 31, in <module>
    import run_seed_fn
  File "/home/quantumxiaol/ManiGaussian/run_seed_fn.py", line 14, in <module>
    from yarr.runners.offline_train_runner import OfflineTrainRunner
  File "/home/quantumxiaol/ManiGaussian/third_party/YARR/yarr/runners/offline_train_runner.py", line 30, in <module>
    from lightning.fabric import Fabric
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/lightning/__init__.py", line 18, in <module>
    from lightning.fabric.fabric import Fabric  # noqa: E402
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/lightning/fabric/__init__.py", line 7, in <module>
    from lightning_utilities.core.imports import package_available
ModuleNotFoundError: No module named 'lightning_utilities'
> /home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/lightning/fabric/__init__.py(7)<module>()
-> from lightning_utilities.core.imports import package_available

缺少 lightning_utilities

>    @torch.compiler.disable
AttributeError: module 'torch' has no attribute 'compiler'
> /home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/lightning/pytorch/trainer/connectors/logger_connector/result.py(355)_ResultCollection()
-> @torch.compiler.disable
AttributeError: module 'torch' has no attribute 'compiler'

python -c "import torch; print(torch.__version__); print(hasattr(torch, 'compiler'))"
2.0.0
False

使用的 PyTorch 构建版本 不是完整支持 TorchDynamo / compile 的构建；是 CPU-only 版本 或者 从非官方源（如清华镜像）安装的精简版/损坏版；
或者是 构建时未启用 torch.compile 所需依赖（如 Triton）。

torch.compiler 是 PyTorch 中与 TorchDynamo 相关的功能模块，它是在 PyTorch 2.0 中引入的一个实验性特性。TorchDynamo 是一个用于动态追踪 Python 函数的框架，旨在为 PyTorch 提供更高效的执行路径和优化机会。通过 torch.compile() 功能，用户可以对模型进行编译，从而可能获得更快的推理速度或训练性能。

torch.compile() 的作用
加速计算：通过对模型进行编译，利用后端优化器（如 NVRTC、Triton 等）来生成更高效的 CUDA 内核。
动态追踪：允许在运行时动态地捕获和优化操作序列，这有助于提高灵活性和效率。

使用pip安装torch而不是conda，就没有这个问题了。

运行训练脚本：`bash scripts/train_and_eval_w_geo_sem_dyna.sh ManiGaussian_BC 0 12345 close_jar`，能够开始训练。
### 测试CoppeliaSim
运行CoppeliaSim: `./coppeliasim.sh`，可以正常显示图形界面
### 测试RLBench
运行测试RLBench，在CoppeliaSim中显示closejar任务，内存错误

    /fix_demo.py
    # 从RLBench加载closejar，用launch在CoppeliaSim中显示
    # fix_demo.py
    # https://github.com/stepjam/RLBench
    from rlbench.action_modes.arm_action_modes import JointVelocity
    from rlbench.action_modes.gripper_action_modes import Discrete as GripperDiscrete
    from rlbench.environment import Environment
    from rlbench.tasks import CloseJar  # 使用 CloseJar 任务
    import numpy as np
    import time

    class MoveArmThenGripper:
        """A simple implementation of combining arm and gripper actions."""
        
        def __init__(self, arm_action_mode, gripper_action_mode):
            self.arm_action_mode = arm_action_mode
            self.gripper_action_mode = gripper_action_mode
            
        def action(self, scene: 'Scene', action: np.ndarray):
            arm_act_size = np.prod(self.arm_action_mode.action_shape(scene))
            arm_action = action[:arm_act_size]
            gripper_action = action[arm_act_size:]
            
            self.arm_action_mode.action(scene, arm_action)
            self.gripper_action_mode.action(scene, gripper_action)

        def action_shape(self, scene: 'Scene'):
            return (np.prod(self.arm_action_mode.action_shape(scene)) +
                    np.prod(self.gripper_action_mode.action_shape(scene)), )

        def main():
            # 设置动作模式
            arm_mode = JointVelocity()
            gripper_mode = GripperDiscrete()

            # 创建组合动作模式
            action_mode = MoveArmThenGripper(arm_mode, gripper_mode)

            # 初始化环境并传入 action_mode 参数
            env = Environment(action_mode=action_mode)
            try:
                env.launch()
                task = env.get_task(CloseJar)
                descriptions, obs = task.reset()
                print("Task reset. Descriptions:", descriptions)
                
                for _ in range(100):  # 运行100步作为演示
                    # 创建一个随机动作，这里仅为演示目的
                    arm_action = np.random.uniform(-1, 1, size=(env.action_size - 1,))
                    gripper_action = np.array([1.0 if _ % 2 == 0 else 0.0])
                    action = np.concatenate([arm_action, gripper_action])

                    obs, reward, done = env.step(action)
                    env.render()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                env.shutdown()
                time.sleep(10)

        if __name__ == '__main__':
            main()


>Error: signal 11:
/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_Z11_segHandleri+0x30)[0x70851ef0aae0]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x708571242520]
/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so(+0x1888d40)[0x70850b688d40]
QMutex: destroying locked mutex

这个错误是由 CoppeliaSim 的 Qt GUI 渲染部分引发的。

问题应该不在仿真软件上，也不是内存太小，我分给WSL2 16GB内存，应该够用。

CoppeliaSim 是基于 Qt 和 OpenGL 的 GUI 应用程序。而 RLBench 启动 CoppeliaSim 作为子进程，并尝试与其通信、渲染画面，这就可能导致以下问题：

Qt GUI 必须运行在主线程中，但 RLBench 可能是在子线程中创建了 GUI 上下文。
OpenGL 上下文初始化失败或与 Mesa 软件渲染器不兼容。

使用gdb检测

>(gdb) run
Starting program: /home/quantumxiaol/anaconda3/envs/manigaussian/bin/python /home/quantumxiaol/fix_demo.py
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff47ff640 (LWP 68549)]
[New Thread 0x7ffff1ffe640 (LWP 68550)]
[New Thread 0x7fffef7fd640 (LWP 68551)]
[New Thread 0x7fffecffc640 (LWP 68552)]
[New Thread 0x7fffea7fb640 (LWP 68553)]
[New Thread 0x7fffe7ffa640 (LWP 68554)]
[New Thread 0x7fffe57f9640 (LWP 68555)]
[New Thread 0x7fffe2ff8640 (LWP 68556)]
[New Thread 0x7fffe07f7640 (LWP 68557)]
[New Thread 0x7fffdfff6640 (LWP 68558)]
[New Thread 0x7fffdb7f5640 (LWP 68559)]
[New Thread 0x7fffd8ff4640 (LWP 68560)]
[New Thread 0x7fffd67f3640 (LWP 68561)]
[New Thread 0x7fffd5ff2640 (LWP 68562)]
[New Thread 0x7fffd37f1640 (LWP 68563)]
[New Thread 0x7fffceff0640 (LWP 68564)]
[New Thread 0x7fffce7ef640 (LWP 68565)]
[New Thread 0x7fffcbfee640 (LWP 68566)]
[New Thread 0x7fffc77ed640 (LWP 68567)]
[New Thread 0x7fffc4fec640 (LWP 68568)]
[New Thread 0x7fffc27eb640 (LWP 68569)]
[New Thread 0x7fffbffea640 (LWP 68570)]
[New Thread 0x7fffbf7e9640 (LWP 68571)]
[New Thread 0x7fffbcfe8640 (LWP 68572)]
[New Thread 0x7fffba7e7640 (LWP 68573)]
[New Thread 0x7fffb7fe6640 (LWP 68574)]
[New Thread 0x7fffb37e5640 (LWP 68575)]
[New Thread 0x7fffb0fe4640 (LWP 68576)]
[New Thread 0x7fffae7e3640 (LWP 68577)]
[New Thread 0x7fffabfe2640 (LWP 68578)]
[New Thread 0x7fffa97e1640 (LWP 68579)]
[New Thread 0x7fff9fdff640 (LWP 68580)]
[New Thread 0x7fff9e7d3640 (LWP 68607)]
[Detaching after vfork from child process 68644]
[New Thread 0x7fff7bfa4640 (LWP 68646)]
[New Thread 0x7fff7b3a3640 (LWP 68647)]
[New Thread 0x7fff7aba2640 (LWP 68648)]
[New Thread 0x7fff7a3a1640 (LWP 68649)]
[New Thread 0x7fff79ba0640 (LWP 68650)]
[New Thread 0x7fff63fff640 (LWP 68651)]
[New Thread 0x7fff637fe640 (LWP 68658)]
[New Thread 0x7fff503ff640 (LWP 68755)]
[New Thread 0x7fff4549f640 (LWP 68756)]
Thread 33 "python" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fff9fdff640 (LWP 68580)]
0x00007fff89025f7d in ?? () from /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so

>(gdb)  bt full
#0  0x00007fff89025f7d in ?? () from /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so
No symbol table info available.
#1  0x0000000000000000 in ?? ()
No symbol table info available.

崩溃确实发生在 Mesa 的软件渲染模块 swrast_dri.so 中
有时界面会加载出来，显示任务场景，但随后闪退，报一模一样的错误。

尝试利用 Windows 上的 X Server（如 VcXsrv）将 WSL2 的图形界面转发到 Windows 桌面。

>export DISPLAY=$(grep -oP '(?<=nameserver ).+' /etc/resolv.conf):0
(manigaussian) (base) quantumxiaol@APL-Laptop:~$ /home/quantumxiaol/anaconda3/envs/manigaussian/bin/python /home/quantumxiaol/fix_demo.py
qt.qpa.xcb: could not connect to display 10.255.255.254:0
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, webgl, xcb.
Aborted (core dumped)

CoppeliaSim中的qt是5.12.5编译的，但是不存在libqxcb.so。所以没法使用转发。

### 下载权重测试评估

运行`python scripts/compute_results.py --file_paths logs/gs_rgb_emb_001_dyna_01_0305/seed0/eval_data.csv --method last`测试 `pip install termcolor`安装termcolor，是终端输出颜色

>df_returns
     step  close_jar  open_drawer  sweep_to_dustpan_of_size  meat_off_grill  turn_tap  slide_block_to_color_target  put_item_in_drawer  reach_and_drag  push_buttons  stack_blocks
0   70000       28.0         64.0                      48.0            52.0      56.0                          8.0                 4.0            80.0          16.0           8.0
1   80000       44.0         64.0                      44.0            48.0      48.0                          4.0                 8.0            92.0          12.0          16.0
2   90000       16.0         68.0                      64.0            60.0      56.0                          8.0                12.0            84.0          12.0          16.0
3  100000       28.0         76.0                      64.0            60.0      56.0                         24.0                16.0            92.0          20.0          12.0
4  100000       28.0         68.0                      56.0            60.0      44.0                          8.0                12.0            88.0          28.0           0.0
5  100000       28.0         56.0                      64.0            64.0      48.0                         24.0                 8.0            88.0          12.0           0.0
6   90000       20.0         76.0                      56.0            60.0      52.0                          8.0                12.0            80.0          20.0          12.0
7  100000       32.0         68.0                      64.0            64.0      48.0                         16.0                 8.0            92.0          20.0           0.0
df_returns_cat
     step  Planning  Long  Tools  Motion  Screw  Occulusion
0   70000      34.0   6.0   45.3    56.0   28.0        64.0
1   80000      30.0  12.0   46.7    48.0   44.0        64.0
2   90000      36.0  14.0   52.0    56.0   16.0        68.0
3  100000      40.0  14.0   60.0    56.0   28.0        76.0
4  100000      44.0   6.0   50.7    44.0   28.0        68.0
5  100000      38.0   4.0   58.7    48.0   28.0        56.0
6   90000      40.0  12.0   48.0    52.0   20.0        76.0
7  100000      42.0   4.0   57.3    48.0   32.0        68.0
last_checkpoint: 3
Average return over all seeds: 44.80
Standard deviation over all seeds: 0.00

这是输出的结果，可以正常评估
### 再次测试生成数据
运行生成数据的脚本`bash scripts/gen_demonstrations_all.sh`

    task=${1}
    cd third_party/RLBench/tools
    xvfb-run -a python nerf_dataset_generator.py --tasks=${task} \
                                --save_path="../../../data/train_data" \
                                --image_size=128,128 \
                                --renderer=opengl \
                                --episodes_per_task=20 \
                                --processes=1 \
                                --all_variations=True
    xvfb-run -a python dataset_generator.py --tasks=${task} \
                                --save_path="../../../data/test_data" \
                                --image_size=128,128 \
                                --renderer=opengl \
                                --episodes_per_task=25 \
                                --processes=1 \
                                --all_variations=True
这是脚本内容，他执行了nerf_dataset_generator.py，使用opengl渲染，生成128*128的图片，保存在data/test_data下。

报错

>###Generating demonstrations for task: close_jar
[NeRFTaskRecorder] num_views: 50
  0%|                                                                                                                          | 0/200 [00:00<?, ?it/s]malloc(): unsorted double linked list corrupted
Fatal Python error: Aborted
Thread 0x0000767857fff640 (most recent call first):
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 316 in wait
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 581 in wait
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/tqdm/_monitor.py", line 60 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Current thread 0x000076787f3e1640 (most recent call first):
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/backend/sim.py", line 46 in simExtLaunchUIThread
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/pyrep.py", line 55 in _run_ui_thread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 917 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Thread 0x00007678c7d08740 (most recent call first):
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/backend/sim.py", line 245 in simHandleVisionSensor
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/objects/vision_sensor.py", line 119 in handle_explicitly
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 228 in get_mask
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 254 in get_observation
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/task_environment.py", line 86 in reset
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 426 in run_all_variations
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 505 in main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 258 in _run_main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 312 in run
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/nerf_dataset_generator.py", line 521 in <module>
Aborted (core dumped)
malloc(): unsorted double linked list corrupted
Fatal Python error: Aborted
Current thread 0x00007e2af61e1640 (most recent call first):
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/backend/sim.py", line 46 in simExtLaunchUIThread
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/pyrep.py", line 55 in _run_ui_thread
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 917 in run
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/threading.py", line 937 in _bootstrap
Thread 0x00007e2b42a42740 (most recent call first):
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/backend/sim.py", line 245 in simHandleVisionSensor
  File "/home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/objects/vision_sensor.py", line 119 in handle_explicitly
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 228 in get_mask
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/backend/scene.py", line 256 in get_observation
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/rlbench/task_environment.py", line 86 in reset
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 378 in run_all_variations
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 445 in main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 258 in _run_main
  File "/home/quantumxiaol/anaconda3/envs/manigaussian/lib/python3.9/site-packages/absl/app.py", line 312 in run
  File "/home/quantumxiaol/ManiGaussian/third_party/RLBench/tools/dataset_generator.py", line 461 in <module>
Aborted (core dumped)

PyRep / RLBench 在渲染或传感器采集阶段崩溃。
从调用栈来看，崩溃发生在：simHandleVisionSensor -> get_mask -> get_observation -> reset

### 渲染器更改

将渲染器改为opengl3，报错发生变化。这里渲染器只能选择opengl或opengl3。

>###Generating demonstrations for task: close_jar
[NeRFTaskRecorder] num_views: 50
  0%|                                                                                                                          | 0/200 [00:00<?, ?it/s]
Error: signal 11:
/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_Z11_segHandleri+0x30)[0x76d74ab0aae0]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x76d79ce42520]
/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so(+0xc25f7d)[0x76d722a25f7d]
QMutex: destroying locked mutex
Error: signal 11:
/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_Z11_segHandleri+0x30)[0x74874030aae0]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x748792442520]
/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so(+0xc25f7d)[0x748721a25f7d]
QMutex: destroying locked mutex

错误发生在 CoppeliaSim 的库文件 (libcoppeliaSim.so.1) 中。
错误与 /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so 相关，这是 Mesa 3D 图形库的一部分，用于软件渲染。
QMutex: destroying locked mutex 指示存在一个互斥量在其被销毁时仍处于锁定状态的问题。



### 安装qt5.12.5
我尝试安装qt5.12.5来解决这个问题。包括库的缺失、渲染异常。
可以在CoppeliaSim根目录下看出so是qt5.12.5编译的。

在https://download.qt.io/archive/qt/5.12/5.12.5/qt-opensource-linux-x64-5.12.5.run.torrent 下载qt5.12.5的运行文件

添加

    export PATH="/home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/bin:$PATH"
    export QT_PLUGIN_PATH="/home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/plugins"
    export LD_LIBRARY_PATH="/home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib:$LD_LIBRARY_PATH"

执行 `source ~/.bashrc`，执行`qmake --version`查看安装情况

### 再次测试数据生成

还是同样的signal 11报错。

### 检查conda环境

先排查conda的问题，运行`conda list | grep "conda-forge\|<develop>"`查看由conda安装的包

>(manigaussian) (base) quantumxiaol@APL-Laptop:~$ conda list | grep "conda-forge\|<develop>"
ca-certificates           2025.4.26            hbd8a1cb_0    conda-forge
clip                      1.0                       dev_0    <develop>
colorama                  0.4.6              pyhd8ed1ab_1    conda-forge
detectron2                0.6                       dev_0    <develop>
diff-gaussian-rasterization 0.0.0                     dev_0    <develop>
freetype                  2.10.4               h0708190_1    conda-forge
fvcore                    0.1.5.post20221221    pyhd8ed1ab_0    conda-forge
jbig                      2.1               h7f98852_2003    conda-forge
jpeg                      9e                   h0b41bf4_3    conda-forge
lcms2                     2.12                 hddcbb42_0    conda-forge
lerc                      2.2.1                h9c3ff4c_0    conda-forge
libblas                   3.9.0           31_h59b9bed_openblas    conda-forge
libcblas                  3.9.0           31_he106b2a_openblas    conda-forge
libdeflate                1.7                  h7f98852_5    conda-forge
libgcc                    15.1.0               h767d61c_2    conda-forge
libgcc-ng                 15.1.0               h69a702a_2    conda-forge
libgfortran               15.1.0               h69a702a_2    conda-forge
libgfortran5              15.1.0               hcea5267_2    conda-forge
libgomp                   15.1.0               h767d61c_2    conda-forge
liblapack                 3.9.0           31_h7ac8fdf_openblas    conda-forge
libopenblas               0.3.29          pthreads_h94d23a6_0    conda-forge
libpng                    1.6.37               h21135ba_2    conda-forge
libstdcxx                 15.1.0               h8f9b012_2    conda-forge
libtiff                   4.3.0                hf544144_1    conda-forge
libwebp-base              1.5.0                h851e524_0    conda-forge
lz4-c                     1.9.3                h9c3ff4c_1    conda-forge
odise                     0.1                       dev_0    <develop>
olefile                   0.47               pyhd8ed1ab_1    conda-forge
openjpeg                  2.4.0                hb52868f_1    conda-forge
openssl                   3.5.0                h7b32b05_1    conda-forge
portalocker               3.0.0            py39hf3d152e_0    conda-forge
pyrep                     4.1.0.3                   dev_0    <develop>
python_abi                3.9                      2_cp39    conda-forge
pytorch3d                 0.7.8                     dev_0    <develop>
pyyaml                    6.0.2            py39h9399b63_2    conda-forge
rlbench                   1.2.0                     dev_0    <develop>
simple-knn                0.0.0                     dev_0    <develop>
tabulate                  0.9.0              pyhd8ed1ab_2    conda-forge
termcolor                 3.1.0              pyhd8ed1ab_0    conda-forge
tqdm                      4.67.1             pyhd8ed1ab_1    conda-forge
yacs                      0.1.8              pyh29332c3_2    conda-forge
yaml                      0.2.5                h7f98852_2    conda-forge
yarr                      0.1                       dev_0    <develop>
zstd                      1.5.0                ha95c52a_0    conda-forge

不是conda的问题。swrast_dri.so 是一个 DRI（Direct Rendering Infrastructure）驱动，用于在没有合适的硬件加速支持时，提供基于软件的 OpenGL 渲染功能。

### 检查OpenGL支持

运行`glxinfo | grep "OpenGL"`查看当前系统的 OpenGL 信息

>OpenGL vendor string: Microsoft Corporation
OpenGL renderer string: D3D12 (NVIDIA GeForce RTX 4080 Laptop GPU)
OpenGL core profile version string: 4.2 (Core Profile) Mesa 23.2.1-1ubuntu3.1~22.04.3
OpenGL core profile shading language version string: 4.20
OpenGL core profile context flags: (none)
OpenGL core profile profile mask: core profile
OpenGL core profile extensions:
OpenGL version string: 4.2 (Compatibility Profile) Mesa 23.2.1-1ubuntu3.1~22.04.3
OpenGL shading language version string: 4.20
OpenGL context flags: (none)
OpenGL profile mask: compatibility profile
OpenGL extensions:
OpenGL ES profile version string: OpenGL ES 3.1 Mesa 23.2.1-1ubuntu3.1~22.04.3
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.10
OpenGL ES profile extensions:

### 检查libcoppeliaSim的依赖

执行`ldd /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1` 检测链接到了哪些共享库

>quantumxiaol@APL-Laptop:~$ ldd /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1
        linux-vdso.so.1 (0x00007fffd459c000)
        liblua5.1.so => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/liblua5.1.so (0x00007f7f81a00000)
        libQt5OpenGL.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5OpenGL.so.5 (0x00007f7f81600000)
        libQt5Widgets.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5Widgets.so.5 (0x00007f7f80c00000)
        libQt5Gui.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5Gui.so.5 (0x00007f7f80200000)
        libQt5Network.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5Network.so.5 (0x00007f7f7fe00000)
        libQt5SerialPort.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5SerialPort.so.5 (0x00007f7f7fa00000)
        libQt5Core.so.5 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libQt5Core.so.5 (0x00007f7f7f200000)
        libGL.so.1 => /lib/x86_64-linux-gnu/libGL.so.1 (0x00007f7f82b4c000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f7f82b47000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f7f7ee00000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f7f82a5e000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f7f81be0000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7f7ea00000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f7f81bc4000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f7f81bbf000)
        libicui18n.so.56 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libicui18n.so.56 (0x00007f7f7e400000)
        libicuuc.so.56 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libicuuc.so.56 (0x00007f7f7e000000)
        libicudata.so.56 => /home/quantumxiaol/Qt5.12.5/5.12.5/gcc_64/lib/libicudata.so.56 (0x00007f7f7c600000)
        libgthread-2.0.so.0 => /lib/x86_64-linux-gnu/libgthread-2.0.so.0 (0x00007f7f81bb8000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007f7f818c6000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f7f82be0000)
        libGLdispatch.so.0 => /lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x00007f7f81548000)
        libGLX.so.0 => /lib/x86_64-linux-gnu/libGLX.so.0 (0x00007f7f81b82000)
        libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f7f814d2000)
        libX11.so.6 => /lib/x86_64-linux-gnu/libX11.so.6 (0x00007f7f80ac0000)
        libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007f7f81b58000)
        libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007f7f81b52000)
        libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007f7f81b48000)
        libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007f7f81b30000)
        libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007f7f818b9000)

Qt5OpenGL 是一个封装 OpenGL 的模块，如果它编译时链接的是 Mesa 的 GL，则会绕过 NVIDIA 的 GL 实现。Qt5 对 WSLg 的支持不如 Qt6 成熟。

### 检查swrast

运行`strace -f -e openat python /home/quantumxiaol/fix_demo.py 2>&1 | grep 'swrast'`追踪是谁调用了swrast

>[pid 15363] openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/dri/tls/swrast_dri.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
[pid 15363] openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so", O_RDONLY|O_CLOEXEC) = 8
/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so(+0xc25f7d)[0x77896d625f7d]

仍在试图使用 Mesa 的软件渲染库而不是 NVIDIA 的 OpenGL 实现

export GALLIUM_DRIVER=d3d12
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

### 指定Linux使用nvidia（未成功）

`sudo nano /usr/share/glvnd/egl_vendor.d/10_nvidia.json`创建
接着，在 nano 编辑器中输入内容：

    {
        "file_format_version": "1.0.0",
        "ICD": {
            "library_path": "libGLX_nvidia.so.0"
        }
    }

### 定位问题
~问题出在fix_demo.py的descriptions, obs = task.reset()。~
问题的核心出在swrast_dri.so 、signal 11 (SIGSEGV)、Segmentation fault上


https://yipko.com/posts/work/coppeliasim-rlbench-troubleshooting-guide/ 提出了解决方案

    报错 “Error: signal 11: /lib/x86_64-linux-gnu/libc.so.6或/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so” 等

    原因： conda等虚拟环境默认使用自带的gcc/g++库，它们版本过低，而系统中的swrast_dri.so等需要高版本gcc/g++库的高版本ABI支持。

    解决办法：

    法1: 手动将系统中的库加入LD_PRELOAD
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libc.so.6
    bash
    法2: conda安装高版本gcc/g++
    conda install conda-forge::libstdcxx-ng
    # if installing libstdcxx-ng not work
    # conda install gcc
    bash
    参考文档： https://github.com/huangwl18/VoxPoser/issues/1#issuecomment-2664404719

输入`conda list libstdcxx-ng`查看libstdcxx-ng的版本
>Name                    Version                   Build  Channel
libstdcxx-ng              11.2.0               h1234567_1  

输入`conda list gcc`查看gcc版本

>Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
libgcc                    15.1.0               h767d61c_2    conda-forge
libgcc-ng                 15.1.0               h69a702a_2    conda-forge

#### 查看链接库的版本
find $CONDA_PREFIX -name "libstdc++.so*"
/home/quantumxiaol/anaconda3/envs/manigaussian/lib/libstdc++.so.6.0.34

ls -l /lib/x86_64-linux-gnu/libstdc++.so.6
lrwxrwxrwx 1 root root 19 May 13  2023 /lib/x86_64-linux-gnu/libstdc++.so.6 -> libstdc++.so.6.0.30

#### 安装libgl1-mesa-dev
运行`dpkg -l | grep libgl1-mesa-dev` 查看是否有libgl1-mesa-dev
没有运行`sudo apt install libgl1-mesa-dev`安装libgl1-mesa-dev

>ii  libgl1-mesa-dev:amd64           23.2.1-1ubuntu3.1~22.04.3               amd64        transitional dummy package

#### 检查缺失库
运行`bash /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libLoadErrorCheck.sh`

>linux-vdso.so.1 (0x00007fff8b9d0000)
/usr/lib/x86_64-linux-gnu/libc.so.6 (0x00007de3b9200000)
liblua5.1.so => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/liblua5.1.so (0x00007de3b9000000)
libQt5OpenGL.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5OpenGL.so.5 (0x00007de3b8c00000)
libQt5Widgets.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Widgets.so.5 (0x00007de3b8200000)
libQt5Gui.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5 (0x00007de3b7800000)
libQt5Network.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Network.so.5 (0x00007de3b7400000)
libQt5SerialPort.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5SerialPort.so.5 (0x00007de3b7000000)
libQt5Core.so.5 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Core.so.5 (0x00007de3b6800000)
libGL.so.1 => /lib/x86_64-linux-gnu/libGL.so.1 (0x00007de3ba4ea000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007de3ba4e5000)
libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007de3b6400000)
libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007de3b9519000)
libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007de3ba4c3000)
/lib64/ld-linux-x86-64.so.2 (0x00007de3ba57e000)
libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007de3ba4a7000)
libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007de3ba4a2000)
libicui18n.so.56 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libicui18n.so.56 (0x00007de3b5e00000)
libicuuc.so.56 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libicuuc.so.56 (0x00007de3b5a00000)
libicudata.so.56 => /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libicudata.so.56 (0x00007de3b4000000)
libgthread-2.0.so.0 => /lib/x86_64-linux-gnu/libgthread-2.0.so.0 (0x00007de3ba49b000)
libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007de3b8ec6000)
libGLdispatch.so.0 => /lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x00007de3b9461000)
libGLX.so.0 => /lib/x86_64-linux-gnu/libGLX.so.0 (0x00007de3ba465000)
libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007de3b918a000)
libX11.so.6 => /lib/x86_64-linux-gnu/libX11.so.6 (0x00007de3b8ac0000)
libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007de3b9437000)
libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007de3ba45d000)
libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007de3b942f000)
libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007de3b9172000)
libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007de3b9165000)

表明 CoppeliaSim 并没有使用 Conda 中的 C++ 标准库，而是直接使用了 WSL2 系统中的版本。

#### 检查swrast_dri.so依赖项
运行`ldd /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so`

>linux-vdso.so.1 (0x00007fff5c7ad000)
libglapi.so.0 => /lib/x86_64-linux-gnu/libglapi.so.0 (0x00007ad721695000)
libdrm.so.2 => /lib/x86_64-linux-gnu/libdrm.so.2 (0x00007ad72167f000)
libLLVM-15.so.1 => /lib/x86_64-linux-gnu/libLLVM-15.so.1 (0x00007ad718400000)
libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007ad72164e000)
libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007ad721632000)
libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007ad721561000)
libsensors.so.5 => /lib/x86_64-linux-gnu/libsensors.so.5 (0x00007ad721551000)
libdrm_radeon.so.1 => /lib/x86_64-linux-gnu/libdrm_radeon.so.1 (0x00007ad721542000)
libelf.so.1 => /lib/x86_64-linux-gnu/libelf.so.1 (0x00007ad721524000)
libdrm_amdgpu.so.1 => /lib/x86_64-linux-gnu/libdrm_amdgpu.so.1 (0x00007ad721518000)
libdrm_nouveau.so.2 => /lib/x86_64-linux-gnu/libdrm_nouveau.so.2 (0x00007ad72150d000)
libdrm_intel.so.1 => /lib/x86_64-linux-gnu/libdrm_intel.so.1 (0x00007ad7214e5000)
libxcb-dri3.so.0 => /lib/x86_64-linux-gnu/libxcb-dri3.so.0 (0x00007ad7214de000)
libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007ad718000000)
libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007ad718319000)
libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007ad7182f9000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ad717c00000)
libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007ad71f3f3000)
libedit.so.2 => /lib/x86_64-linux-gnu/libedit.so.2 (0x00007ad7182bf000)
libtinfo.so.6 => /lib/x86_64-linux-gnu/libtinfo.so.6 (0x00007ad71828d000)
libxml2.so.2 => /lib/x86_64-linux-gnu/libxml2.so.2 (0x00007ad717a1e000)
/lib64/ld-linux-x86-64.so.2 (0x00007ad7216d5000)
libpciaccess.so.0 => /lib/x86_64-linux-gnu/libpciaccess.so.0 (0x00007ad718282000)
libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007ad718256000)
libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007ad71823e000)
libicuuc.so.70 => /lib/x86_64-linux-gnu/libicuuc.so.70 (0x00007ad717823000)
liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007ad717fd5000)
libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007ad718238000)
libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007ad71822e000)
libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007ad717fc8000)
libicudata.so.70 => /lib/x86_64-linux-gnu/libicudata.so.70 (0x00007ad715c00000)

#### 检查兼容性
运行`strings /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so | grep 'CXXABI'`

>CXXABI_1.3.8
CXXABI_1.3
CXXABI_1.3.9

运行`strings /usr/lib/x86_64-linux-gnu/libstdc++.so.6 | grep 'CXXABI'`

>CXXABI_1.3
CXXABI_1.3.1
CXXABI_1.3.2
CXXABI_1.3.3
CXXABI_1.3.4
CXXABI_1.3.5
CXXABI_1.3.6
CXXABI_1.3.7
CXXABI_1.3.8
CXXABI_1.3.9
CXXABI_1.3.10
CXXABI_1.3.11
CXXABI_1.3.12
CXXABI_1.3.13
CXXABI_TM_1
CXXABI_FLOAT128

从 ABI 兼容性的角度来看，不应该存在因为缺少所需的 CXXABI 版本而导致的问题。

`strings /home/quantumxiaol/anaconda3/envs/manigaussian/lib/libstdc++.so.6.0.34 | grep 'CXXABI'`

>CXXABI_1.3
CXXABI_1.3.1
CXXABI_1.3.2
CXXABI_1.3.3
CXXABI_1.3.4
CXXABI_1.3.5
CXXABI_1.3.6
CXXABI_1.3.7
CXXABI_1.3.8
CXXABI_1.3.9
CXXABI_1.3.10
CXXABI_1.3.11
CXXABI_1.3.12
CXXABI_1.3.13
CXXABI_1.3.14
CXXABI_1.3.15
CXXABI_TM_1
CXXABI_FLOAT128
CXXABI_1.3
CXXABI_1.3.15
CXXABI_1.3.11
CXXABI_1.3.2
CXXABI_1.3.6
CXXABI_FLOAT128
CXXABI_1.3.12
CXXABI_1.3.9
CXXABI_1.3.1
CXXABI_1.3.5
CXXABI_1.3.8
CXXABI_1.3.13
CXXABI_1.3.4
CXXABI_TM_1
CXXABI_1.3.7
CXXABI_1.3.14
CXXABI_1.3.10
CXXABI_1.3.3

#### 检查pyrep
运行`python ManiGaussian/third_party/PyRep/examples/example_reinforcement_learning_env.py`

>.......
Episode 4, step 193, reward: -0.625269
Episode 4, step 194, reward: -0.629068
Episode 4, step 195, reward: -0.629263
Episode 4, step 196, reward: -0.631026
Episode 4, step 197, reward: -0.636068
Episode 4, step 198, reward: -0.628632
Episode 4, step 199, reward: -0.621436
Done!
[CoppeliaSim:loadinfo]   done.
Segmentation fault (core dumped)

可以正常执行，显示运动。

#### 检查RLBench
运行`python /home/quantumxiaol/ManiGaussian/third_party/RLBench/examples/single_task_rl.py`

    # single_task_rl.py
    import numpy as np
    from rlbench.action_modes.action_mode import MoveArmThenGripper
    from rlbench.action_modes.arm_action_modes import JointVelocity
    from rlbench.action_modes.gripper_action_modes import Discrete
    from rlbench.environment import Environment
    from rlbench.observation_config import ObservationConfig
    from rlbench.tasks import ReachTarget


    class Agent(object):

        def __init__(self, action_shape):
            self.action_shape = action_shape

        def act(self, obs):
            arm = np.random.normal(0.0, 0.1, size=(self.action_shape[0] - 1,))
            gripper = [1.0]  # Always open
            return np.concatenate([arm, gripper], axis=-1)


    env = Environment(
        action_mode=MoveArmThenGripper(
            arm_action_mode=JointVelocity(), gripper_action_mode=Discrete()),
        obs_config=ObservationConfig(),
        headless=False)
    env.launch()

    task = env.get_task(ReachTarget)

    agent = Agent(env.action_shape)

    training_steps = 120
    episode_length = 40
    obs = None
    for i in range(training_steps):
        if i % episode_length == 0:
            print('Reset Episode')
            descriptions, obs = task.reset()
            print(descriptions)
        action = agent.act(obs)
        print(action)
        obs, reward, terminate = task.step(action)

    print('Done')
    env.shutdown()


>Reset Episode
Error: signal 11:
/home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_Z11_segHandleri+0x30)[0x758306d0aae0]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x758359042520]
/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so(+0xc25f7d)[0x7582e9a25f7d]
QMutex: destroying locked mutex

看来问题出在RLBench上。我在https://github.com/stepjam/RLBench/issues/170 找到了一样的问题，但是没有解决。也是Pyrep和CoppeliaSim都可以运行，但是RLBench不可以。

https://github.com/stepjam/RLBench/issues/146 也有类似的问题。

使用gdb调试

>(gdb) run
Starting program: /home/quantumxiaol/anaconda3/envs/manigaussian/bin/python ./ManiGaussian/third_party/RLBench/examples/single_task_rl.py
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff47ff640 (LWP 5521)]
[New Thread 0x7ffff3ffe640 (LWP 5522)]
[New Thread 0x7fffef7fd640 (LWP 5523)]
[New Thread 0x7fffecffc640 (LWP 5524)]
[New Thread 0x7fffea7fb640 (LWP 5525)]
[New Thread 0x7fffe7ffa640 (LWP 5526)]
[New Thread 0x7fffe57f9640 (LWP 5527)]
[New Thread 0x7fffe4ff8640 (LWP 5528)]
[New Thread 0x7fffe07f7640 (LWP 5529)]
[New Thread 0x7fffdfff6640 (LWP 5530)]
[New Thread 0x7fffdb7f5640 (LWP 5531)]
[New Thread 0x7fffdaff4640 (LWP 5532)]
[New Thread 0x7fffd67f3640 (LWP 5533)]
[New Thread 0x7fffd3ff2640 (LWP 5534)]
[New Thread 0x7fffd17f1640 (LWP 5535)]
[New Thread 0x7fffceff0640 (LWP 5536)]
[New Thread 0x7fffcc7ef640 (LWP 5537)]
[New Thread 0x7fffc9fee640 (LWP 5538)]
[New Thread 0x7fffc77ed640 (LWP 5539)]
[New Thread 0x7fffc6fec640 (LWP 5540)]
[New Thread 0x7fffc27eb640 (LWP 5541)]
[New Thread 0x7fffc1fea640 (LWP 5542)]
[New Thread 0x7fffbf7e9640 (LWP 5543)]
[New Thread 0x7fffbcfe8640 (LWP 5544)]
[New Thread 0x7fffba7e7640 (LWP 5545)]
[New Thread 0x7fffb7fe6640 (LWP 5546)]
[New Thread 0x7fffb57e5640 (LWP 5547)]
[New Thread 0x7fffb0fe4640 (LWP 5548)]
[New Thread 0x7fffae7e3640 (LWP 5549)]
[New Thread 0x7fffabfe2640 (LWP 5550)]
[New Thread 0x7fffa97e1640 (LWP 5551)]
[New Thread 0x7fff9fdff640 (LWP 5552)]
[New Thread 0x7fff9e7d3640 (LWP 5553)]
[Detaching after vfork from child process 5570]
[New Thread 0x7fff7b5a4640 (LWP 5572)]
[New Thread 0x7fff7a9a3640 (LWP 5578)]
[New Thread 0x7fff7a1a2640 (LWP 5579)]
[New Thread 0x7fff799a1640 (LWP 5580)]
[New Thread 0x7fff791a0640 (LWP 5581)]
[New Thread 0x7fff63bff640 (LWP 5582)]
[New Thread 0x7fff633fe640 (LWP 5604)]
[New Thread 0x7fff4fbff640 (LWP 5628)]
Reset Episode
[New Thread 0x7fff4497a640 (LWP 5636)]
Thread 33 "python" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fff9fdff640 (LWP 5552)]
0x00007fff88625f7d in ?? () from /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so
(gdb) bt full
#0  0x00007fff88625f7d in ?? () from /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so
No symbol table info available.
#1  0x0000000000000000 in ?? ()
No symbol table info available.
(gdb) quit
A debugging session is active.
        Inferior 1 [process 5518] will be killed.
Quit anyway? (y or n) y

使用sudo apt install valgrind检查

运行`valgrind --track-origins=yes python /home/quantumxiaol/ManiGaussian/third_party/RLBench/examples/single_task_rl.py`

>==8414== Invalid write of size 4
==8414==    at 0x79839970: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7983A3C8: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798389F2: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798EF208: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D7C8C: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D85CF: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B977169: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x77D108EB: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77D4EA74: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77C473E8: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x6C0F301A: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==    by 0x6C0F4E17: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==  Address 0x7f2a8ea165ac is not stack'd, malloc'd or (recently) free'd
==8414== 
==8414== Invalid write of size 4
==8414==    at 0x79839978: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7983A3C8: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798389F2: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798EF208: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D7C8C: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D85CF: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B977169: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x77D108EB: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77D4EA74: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77C473E8: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x6C0F301A: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==    by 0x6C0F4E17: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==  Address 0x7f2a8ea165b0 is not stack'd, malloc'd or (recently) free'd
==8414== 
==8414== Invalid write of size 4
==8414==    at 0x7983996A: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7983A3FD: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798389F2: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x798EF208: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D7C8C: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B0D85CF: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x7B977169: ??? (in /usr/lib/wsl/drivers/nvtfi.inf_amd64_60d774447fb9f1f6/libnvwgf2umx.so)
==8414==    by 0x77D108EB: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77D4EA74: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x77C473E8: ??? (in /usr/lib/wsl/lib/libd3d12core.so)
==8414==    by 0x6C0F301A: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==    by 0x6C0F4E17: ??? (in /usr/lib/wsl/lib/libd3d12.so)
==8414==  Address 0x7f2a8ea165b4 is not stack'd, malloc'd or (recently) free'd
==8414== 
==8414== 
==8414== More than 1000 different errors detected.  I'm not reporting any more.
==8414== Final error counts will be inaccurate.  Go fix your program!
==8414== Rerun with --error-limit=no to disable this cutoff.  Note
==8414== that errors may occur in your program without prior warning from
==8414== Valgrind, because errors are no longer being displayed.
==8414== 
Reset Episode
==8414== 
==8414== Process terminating with default action of signal 11 (SIGSEGV)
==8414==  Access not within mapped region at address 0x1102
==8414==    at 0x57DD132: x86_64_fallback_frame_state (md-unwind-support.h:57)
==8414==    by 0x57DD132: uw_frame_state_for (unwind-dw2.c:1016)
==8414==    by 0x57DE4C7: _Unwind_Backtrace (unwind.inc:303)
==8414==    by 0x4A8FBB2: backtrace (backtrace.c:78)
==8414==    by 0x5A191ADF: _segHandler(int) (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==8414==    by 0x499E51F: ??? (in /usr/lib/x86_64-linux-gnu/libc.so.6)
==8414==    by 0x6F436F7C: ??? (in /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so)
==8414==    by 0x1101: ???
==8414==    by 0x991A468F: ???
==8414==  If you believe this happened as a result of a stack
==8414==  overflow in your program's main thread (unlikely but
==8414==  possible), you can try to increase the size of the
==8414==  main thread stack using the --main-stacksize= flag.
==8414==  The main thread stack size used in this run was 8388608.
==8414== 
==8414== HEAP SUMMARY:
==8414==     in use at exit: 142,930,379 bytes in 231,686 blocks
==8414==   total heap usage: 4,359,130 allocs, 4,127,444 frees, 622,318,926 bytes allocated
==8414== 
==8414== LEAK SUMMARY:
==8414==    definitely lost: 69,888 bytes in 316 blocks
==8414==    indirectly lost: 32 bytes in 1 blocks
==8414==      possibly lost: 28,393,465 bytes in 17,101 blocks
==8414==    still reachable: 114,464,978 bytes in 214,247 blocks
==8414==                       of which reachable via heuristic:
==8414==                         stdstring          : 45,209 bytes in 1,064 blocks
==8414==                         newarray           : 113,496 bytes in 123 blocks
==8414==                         multipleinheritance: 423,864 bytes in 246 blocks
==8414==         suppressed: 0 bytes in 0 blocks
==8414== Rerun with --leak-check=full to see details of leaked memory
==8414== 
==8414== For lists of detected and suppressed errors, rerun with: -s
==8414== ERROR SUMMARY: 35923 errors from 1000 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)

这些泄漏主要集中在 libsimExtDynamicsBullet-2-83.so 和 libcoppeliaSim.so 库中，特别是在动态分配内存的地方。
最终导致了段错误（Segmentation fault），这通常意味着程序试图访问未分配或已释放的内存区域。
从堆栈跟踪来看，段错误发生在 CWorld::_simulationAboutToStart() 或其附近的调用链中。

运行`valgrind --leak-check=full --track-origins=yes python /home/quantumxiaol/ManiGaussian/third_party/RLBench/examples/single_task_rl.py > valgrind_output.log 2>&1`

>==16099==    by 0x6F3C602D: ??? (in /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so)
==16099==    by 0x6F3C7692: ??? (in /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so)
==16099== 
==16099== 3,342,359 bytes in 1 blocks are possibly lost in loss record 72,756 of 72,760
==16099==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==16099==    by 0x6CDB79F7: btAlignedAllocDefault(unsigned long, int) (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libsimExtDynamicsBullet-2-83.so)
==16099==    by 0x6CD555B8: btDefaultCollisionConfiguration::btDefaultCollisionConfiguration(btDefaultCollisionConstructionInfo const&) (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libsimExtDynamicsBullet-2-83.so)
==16099==    by 0x6CCEDD0B: CRigidBodyContainerDyn_bullet283::CRigidBodyContainerDyn_bullet283() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libsimExtDynamicsBullet-2-83.so)
==16099==    by 0x6CCDE314: dynPlugin_startSimulation (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libsimExtDynamicsBullet-2-83.so)
==16099==    by 0x5A35B3D5: CPluginContainer::dyn_startSimulation(int, int, float const*, int const*) (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5A0F3A5E: CDynamicsContainer::addWorldIfNotThere() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5A0B903F: CWorld::_simulationAboutToStart() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5A0BA607: CWorld::simulationAboutToStart() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5A0CC4CF: CSimulation::startOrResumeSimulation() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5A1BDD3E: simStartSimulation_internal() (in /home/quantumxiaol/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so)
==16099==    by 0x5777901E: _cffi_f_simStartSimulation (in /home/quantumxiaol/ManiGaussian/third_party/PyRep/pyrep/backend/_sim_cffi.cpython-39-x86_64-linux-gnu.so)
==16099== 
==16099== LEAK SUMMARY:
==16099==    definitely lost: 69,552 bytes in 315 blocks
==16099==    indirectly lost: 32 bytes in 1 blocks
==16099==      possibly lost: 31,678,171 bytes in 17,908 blocks
==16099==    still reachable: 111,160,380 bytes in 213,486 blocks
==16099==                       of which reachable via heuristic:
==16099==                         stdstring          : 45,209 bytes in 1,064 blocks
==16099==                         newarray           : 112,976 bytes in 122 blocks
==16099==                         multipleinheritance: 419,156 bytes in 198 blocks
==16099==         suppressed: 0 bytes in 0 blocks
==16099== Reachable blocks (those to which a pointer was found) are not shown.
==16099== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==16099== 
==16099== For lists of detected and suppressed errors, rerun with: -s
==16099== ERROR SUMMARY: 39611 errors from 4481 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)


CWorld::_simulationAboutToStart()
CSimulation::startOrResumeSimulation()
simStartSimulation_internal()
_cffi_f_simStartSimulation()
这些泄漏的内存大多来自以下库：
swrast_dri.so（Mesa 软件渲染器）
libnvwgf2umx.so（NVIDIA 驱动）
libcoppeliaSim.so 和 libsimExtDynamicsBullet-2-83.so（CoppeliaSim 相关）

似乎与 NVIDIA 驱动程序库 libnvwgf2umx.so 有关

#### 排查WSL和CUDA的问题
https://docs.nvidia.com/cuda/wsl-user-guide/index.html#getting-started-with-cuda-on-wsl-2
列出了WSL尚未解决的问题。

Features Not Yet Supported
The following table lists the set of features that are currently not supported.

|Limitations|Impact|
|  ----  | ----  |
|NVML (nvidia-smi) does not support all the queries yet.|GPU utilization, active compute process are some queries that are not yet supported. Modifiable state features (ECC, Compute mode, Persistence mode) will not be supported.|
|OpenGL-CUDA Interop is not yet supported.|Applications relying on OpenGL will not work.|

RLBench渲染过程使用了opengl，而wsl CUDA尚不支持opengl。

#### 检查MESA
运行`dpkg -l | grep -E 'mesa|libgl|llvm'`检查MESA安装情况

>ii  libegl-mesa0:amd64              23.2.1-1ubuntu3.1~22.04.3               amd64        free implementation of the EGL API -- Mesa vendor library
ii  libgl-dev:amd64                 1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GL development files
ii  libgl1:amd64                    1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- legacy GL support
ii  libgl1-amber-dri:amd64          21.3.9-0ubuntu1~22.04.1                 amd64        free implementation of the OpenGL API -- Amber DRI modules
ii  libgl1-mesa-dev:amd64           23.2.1-1ubuntu3.1~22.04.3               amd64        transitional dummy package
ii  libgl1-mesa-dri:amd64           23.2.1-1ubuntu3.1~22.04.3               amd64        free implementation of the OpenGL API -- DRI modules
ii  libgl1-mesa-glx:amd64           23.0.4-0ubuntu1~22.04.1                 amd64        transitional dummy package
ii  libglapi-mesa:amd64             23.2.1-1ubuntu3.1~22.04.3               amd64        free implementation of the GL API -- shared library
ii  libgles-dev:amd64               1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GLES development files
ii  libgles1:amd64                  1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GLESv1 support
ii  libgles2:amd64                  1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GLESv2 support
ii  libglib2.0-0:amd64              2.72.4-0ubuntu2.4                       amd64        GLib library of C routines
ii  libglib2.0-bin                  2.72.4-0ubuntu2.4                       amd64        Programs for the GLib library
ii  libglib2.0-data                 2.72.4-0ubuntu2.4                       all          Common files for GLib library
ii  libglu1-mesa:amd64              9.0.2-1                                 amd64        Mesa OpenGL utility library (GLU)
ii  libglvnd-core-dev:amd64         1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- core development files
ii  libglvnd-dev:amd64              1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- development files
ii  libglvnd0:amd64                 1.4.0-1                                 amd64        Vendor neutral GL dispatch library
ii  libglx-dev:amd64                1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GLX development files
ii  libglx-mesa0:amd64              23.2.1-1ubuntu3.1~22.04.3               amd64        free implementation of the OpenGL API -- GLX vendor library
ii  libglx0:amd64                   1.4.0-1                                 amd64        Vendor neutral GL dispatch library -- GLX support
ii  libllvm15:amd64                 1:15.0.7-0ubuntu0.22.04.3               amd64        Modular compiler and toolchain technologies, runtime library
ii  mesa-utils                      8.4.0-1ubuntu1                          amd64        Miscellaneous Mesa utilities -- symlinks
ii  mesa-utils-bin:amd64            8.4.0-1ubuntu1                          amd64        Miscellaneous Mesa utilities -- native applications
ii  mesa-va-drivers:amd64           23.2.1-1ubuntu3.1~22.04.3               amd64        Mesa VA-API video acceleration drivers
ii  mesa-vdpau-drivers:amd64        23.2.1-1ubuntu3.1~22.04.3               amd64        Mesa VDPAU video acceleration drivers

这说明在使用 Microsoft 的 Direct3D 12 (D3D12) 驱动，并通过 Mesa 提供 OpenGL 支持。

运行


## 使用Ubuntu安装
### 运行RLBench示例
>(manigaussian) lxl@lxl-Lenovo:~/MG$ python ManiGaussian/third_party/RLBench/examples/single_task_rl.py
Reset Episode
['reach the red target', 'touch the red ball with the panda gripper', 'reach the red sphere']
[-0.09218847  0.15086247 -0.0382969  -0.14304494 -0.00387287 -0.04638115
  0.00897694  1.        ]
Traceback (most recent call last):
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/examples/single_task_rl.py", line 42, in <module>
    obs, reward, terminate = task.step(action)
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/rlbench/task_environment.py", line 99, in step
    self._action_mode.action(self._scene, action)
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/rlbench/action_modes/action_mode.py", line 35, in action
    self.arm_action_mode.action(scene, arm_action, ignore_collisions)
TypeError: action() takes 3 positional arguments but 4 were given
QObject::~QObject: Timers cannot be stopped from another thread
QMutex: destroying locked mutex
Error: signal 11:
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_Z11_segHandleri+0x30)[0x7f46e610aae0]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7f4710c42520]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5(_ZN15QGuiApplication13primaryScreenEv+0x13)[0x7f46e434b463]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5(_ZN7QCursor3posEv+0x9)[0x7f46e4361b49]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_ZN13COpenglWidget38_handleMouseAndKeyboardAndResizeEventsEPvi+0x84b)[0x7f46e65294eb]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1(_ZN13COpenglWidget16_timer100ms_fireEv+0xbf)[0x7f46e652b84f]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Core.so.5(_ZN11QMetaObject8activateEP7QObjectiiPPv+0x659)[0x7f46e349fac9]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Core.so.5(_ZN6QTimer7timeoutENS_14QPrivateSignalE+0x27)[0x7f46e34ac787]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Core.so.5(_ZN6QTimer10timerEventEP11QTimerEvent+0x28)[0x7f46e34aca58]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Core.so.5(_ZN7QObject5eventEP6QEvent+0x7b)[0x7f46e34a09db]

使用gdb检查
> <-Type <RET> for more, q to quit, c to continue without paging--
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from python...
Starting program: /home/lxl/anaconda3/envs/manigaussian/bin/python ManiGaussian/third_party/RLBench/examples/single_task_rl.py
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff3fff640 (LWP 42040)]
[New Thread 0x7ffff37fe640 (LWP 42041)]
[New Thread 0x7ffff0ffd640 (LWP 42042)]
[New Thread 0x7fffee7fc640 (LWP 42043)]
[New Thread 0x7fffe9ffb640 (LWP 42044)]
[New Thread 0x7fffe97fa640 (LWP 42045)]
[New Thread 0x7fffe6ff9640 (LWP 42046)]
[New Thread 0x7fffe47f8640 (LWP 42047)]
[New Thread 0x7fffe1ff7640 (LWP 42048)]
[New Thread 0x7fffdd7f6640 (LWP 42049)]
[New Thread 0x7fffdcff5640 (LWP 42050)]
[New Thread 0x7fffd87f4640 (LWP 42051)]
[New Thread 0x7fffd7ff3640 (LWP 42052)]
[New Thread 0x7fffd37f2640 (LWP 42053)]
[New Thread 0x7fffd0ff1640 (LWP 42054)]
[New Thread 0x7fffc75ff640 (LWP 42055)]
[New Thread 0x7fffc5fd3640 (LWP 42056)]
[New Thread 0x7fffbffff640 (LWP 42057)]
[New Thread 0x7fffbf7fe640 (LWP 42058)]
[New Thread 0x7fffa13ff640 (LWP 42060)]
[New Thread 0x7fff91dff640 (LWP 42063)]
Reset Episode
['reach the red target', 'touch the red ball with the panda gripper', 'reach the red sphere']
[-0.06036199 -0.07500775  0.05743916 -0.02199129  0.01278853  0.10599649
 -0.08668112  1.        ]
Traceback (most recent call last):
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/examples/single_task_rl.py", line 42, in <module>
    obs, reward, terminate = task.step(action)
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/rlbench/task_environment.py", line 99, in step
    self._action_mode.action(self._scene, action)
  File "/home/lxl/MG/ManiGaussian/third_party/RLBench/rlbench/action_modes/action_mode.py", line 35, in action
    self.arm_action_mode.action(scene, arm_action, ignore_collisions)
TypeError: action() takes 3 positional arguments but 4 were given
[Thread 0x7fff91dff640 (LWP 42063) exited]
[Thread 0x7fffa13ff640 (LWP 42060) exited]
QObject::~QObject: Timers cannot be stopped from another thread
QMutex: destroying locked mutex
[Thread 0x7ffff0ffd640 (LWP 42042) exited]
[Thread 0x7fffd0ff1640 (LWP 42054) exited]
[Thread 0x7fffd37f2640 (LWP 42053) exited]
[Thread 0x7fffd7ff3640 (LWP 42052) exited]
[Thread 0x7fffd87f4640 (LWP 42051) exited]
[Thread 0x7fffdcff5640 (LWP 42050) exited]
[Thread 0x7fffdd7f6640 (LWP 42049) exited]
[Thread 0x7fffe1ff7640 (LWP 42048) exited]
[Thread 0x7fffe47f8640 (LWP 42047) exited]
[Thread 0x7fffe6ff9640 (LWP 42046) exited]
[Thread 0x7fffe97fa640 (LWP 42045) exited]
[Thread 0x7fffe9ffb640 (LWP 42044) exited]
[Thread 0x7fffee7fc640 (LWP 42043) exited]
[Thread 0x7ffff37fe640 (LWP 42041) exited]
[Thread 0x7ffff3fff640 (LWP 42040) exited]
Thread 17 "python" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fffc75ff640 (LWP 42055)]
0x00007fffcb34b463 in QGuiApplication::primaryScreen() () from /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5
(gdb) bt full
#0  0x00007fffcb34b463 in QGuiApplication::primaryScreen() ()
   from /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5
No symbol table info available.
#1  0x00007fffcb361b49 in QCursor::pos() ()
   from /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5
No symbol table info available.
#2  0x00007fffcd5294eb in COpenglWidget::_handleMouseAndKeyboardAndResizeEvents(void*, int) () from /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1
No symbol table info available.
#3  0x00007fffcd52b84f in COpenglWidget::_timer100ms_fire() ()
   from /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libcoppeliaSim.so.1
No symbol table info available.
#4  0x00007fffca49fac9 in QMetaObject::activate(QObject*, int, int, void**) ()

CoppeliaSim 在一个定时器回调函数 _timer100ms_fire() 中调用了 GUI 相关的 Qt 函数。
其中调用了 QCursor::pos() 和 QGuiApplication::primaryScreen()。
这些函数试图访问当前屏幕和鼠标状态，但此时可能没有可用的 GUI 上下文（例如无头模式未启用），从而导致段错误。

LD_DEBUG=libs python ManiGaussian/third_party/RLBench/examples/single_task_rl.py > debug_output.log 2>&1

grep 'libQt5Gui' debug_output.log
     42265:	find library=libQt5Gui.so.5 [0]; searching
     42265:	  trying file=/usr/local/cuda/lib64/libQt5Gui.so.5
     42265:	  trying file=glibc-hwcaps/x86-64-v3/libQt5Gui.so.5
     42265:	  trying file=glibc-hwcaps/x86-64-v2/libQt5Gui.so.5
     42265:	  trying file=tls/haswell/x86_64/libQt5Gui.so.5
     42265:	  trying file=tls/haswell/libQt5Gui.so.5
     42265:	  trying file=tls/x86_64/libQt5Gui.so.5
     42265:	  trying file=tls/libQt5Gui.so.5
     42265:	  trying file=haswell/x86_64/libQt5Gui.so.5
     42265:	  trying file=haswell/libQt5Gui.so.5
     42265:	  trying file=x86_64/libQt5Gui.so.5
     42265:	  trying file=libQt5Gui.so.5
     42265:	  trying file=/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5
     42265:	calling init: /home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5(_ZN15QGuiApplication13primaryScreenEv+0x13)[0x7fe07d74b463]
/home/lxl/MG/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04/libQt5Gui.so.5(_ZN7QCursor3posEv+0x9)[0x7fe07d761b49]


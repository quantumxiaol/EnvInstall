# ManiGaussian环境安装
ManiGaussian 是多智能体协作的项目，使用pyrep与vrep交互，模拟环境

安装过程见
https://github.com/GuanxingLu/ManiGaussian/blob/main/docs/INSTALL.md

作者自己在搞docker，但很显然他目前还没有成功，这个环境确实复杂，他们在Ubuntu上就行了尝试

# 总结
不要在Windows上安装，PyRep4.0.2应该只能在Linux上运行。

虚拟环境名称需要manigaussian，后续的测试训练脚本是硬编码的。

安装YARR需要降级pip版本到24，这个版本对依赖比较宽容。

安装odise需要降级setuptools版本到小于60。

安装 lightning会自动下最新的，从而顶掉torch变成cpu版本，需要指定lightning版本为2.2.1。

特别注意不要使用conda安装torch，后面安装包有的会自动用pip修改torch，导致出现包对不上的问题。

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

clone代码库
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

安装CLIP

>Obtaining file:///home/quantumxiaol/CLIP
  Preparing metadata (setup.py) ... done
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/ftfy/
Collecting ftfy (from clip==1.0)
  Downloading ftfy-6.3.1-py3-none-any.whl.metadata (7.3 kB)
INFO: pip is looking at multiple versions of clip to determine which version is compatible with other requirements. This could take a while.
ERROR: Could not find a version that satisfies the requirement packaging (from clip) (from versions: none)
ERROR: No matching distribution found for packaging

安装open-clip-torch

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

安装YARR

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

安装odise
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


安装submodules/diff-gaussian-rasterization

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

[环境](./ManiGaussianEnvList.md)



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


# Install on WSL
#### [WSL installation](../WSL/readme.md)
安装WSL2，我使用了22.04，从coppeliarobotics来看，4.1.0支持ubuntu16.04、18.04、20.04；CUDA使用了11.7。
#### 0 clone the repo and create env

    git clone https://github.com/GuanxingLu/ManiGaussian.git

    # [Optional] We have wrapped (modified) third party packages into this repo, so it might be oversized. To address this, run:
    # git config --global http.postBuffer 104857600 

    conda remove -n manigaussian --all
    conda create -n manigaussian python=3.9
    conda activate manigaussian

#### Install pytorch

    ~conda install pytorch==1.10.0 torchvision torchaudio cudatoolkit=11.3 -c pytorch~
    pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113


#### install pytorch3d
    cd ..
    git clone https://github.com/facebookresearch/pytorch3d.git
    cd pytorch3d
    conda install -c fvcore -c iopath -c conda-forge fvcore iopath
    pip install -e .
    cd ../ManiGaussian

#### install CLIP
    cd ..
    git clone https://github.com/openai/CLIP.git
    cd CLIP
    pip install -e .
    cd ../ManiGaussian
    pip install open-clip-torch

#### download coppeliasim and add path to env
Download CoppeliaSim from https://www.coppeliarobotics.com/previousVersions,currently only edu version on 4.1.0 is available.

    wget https://downloads.coppeliarobotics.com/V4_1_0/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04.tar.xz
    tar -xf CoppeliaSim_Edu_V4_1_0_Ubuntu20_04.tar.xz
    rm CoppeliaSim_Player_V4_1_0_Ubuntu18_04.tar.xz
add path to bashrc

    vim ~/.bashrc
    export COPPELIASIM_ROOT=EDIT/ME/PATH/TO/COPPELIASIM/INSTALL/DIR
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$COPPELIASIM_ROOT
    export QT_QPA_PLATFORM_PLUGIN_PATH=$COPPELIASIM_ROOT

source your bashrc `source ~/.bashrc`

#### install PyRep
    cd third_party/PyRep
    pip install -r requirements.txt
    pip install .
    cd ../..

#### install RLBench
    cd third_party/RLBench
    pip install -r requirements.txt
    python setup.py develop
    cd ../..

#### install YARR

    cd third_party/YARR
    pip install -r requirements.txt
    python setup.py develop
    cd ../..

#### install ManiGaussian requirements
    pip install "pip<24.1"
    pip install -r requirements.txt

#### install other utility packages
    pip install packaging==21.3 dotmap pyhocon wandb==0.14.0 chardet opencv-python-headless gpustat ipdb visdom sentencepiece

### install odise
    pip install "setuptools<59"
Install xformers (this version is a must to avoid errors from detectron2)

    pip install xformers==0.0.18 
Install detectron2:

    cd ..
    git clone https://github.com/facebookresearch/detectron2.git
    cd detectron2
    pip install -e .
    cd ../ManiGaussian
Install ODISE packages

    cd third_party/ODISE
    pip install -e .
    cd ../..

#### fix some possible problems
Since a lot of packages are installed, there are some possible bugs. Use these commands first before running the code.

    ~conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.7 -c pytorch -c nvidia~
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch==2.0.0+cu117 torchvision==0.15.0+cu117 torchaudio==2.0.0 --extra-index-url https://download.pytorch.org/whl/cu117

    pip install hydra-core==1.1
    pip install opencv-python-headless
    pip install numpy==1.23.5
    ~pip install numpy==1.26.4~

#### install Gaussian Splatting Renderer
    cd third_party/gaussian-splatting/
    pip install -e submodules/diff-gaussian-rasterization
    pip install -e submodules/simple-knn
    cd ../..

#### install Lightning Fabric
不指定版本号会下载最新的lightning，这样会自动更新torch到2.4的cpu版本。
    pip install lightning==2.2.1

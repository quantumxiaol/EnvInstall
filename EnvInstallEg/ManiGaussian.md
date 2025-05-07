ManiGaussian 是多智能体协作的项目，使用pyrep与vrep交互，模拟环境

安装过程见
https://github.com/GuanxingLu/ManiGaussian/blob/main/docs/INSTALL.md

作者自己在搞docker，但很显然他目前还没有成功，这个环境确实复杂

我在Windows上安装，踩了不少坑，最后也没有成功

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


使用WSL安装

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
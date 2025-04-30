# 遇到的报错
## 1
>command 'Visual Studio\\VC\\Tools\\MSVC\\14.28.29333\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2

cl.exe 返回的退出代码 2 表示编译过程中出现了错误。这通常是由以下原因引起的：

源码中存在语法错误或不兼容的代码；

缺少必要的依赖项或头文件；

编译器版本与源码要求不匹配；

环境变量未正确配置。

可能的原因

C++ 标准不匹配：pytorch3d 的某些模块可能需要支持 C++17 或更高版本的编译器。

CUDA 配置问题：如果 pytorch3d 使用 CUDA 扩展，但 CUDA 工具链未正确安装或配置，可能会导致编译失败。

依赖项版本冲突：例如，torch 的版本与 pytorch3d 不兼容。

路径问题：编译器可能无法找到必要的头文件或库文件。

## 2
>exec(code, locals())
            File "<string>", line 16, in <module>
          ModuleNotFoundError: No module named 'torch'
          [end of output]

找不到torch
但是我明明有，我在setup.py中import torch，print(torch.__version__)
结果解决了（但是报了其他错误，CUDA编译有问题）

是通过构建pyproject.toml解决的。
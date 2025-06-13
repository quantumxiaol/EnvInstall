# Hello World

测试编程语言是否可用，输出Hello World!

- [x]C
- [x]C++
- [x]CUDA
- [x]Python
- [x]Java

`g++ -std=c++11 -fopenmp main.cpp -o main`

配置tasks.json。在VS Code中，按`Ctrl+Shift+P`，然后输入并选择Tasks: Configure Task，选择Create tasks.json file from template，然后选择Others。编辑生成的tasks.json文件，添加如下内容（源文件名为main.cpp）：
`Ctrl+Shift+B` 运行

    {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "build openmp app",
                "type": "shell",
                "command": "g++",
                "args": [
                    "-fopenmp", // 启用OpenMP支持
                    "-o", "${workspaceFolder}/output/main", // 输出可执行文件名
                    "${workspaceFolder}/main.cpp" // 输入源文件
                ],
                "group": {
                    "kind": "build",
                    "isDefault": true
                },
                "problemMatcher": ["$gcc"],
                "detail": "Task to compile a C++ application with OpenMP support."
            }
        ]
    }
# deer-flow

DeerFlow（Deep Exploration and Efficient Research Flow）是一个社区驱动的深度研究框架，它建立在开源社区的杰出工作基础之上。我们的目标是将语言模型与专业工具（如网络搜索、爬虫和 Python 代码执行）相结合，同时回馈使这一切成为可能的社区。

https://github.com/bytedance/deer-flow

# 安装过程

使用uv安装

## 安装uv

    curl -LsSf https://astral.sh/uv/install.sh | sh
    nano ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.bashrc
    uv --version

## 安装npm pnpm

    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    source ~/.bashrc
    nvm --version

    nvm install 22
    npm install -g pnpm
    pnpm --version

## 创建虚拟环境

    cd deer-flow
    # 使用uv.lock
    uv sync
    cd deer-flow/web
    pnpm install

## 运行

    ./bootstrap.sh -d

在浏览器访问 http://127.0.0.1:3000/
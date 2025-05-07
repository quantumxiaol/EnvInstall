# 使用Git
## 设置用户名和邮箱（全局配置）：
    git config --global user.name "你的名字"
    git config --global user.email "你的邮箱地址"

## 克隆仓库
git clone [仓库地址]

深克隆，有时一个仓库会链接另一个仓库

git clone --recurse-submodules [仓库地址]

# 使用GitHub
## 网络代理
有时需要配置Git以使用服务器作为HTTP/HTTPS代理

    git config --global http.proxy 'http://localhost:代理端口号'
    git config --global https.proxy 'http://localhost:代理端口号'

验证代理设置

    git config --global --get http.proxy
    git config --global --get https.proxy

配置错误移除代理

    git config --global --unset http.proxy
    git config --global --unset https.proxy

## 命令
git pull
用于从远程仓库获取最新的更改并将其合并到当前分支。它实际上是两个命令的组合：git fetch（获取远程更新）加上git merge（将这些更新合并到当前分支）。

git push用于将本地仓库中的提交推送到远程仓库。

git merge用于将指定分支的更改合并到当前分支中。

git rebase也是一种整合变更的方法，但它通过将当前分支的更改应用到另一个基础分支之上，而不是创建一个新的合并提交。
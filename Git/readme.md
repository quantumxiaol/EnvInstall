# Git&Github

## 使用Git

### 设置用户名和邮箱（全局配置）：

    git config --global user.name "你的名字"
    git config --global user.email "你的邮箱地址"

### 创建SSH密钥

    ssh-keygen -t rsa -b 4096 -C "你的邮箱地址"

把公钥上传到GitHub中，linux在`~/.ssh/id_rsa.pub`，windows在`C:\Users\用户名\.ssh\id_rsa.pub`中

### 克隆仓库

git clone [仓库地址]

深克隆，有时一个仓库会链接另一个仓库

git clone --recurse-submodules [仓库地址]

## 使用GitHub

当git配置的用户名和邮箱与GitHub的账户一致时，会自动绑定。

### 网络代理

有时需要配置Git以使用服务器作为HTTP/HTTPS代理

    git config --global http.proxy 'http://localhost:代理端口号'
    git config --global https.proxy 'http://localhost:代理端口号'

验证代理设置

    git config --global --get http.proxy
    git config --global --get https.proxy

配置错误移除代理

    git config --global --unset http.proxy
    git config --global --unset https.proxy

## 项目拉取

### 命令

`git pull`
用于从远程仓库获取最新的更改并将其合并到当前分支。它实际上是两个命令的组合：`git fetch`（获取远程更新）加上`git merge`（将这些更新合并到当前分支）。

`git push`用于将本地仓库中的提交推送到远程仓库。

`git merge`用于将指定分支的更改合并到当前分支中。

`git rebase`也是一种整合变更的方法，但它通过将当前分支的更改应用到另一个基础分支之上，而不是创建一个新的合并提交。

保持线性的项目历史
如果希望项目的提交历史尽可能地保持线性（即避免合并提交），可以使用 git rebase。这使得历史记录更加清晰易读。

在同步远程更新时减少冲突
当在一个特性分支上工作，而主分支（如 main 或 master）有了新的更新，可以先将这些更新拉取到本地并进行变基，而不是直接合并。这样做可以让新提交基于最新的代码库进行，从而可能减少未来合并时的冲突。
比如，在准备提交 PR（Pull Request）前，先将目标分支的新变化整合进来。

清理提交历史
在特性分支开发过程中，可能会有多个小的、零散的提交。在最终合并之前，可以通过 git rebase -i（交互式变基）来压缩或整理这些提交，使之更易于理解和维护。这种做法有助于创建更有意义的提交信息，并移除不必要的中间状态。

修复上游问题
如果在特性分支上工作，而基础分支上的某些更改影响了当前工作（比如引入了一个 bug 或者改变了 API），可以通过变基快速重新应用更改，并解决任何出现的问题。

### 冲突处理

冲突通常发生在两个或多个分支对同一文件的同一部分进行了不同的修改，并且尝试将这些分支合并或变基时。Git 无法自动决定应采用哪个版本的更改，因此需要人工介入来解决这种冲突。

如果在不同的分支中只是添加了空行，而这些空行的添加没有导致实际内容在同一位置发生冲突，那么通常情况下 Git 不会产生冲突。

## Git 进阶操作

### 拉取远程更新并保留本地未提交的工作

当在一个新分支上工作并创建了一些新文件但尚未提交，同时远程仓库有了新的更新（比如别人修复了bug），可以按照以下步骤来拉取最新的更改并保留本地未提交的工作：

保存当前工作状态，如果已经对某些文件执行了 git add 但是还没有提交，可以使用 git stash 来保存这些更改。

    git stash push -u
这里的 -u 参数会包含未跟踪的文件（即新文件）到暂存区中一起保存。
切换回主分支并拉取最新更新，然后从远程仓库拉取最新的更改。

    git checkout main
    git pull origin main
切换回的特性分支并合并更改，并将主分支上的更改合并进来。

    git checkout your-feature-branch
    git merge main
如果有冲突，根据提示解决冲突。
恢复之前的工作，使用 `git stash pop` 来恢复之前保存的工作状态（包括新文件和已暂存的更改）。
如果有冲突，Git 会通知你哪些文件存在冲突。需要手动编辑这些文件来解决冲突。

### 分支操作

#### 创建分支

创建一个新分支但不自动切换到该分支：

    git branch <branch-name>
创建并切换到新分支（常用）：

    git checkout -b <branch-name>
或者使用 Git 版本 2.23 及以上推荐的 switch 命令：

    git switch -c <branch-name>

#### 切换分支

切换到已有分支，checkout或者switch：

    git checkout <branch-name>
    git switch <branch-name>

#### 查看分支

列出所有本地分支：

    git branch
列出所有远程和本地分支：

    git branch -a
查看当前分支及其最近提交的信息：

    git branch -v

#### 合并分支

将指定分支合并到当前分支：

    git merge <branch-name>

#### 删除分支

删除本地分支（需先切换出目标分支）：

    git branch -d <branch-name>
如果要强制删除未完全合并的分支：

    git branch -D <branch-name>
删除远程分支：

    git push origin --delete <branch-name>

#### 更新分支信息

从远程更新本地分支列表：

    git fetch
同步远程分支到本地（假设你想让本地分支与远程分支保持一致）：

    git pull origin <branch-name>

#### 重命名分支

重命名当前分支：

    git branch -m <new-branch-name>
重命名指定分支（需要先切换出目标分支）：

    git branch -m <old-branch-name> <new-branch-name>

#### 变基（Rebase）

变基是一种将一个分支上的更改应用到另一个分支之上的方法，它可以用来使提交历史更加线性。

将当前分支变基到目标分支之上：

    git rebase <target-branch>
交互式变基（用于修改、压缩或重新排序提交）：

    git rebase -i HEAD~n
其中 n 表示你想要回顾的最近几次提交的数量。

#### 设置上游分支

克隆了一个仓库后，默认情况下 origin/master 是 master 的上游分支。但是如果创建了一个新的本地分支，可能需要设置它的上游分支以便于推送和拉取操作。

为本地分支设置上游分支：

    git push --set-upstream origin <branch-name>
简写形式：

    git push -u origin <branch-name>

#### 比较分支

比较两个分支之间的差异：

    git diff <branch1>..<branch2>
查看哪个分支包含了某个特定的提交：

    git branch --contains <commit-id>

### 删除远程仓库的关联

    git remote remove origin

接下来不需要与任何远程仓库交互的话（例如推送或拉取更新），只是用来下好执行，可以移除与远程仓库的关联。这不会影响当前本地的工作目录和版本历史记录，但会阻止~菜鸟~意外地将更改推送到远程仓库，~你也不想自己的代码被推到公共仓库吧~。

### http仓库转ssh仓库

运行`git remote -v`查看远程仓库的 URL，然后根据 URL 的前缀来选择使用哪种协议（http 或 ssh）。

运行`git remote set-url origin git@*****.com:****/****.git`

运行`git pull --tags origin main`

配置本机的ssh 配置

    Host git**
        HostName git**
        User git
        IdentityFile ~/.ssh/id_rsa  # 指定你的私钥文件路径

这样把仓库的 URL 更改为 ssh，可以免去输入密码。

### clone别人的仓库

克隆了一个不是自己的 GitHub 仓库，

在本地创建一个分支

    git branch -vv
    git checkout -b feat-my-local

对代码进行修改（只保留在本地）

    git add .
    git commit -m "My local changes"

将来还能从远端拉取更新（如 main 或其他分支的更新）

    git fetch origin
    git checkout main
    git merge origin/main

    git checkout my-local-changes
    git merge main
在保留本地修改的同时，保持与上游仓库同步。

# ManiGaussian环境安装
ManiGaussian 是多智能体协作的项目，使用pyrep与vrep交互，模拟环境

安装过程见
https://github.com/GuanxingLu/ManiGaussian/blob/main/docs/INSTALL.md

作者自己在搞docker，但很显然他目前还没有成功，这个环境确实复杂，他们在Ubuntu上就行了尝试

# 总结
不要在Windows上安装，PyRep4.0.2只能在Linux上运行。尽管coppeliasim可以在Windows上使用。

PyRep需要4.1.0的coppeliasim。

虚拟环境名称需要manigaussian，后续的测试训练脚本是硬编码的。

安装YARR需要降级pip版本到24，这个版本对依赖比较宽容。

安装odise需要降级setuptools版本到小于60。

安装 lightning会自动下最新的，从而顶掉torch变成cpu版本，需要指定lightning版本为2.2.1。

特别注意不要使用conda安装torch，后面安装包有的会自动用pip修改torch，导致出现包对不上的问题。

Windows和WSL都不可用，WSL会有RLBench渲染的错误，Windwos更是不支持PyRep。

# Install on Ubuntu
~~#### [WSL installation](../WSL/readme.md)~~
~~安装WSL2，我使用了22.04，从coppeliarobotics来看，4.1.0支持ubuntu16.04、18.04、20.04；CUDA使用了11.7。~~
#### [Ubuntu installation](../Linux/readme.md)
安装Ubuntu22.04,安装Nvidia驱动，安装CUDA11.7，安装anaconda。
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
    # 补全glm
    cd submodules/diff-gaussian-rasterization/third_party
    git clone https://github.com/g-truc/glm.git
    cd ../../..

    pip install -e submodules/diff-gaussian-rasterization
    pip install -e submodules/simple-knn
    cd ../..

#### install Lightning Fabric
不指定版本号会下载最新的lightning，这样会自动更新torch到2.4的cpu版本。

    pip install lightning==2.2.1
#### install xvfb
sudo apt install -y xvfb

# 测试环境
## 测试coppeliasim
运行`./coppeliaSim.sh`
## 测试PyRep
运行`python ManiGaussian/third_party/PyRep/examples/example_reinforcement_learning_env.py`
## 测试RLBench
运行`python ManiGaussian/third_party/RLBench/examples/single_task_rl.py`
## 测试示例

## 演示
bash scripts/gen_demonstrations_all.sh
## 测试训练脚本
bash scripts/train_and_eval_w_geo_sem_dyna.sh ManiGaussian_BC 0,1 12345 close_jar

# [踩坑记录](./ManiGaussianError.md)
在Windows、WSL、Ubuntu中测试出现的错误。
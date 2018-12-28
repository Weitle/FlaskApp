# 安装
- 操作系统：`CentOS 7`
- 安装 `Anaconda 3`
    - 从中科大镜像网站下载 `anaconda3-5.2`，下载地址：`http://mirrors.ustc.edu.cn/anaconda/archive/Anaconda3-5.2.0-Linux-x86_64.sh`
    - 运行安装命令 `bash Anaconda3-5.2.0-Linux-x86_64.sh`
    - 选择默认安装路径 `/root/anaconda3` 或选择安装路径并将执行路径 `$installdir/anaconda3/bin` 添加到 `PATH` 变量中
    - 查看 `python` 版本：`python -V`，显示结果如下： `Python 3.6.5 :: Anaconda, Inc.`
    - 安装 `Anaconda` 的同时也安装了 `Flask`，查看 `Flask` 版本：`flask --version`，显示结果如下：

        ![flask_version](../public/images/ch1_flaskversion.jpg)
    
    - 为了不同项目之间互相隔离，对不同项目还是使用不同的虚拟环境
- 使用 `Anaconda` 创建本项目使用的虚拟环境（名称为 `flaskapp_1.0`），基于 `Python 3.7` 和 `Flask1.0.2`
    - 运行 `conda create -n flaskapp_1.0 python=3.7`，执行成功后在 `$installdir/anaconda3/envs/` 目录下会生成一个 `flaskapp_1.0` 目录
    - 激活 `flaskapp_1.0` 虚拟环境：`source activate flaskapp_1.0`，进入虚拟环境，此时终端提示符会显示虚拟环境名称
    - 退出虚拟环境：在虚拟环境中运行 `source deactivate` 退出
    - 安装 `flask 1.0.2`：在虚拟环境中运行 `pip install flask==1.0.2`，此时会安装 `Flask 1.0.2` 及其所以来的包
    - 查看虚拟环境下安装的 `flask` 版本：`flask --version`，显示结果如下：

        ![flask_version_virtual](../public/images/ch1_flaskversion_vir.jpg)

    - 可以看出虚拟环境下的 `flask` 是基于 `python 3.7` 的，与操作系统也是隔离的


    
[下一章 程序的基本结构](../Chapter2/note.md)
# 安装
- 操作系统：`CentOS 7`
## 安装 `Anaconda 3`
- 从中科大镜像网站下载 `anaconda3-5.2`，下载地址：`http://mirrors.ustc.edu.cn/anaconda/archive/Anaconda3-5.2.0-Linux-x86_64.sh`
- 运行安装命令 `bash Anaconda3-5.2.0-Linux-x86_64.sh`
- 选择默认安装路径 `/root/anaconda3` 或选择安装路径并将执行路径 `$installdir/anaconda3/bin` 添加到 `PATH` 变量中
- 查看 `python` 版本：`python -V`，显示结果如下： `Python 3.6.5 :: Anaconda, Inc.`
- 安装 `Anaconda` 的同时也安装了 `Flask`，查看 `Flask` 版本：`flask --version`，显示结果如下：

    ![flask_version](../public/images/ch1_flaskversion.jpg)
    
- 为了不同项目之间互相隔离，对不同项目还是使用不同的虚拟环境

## 创建虚拟环境
- 使用 `Anaconda` 创建本项目使用的虚拟环境（名称为 `flaskapp_1.0`），基于 `Python 3.7` 和 `Flask1.0.2`
- 运行 `conda create -n flaskapp_1.0 python=3.7`，执行成功后在 `$installdir/anaconda3/envs/` 目录下会生成一个 `flaskapp_1.0` 目录
- 激活 `flaskapp_1.0` 虚拟环境：`source activate flaskapp_1.0`，进入虚拟环境，此时终端提示符会显示虚拟环境名称
- 退出虚拟环境：在虚拟环境中运行 `source deactivate` 退出
- 安装 `flask 1.0.2`：在虚拟环境中运行 `pip install flask==1.0.2`，此时会安装 `Flask 1.0.2` 及其所以来的包
- 查看虚拟环境下安装的 `flask` 版本：`flask --version`，显示结果如下：

    ![flask_version_virtual](../public/images/ch1_flaskversion_vir.jpg)

- 可以看出虚拟环境下的 `flask` 是基于 `python 3.7` 的，与操作系统也是隔离的

## 安装并使用 MySQL
### 使用 rpm 包安装 mysql-5.7
- 参考[菜鸟教程](http://www.runoob.com/mysql/mysql-install.html)
    - 创建 `mysql` 用户
        - `groupadd mysql`
        - `useradd -g mysql -M -s /sbin/nologin mysql`
    - 下载并安装
        - `wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm`
        - `rpm -ivh mysql-community-release-el7-5.noarch.rpm`
        - `yum update`
        - `yum install mysql-server`
    - 权限设置
        - `chown mysql:mysql -R /var/lib/mysql`
    - 初始化 `MySQL`
        - `mysqld --initialize --user=mysql`
    - 启动 `MySQL`
        - `systemctl start mysqld`
    - 查看 `MySQL` 运行状态
        - `systemctl status mysqld`
    - 设置开机自启动
        - `systemctl enable mysqld`
    - 使用 `root` 用户通过 'MySQL Client' 客户端连接服务器
        - mysql -u root
        - 修改 `root` 用户密码: `set password for 'root'@'localhost'=password('somesecretstring')`
        - 退出后通过 `root` 用户使用密码连接服务器：`mysql -u root -p`
### 通过 python 访问 mysql 数据库
- 在虚拟环境中安装 `PyMySQL` 驱动用于连接服务器
    - `pip install PyMySQL`
- 测试数据库环境搭建
    - 创建数据库 `testdb`
    - 创建一个对该数据库具有全部权限的用户 `testuser` 并设置密码 `test123`
    - 创建数据表 `employee`，包含字段：`first_name`，`last_name`，`age`，`gender`，`income`
- 连接数据库
    ```
        # connect.py
        import pymysql

        # 打开数据库连接
        db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
        # 使用 cursor() 方法创建一个游标对象 
        cursor = db.cursor()
        # 使用 execute() 方法执行查询
        cursor.execute('select version()')
        # 使用 fetchone() 方法获取数据
        data = cursor.fetchone()
        # 输出结果
        print('Database version is: %s.' % data)
        # 关闭数据库连接
        db.close()
    ```
- 创建数据库表
    ```
        # create_table.py
        import pymysql

        db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
        try:
            cursor = db.cursor()
            cursor.execute('drop table if exists employee')
            sql = '''create table if not exists employee(
                        first_name char(20) not null,
                        last_name char(20) not null,
                        age smallint unsigned,
                        gender char(1) default 'M',
                        income float(8, 2) default 0
                    ) ENGINE=InnoDB DEFAULT CHARSET utf8'''
            cursor.execute(sql)
            print('table employee is created.')
        except Exception as e:
            print('Error: ', e)
        finally:
            db.close()
    ```
- 数据库插入操作
    ```
        import pymysql
        db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
        sql = "insert into employee values('Mac', 'Mohan', 20, 'M', 2000)"
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误回滚
            db.rollback()
        else:
            # 没发生错误输出成功信息
            print(u'数据插入成功')
        finally:
            db.close()
    ```
- 数据库查询操作
    - `cursor.fetchone()`：获取单条数据，用于获取下一个查询结果集，结果集是一个对象
    - `cursor.fetchall()`：获取多条数据，用于接收全部的返回结果行
    - `cursor.rowcount`：只读属性，返回执行 `execute()` 方法后影响的行数
    - 查询示例1:：查询并返回工资大于1000的所有数据（使用 `fetchall`）
        ```
            # fetchall.py
            import pymysql

            sql = "select * from employee where income > 1000"
            db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
            except:
                print('Error: unable to fetch data.')
            else:
                for row in results:
                    # 逐条打印结果
                    print("First Name: %s, Last Name: %s, Age: %s, Gender: %s, Income: %s" % (row[0], row[1], row[2], row[3], row[4]))
            finally:
                db.close()
        ```
    - 查询示例2：查询并返回工资大于1000的第一条数据（使用 `fetchone`）
        ```
            # fetchone.py
            import pymysql
            sql = "select * from employee where income > 1000"
            db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                rowcount = cursor.rowcount
                row = cursor.fetchone()
            except:
                print('Error: unable to fetch data.')
            else:
                print('共 %d 条数据' % rowcount)
                print('第一条数据：')
                print("First Name: %s, Last Name: %s, Age: %s, Gender: %s, Income: %s" % (row[0], row[1], row[2], row[3], row[4]))
            finally:
                db.close()
        ```
- 数据库更新操作
    - 更新示例：将 `employee` 表中性别为 `M` 的年龄加1
        ```
            # update.py
            import pymysql
            sql = "update employee set age = age + 1 where gender = 'M'"
            db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                # 提交数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()
                print(u'更新数据失败')
            else:
                # 未发生错误输出成功信息
                print(u'成功更新 %d 条数据' % cursor.rowcount)
            finally:
                db.close()
        ```
- 删除操作
    - 删除操作示例：删除 `employee` 表中 `age` 大于 21 的所有数据
        ```
            # delete.py
            import pymysql
            sql = "delete from employee where age > %d" % (21,)
            db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                # 提交数据库执行
                db.commit()
            except Exception as e:
                # 发生错误时回滚
                db.rollback()
                print(u'删除数据失败')
                print(e)
            else:
                # 未发生错误输出成功信息
                print(u'成功删除 %d 条数据' % cursor.rowcount)
            finally:
                db.close()
        ```
- 执行事务操作
    - 事务机制可以确保数据的一致性
    - 对于支持事务的数据库，`python` 库在游标建立之时自动开启了一个隐形的事务
    - `commit` 方法提交游标的所有操作，`rollback`方法回滚当前游标的所有操作
    - 基本操作结构：
        ```
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        ```
## 安装并使用 MongoDB
- 参考菜鸟教程 [MongoDB - 菜鸟教程](http://www.runoob.com/mongodb/mongodb-tutorial.html)
### Linux 平台安装 MongoDB
- 下载地址：`https://www.mongodb.com/download-center#community`
- 选择版本，下载安装
    - 下载：`wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.0.5.tgz`
    - 解压：`tar -xvzf mongodb-linux-x86_64-rhel70-4.0.5.tgz`
    - 将解压包移动到指定目录：`mv mongodb-linux-x86_64-rhel70-4.0.5 /usr/local/mongodb`
    - 将 `mongodb` 可执行文件添加到 `PATH` 路径中：
        `export PATH=/usr/local/mongodb/bin:$PATH`
- 创建数据库目录
    - `MongoDB` 数据存储在 `data/db` 目录，需要手动创建这个目录 `mkdir -p /var/data/db`
- 运行 `MongoDB` 服务
    - 通过执行 `mongod` 命令来启动 `mongodb` 服务
    - `mongodb` 默认数据库目录是 `/data/db`，可以通过 `--dbpath` 参数指定
    - 后台运行：`mongod --dbpath=/var/data/db --logpath=/var/data/db/log/mongod.log --fork`
- 设置开机自启动
    - 编辑配置文件 `/etc/mongodb.cnf`
        ```
            # mongodb.cnf
            # mongodb 参数说明：
            # --dbpath: 数据库路径（数据文件）
            # --logpath: 日志文件路径
            # --master: 指定为主机器
            # --slave: 指定为从机器
            # --source: 指定主及其的 IP 地址
            # --pologSize: 指定日志文件大小（建议不超过64M）
            # --logappend: 日志文件末尾添加
            # --port: 启用端口
            # --fork: 在后台运行
            # --only: 指定只复制哪一个数据库
            # --auth: 是否需要验证权限登录（使用用户名和密码）
            dbpath=/var/data/db
            logpath=/var/data/db/log/mongod.log
            logappend=true
            port=27017
            fork=true
            bind_ip=0.0.0.0 
        ```
    - 在 `/lib/systemd/system` 目录下新建文件 `mongodb.service`:
        ```
            # /lib/systemd/system/mongodb.service
            [Unit]
            Description=mongodb
            After=network.target remote-fs.target nss-lookup.target

            [Service]
            Type=forking
            ExecStart=/usr/local/mongodb/bin/mongod --config /etc/mongodb.cnf
            ExecReload=/bin/kill -s HUP $MAINPID
            ExecStop=/usr/local/mongodb/bin/mongod --shutdown --config /etc/mongodb.cnf
            PrivateTmp=true

            [Install]
            WantedBy=multi-user.target
        ```
    - 设置权限：`chmod 754 mongodb.service`
    - 启动关闭服务，设置开机自启动
        ```
            # 启动服务
            systemctl start mongodb.service
            # 关闭服务
            systemctl stop mongodb.service
            # 设置开机自启动
            systemctl enable mongodb.service
        ```



[下一章 程序的基本结构](../Chapter2/note.md)
# blog_django
my blog docker version

## 使用说明（在你自己的vps上）
1. 拉取docker

`docker pull friday21/blog:v4`

2. 创建项目  
```
cd /root
mkdir friday
cd friday
git clone https://github.com/Friday21/friday_blog.git
```

3. 使用已有Mysql文件（可选）
把数据库文件放到 /root/friday/data/mysql目录下， 

4. 修改域名  

在 /friday/friday_blog/nginx 目录下修改nginx.conf文件中
的46行， server_name  www.fridayhaohao.com;， 改成自己的域名

5. 启动docker

`docker run -it -v /root/friday:/friday -p 80:80 friday21/blog:v2`

6. 修改mysql目录（可选， 如果做了3，那这部必选）
在启动mysql前指定data目录为 /friday/data/mysql (修改配置文件 /etc/mysql/my.cnf, 添加如下内容)
```
[mysqld]
user            = mysql
pid-file        = /var/run/mysqld/mysqld.pid
port            = 3306
basedir         = /usr
datadir         = /friday/data/mysql
tmpdir          = /tmp
lc-messages-dir = /usr/share/mysql
```

7. 在docker内启动shell
```
sh /friday/friday_blog/docker.sh
```

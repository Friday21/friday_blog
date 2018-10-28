# blog_django
my blog docker version

## 使用说明（在你自己的vps上）
1. 拉取docker

`docker pull friday21/blog:v2`

2. 创建项目  
```
cd /root
mkdir friday
cd friday
git clone https://github.com/Friday21/friday_blog.git
```

3. 修改域名  

在 /friday/friday_blog/nginx 目录下修改nginx.conf文件中
的46行， server_name  www.fridayhaohao.com;， 改成自己的域名

4. 启动docker

`docker run -it -v /root/friday:/friday -p 80:80 friday21/blog:v2`

5. 在docker内启动shell
```
sh /friday/friday_blog/docker.sh
```

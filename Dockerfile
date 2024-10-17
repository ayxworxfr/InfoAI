# 使用官方的 CentOS 7 镜像作为基础镜像
FROM centos:7

# 设置环境变量以避免在安装过程中交互提示
ENV MYSQL_ROOT_PASSWORD=Infoai@517
ENV MYSQL_USER=guet517
ENV MYSQL_PASSWORD=Infoai@517

# 更换为阿里云的 CentOS 7 源
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak && \
    curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
    yum clean all && \
    yum makecache
                 
# 更新系统并安装必要的软件包
RUN yum -y update && \
    yum -y install epel-release && \
    yum -y install wget vim net-tools

# 导入 MySQL GPG 公钥
RUN rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2023

# 安装 MySQL
RUN wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm && \
    rpm -Uvh mysql80-community-release-el7-3.noarch.rpm && \
    yum makecache fast && \   
    yum -y install mysql-server

# 安装 Redis
RUN yum -y install redis

# 创建数据目录并设置权限
RUN mkdir -p /data/docker/mysql /data/docker/redis && \
    chown -R mysql:mysql /data/docker/mysql && \
    chown -R redis:redis /data/docker/redis

# 暴露 MySQL 和 Redis 的端口
EXPOSE 3306 6379

# 启动 MySQL 和 Redis 服务
CMD ["/bin/bash", "-c", "mysqld_safe & redis-server --daemonize no & tail -f /dev/null"]


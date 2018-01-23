Title: 13、Redis 简介、安装和配置
Author: Martin
Date: 2016-03-28 12:35
Summary: 简单介绍下 redis, 及其安装、配置.

[TOC]

# 简介
Redis 是一款 NoSQL(Not Only Sql 非关系型数据库)

- Redis, Remote Directory Server \[远程服务器字典\]
    + 底层 C 语言实现
    + 以字典的结构存储数据
    + 允许通过 TCP 协议读写
    + 内存存储, 但支持持久化
    + 支持排序
    + MQ (队列系统)
    + 发布/订阅模式

# 安装
## 下载
Windows:

```
https://github.com/MSOpenTech/redis/releases
```

注意下载稳定版.

下载好后, 直接解压即可.

另外, 对于 Windows 下, 有一个__桌面化管理工具__: redis-desktop-manager, 也可下载配合使用.

__Redis 命令不区分大小写.__

## redis 生态

- redis.conf: 配置文件(windows 下可能是叫 redis.windows.conf/redis.windows-service.conf)
    + linux
        * 设置 redis.conf 的 __daemonize__ 为 yes (默认为 no), 是否以后台 __Daemon__(守护进程) 方式运行 Redis
            - 如果为 yes, 那么启动 Redis 后, Redis 将做以后台进程的方式一直运行着
            - 如果为 no, 那么 Redis 就是运行在 CMD 上, CMD 一关闭, Redis 就关闭了
    + windows
        * __redis.windows.conf__
            - 同 linux 中把 daemonize 设为 no, 即为独占一个 cmd 的方式运行 redis
        * __redis.windows-service.conf__
            - 同 linux 中把 daemonize 设为 yes, 把 redis 做为 windows 的服务启动
- redis-server: Redis 服务器程序
    + 启动服务: redis-server, 默认的配置文件是使用 redis.conf (__linux__ 下)
    + 指定配置文件启动服务: redis-server redis.windows.conf (__windows__ 下请指定)
    + 这里有可能会报错, 大意是说 maxheap 没定义, 打开 redis.conf 定义下, maxheap 1024000000
- redis-cli: 客户端程序
    + 启动客户端: redis-cli
    + 清空缓存: redis-cli flushdb
    + 关闭服务器: redis-cli -h 127.0.0.1 -p 6379 shutdown
- redis-benchmark: 性能测试工具
- redis-check-aof: AOF 文件修复工具
- redis-check-dump: RDB 文件修复工具

# redis.conf 详解
### 配置 redis 的方法
Redis 服务器的配置, 可以在 redis.conf 设置, 也可以 redis-server 时指定, 还可以 cli 端中动态获取/配置.

config get xxx, 返回双行字符串

- key
- value

config set xxx yyy, 设置 config

### 配置信息
- port 端口, 默认 6379
- bind 绑定主机地址
- timeout 当客户端多久没有操作后关闭连接, 0 代表没有使用这个功能
- requirepass 身份验证, 设置这项后, 客户端连接时需要输入 requirepass 设置的密码
- loglevel 指定日志级别, 有四个级别
    + debug 调试级别, 很详细的信息, 适合开发测试
    + verbos 比 debug 少一些, 但也包含许多无用信息
    + notice 比较适合生产环境
    + warning 只记录警告信息
- logfile 日志记录方式
- database 数据库数量, 默认 16 个(从 0 开始编号, 个人理解就是 mysql 中的表), 通过 select x 可以切换到指定序号的数据库
- 持久化相关
    + save 900 1
    + save 300 10
    + save 60 10000, 这几个选项的意思是 x 秒内有 y 个修改就持久化
    + rdbcompression 持久化时, 是否启用压缩
    + dbfilename 指定执久化的文件名
    + dir 指定执久化文件存放目录
- Hash 相关
    + hash-max-ziplist-value 存储的最大字段数目
    + hash-max-ziplist-entries 每个数目的最大字节
    + 关于这两个选项的意义在 __02、Redis 数据类型__ Hash 章节中有说明


## 命令返回值
- 状态回复
    + PONG
    + OK
- 错误回复
    + error 开头
- 整数回复
    + integer 开头
- 字符串回复
    + 双引号包括
- 多行字符串回复
    + 序号 \+ 单符串

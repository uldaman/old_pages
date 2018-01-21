Title: 01、Mongodb 简介、安装和配置
Author: Martin
Date: 2016-04-08 10:29
Summary: Mongodb 是一款 NoSQL(Not Only Sql 非关系型数据库), 虽然现在有人说它性能不好, 其实只要遵循它的设计原则和要求, 也能实现出高性能的数据库.

[TOC]

## 简介
Mongodb 是一款 NoSQL(Not Only Sql 非关系型数据库), 由 C++ 语言编写而成, 现在网上说 Mongodb 这里不行那里不行的人挺多, 包括性能什么的, 特别是大访问量的时候...

其实 Mongodb 是也是支持大访问量的, 性能也还不错, 很多大型网站也都是使用 Mongodb 做数据库, 但是首先, 你得遵照它的设计原则, 如果不尊重它的原则和要求, 它就会"惩罚"你...

MongoDB 是面向__文档__存储的数据库, 它将传统意义上的数据库视为一个__文档__, 数据结构由__键值对__(key=\>value)对组成.

## 下载
直接去官网下载即可.

另外, 对于 Windows 下, 有一个__桌面化管理工具__: [Robomongo 64位](https://yunpan.cn/cqXnDqkxqwSCX), 访问密码 __378c__, 也可下载配合使用.

__mongo 命令不区分大小写.__

## 创建数据目录
安装好后, Mongodb 需要手动创建一个根目录用来存放数据, 请注意, 数据目录应该放在根目录下(如 C:\ 或者 D:\ 等).<br>
如在 C: 盘 下创建一个 Data 目录做为 Mongodb 的数据目录.

```
D:\

mkdir Data
```
<br>

## 以 CMD 进程运行 MongoDB 服务器
为了从命令提示符下运行 MongoDB 服务器, 需要在 MongoDB 目录的 __bin__ 目录中执行 __mongod.exe__ 文件.

```
mongod --dbpath D:\Data
```
<br>

如果执行成功, 可能会输出类似如下信息:

```
I CONTROL  [main] Hotfix KB2731284 or later update is not installed, will zero-out data files
I CONTROL  [initandlisten] MongoDB starting : pid=10916 port=27017 dbpath=D:\Data 64-bit host=SH61041PCW
I CONTROL  [initandlisten] targetMinOS: Windows Vista/Windows Server 2008
I CONTROL  [initandlisten] db version v3.2.4
I CONTROL  [initandlisten] git version: e2ee9ffcf9f5a94fad76802e28cc978718bb7a30
I CONTROL  [initandlisten] allocator: tcmalloc
I CONTROL  [initandlisten] modules: none
I CONTROL  [initandlisten] build environment:
I CONTROL  [initandlisten]     distarch: x86_64
I CONTROL  [initandlisten]     target_arch: x86_64
I CONTROL  [initandlisten] options: { storage: { dbPath: "D:\Data" } }
I STORAGE  [initandlisten] wiredtiger_open config: create,cache_size=4G,session_max=20000,eviction=(threads_max=4),config_base=false,statistics=(fast),log=(enabled=true,archive=true,path=journal,compressor=snappy),file_manager=(close_idle_time=100000),checkpoint=(wait=60,log_size=2GB),statistics_log=(wait=0),
I NETWORK  [HostnameCanonicalizationWorker] Starting hostname canonicalization worker
I FTDC     [initandlisten] Initializing full-time diagnostic data capture with directory 'D:/Data/diagnostic.data'
I NETWORK  [initandlisten] waiting for connections on port 27017
……
```
<br>

## 以 Windows 服务运行 MongoDB 服务器
```
mongod --bind_ip [your id adress] --logpath [D:\Data\mongodb.log] --logappend --dbpath [D:\Data] --port [your port number] --serviceName [your service name] --serviceDisplayName [your service name] --install
```
<br>

下表为 mongodb 启动的参数说明:

- __bind_ip__               绑定服务 IP, 若绑定 127.0.0.1, 则只能本机访问, __默认__所有 IP
- __logpath__               指定 MongoDB 日志文件, 注意是指定文件不是目录
- __logappend__             使用追加的方式写日志
- __dbpath__                指定数据库路径
- __port__                  指定服务端口号, __默认__端口 27017
- __serviceName__           指定服务名称
- __serviceDisplayName__    指定服务名称, 有多个 mongodb 服务时执行
- __install__               指定作为一个 Windows 服务安装

## MongoDB 自带的 Client
MongoDB 自带的 Client 是交互式的 Shell, 用来对 MongoDB 进行操作和管理, 执行 MongoDB 根目录下 __bin__ 目录中的 __mongo.exe__ 文件就能打开这个交互环境.

当进入 MongoDB Client 后, 它默认会链接到 __test__ 文档(__MongoDB 的文档就是常规理解中的数据库__)

```
> mongo
MongoDB shell version: 3.0.6
connecting to: test
……
```
<br>
__db__ 命令用于查看当前操作的文档(数据库):

```
> db
test
>
```
<br>
__db.serverCmdLineOpts()__ 方法用来查看连接的 Mongodb 的信息:

```js
db.serverCmdLineOpts()
{
        "argv" : [
                "mongod",
                "--dbpath",
                "D:\\Data"
        ],
        "parsed" : {
                "storage" : {
                        "dbPath" : "D:\\Data"
                }
        },
        "ok" : 1
}
```
<br>
MongoDB Client 中还可以运行一些简单的算术运算:

```
> 2 + 2
4
>
```

## 关闭服务

可以用以下三种方法来关闭已启动的 Mongodb 服务器:

- 最暴力, 直接 kill mongodb process
- 打开个 CMD, mogod \-\-shutdown \-\-dbpath xxx (好像新版的 mongodb 已经去除这个命令了)
- 用 Client 连上服务器, 然后切换到 admin 数据库, 使用 db.shutdownServer()
    + use admin
    + db.shutdownServer()

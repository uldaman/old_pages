Title: 07. zookeeper 简介
Author: HanXiao
Date: 2016-11-03 23:07
Summary: zookeeper 简介

[TOC]

# 简介
zookeeper 是一个分布式协调服务, 管理分布式环境中的数据, 为分布式应用提供**一致性**服务的软件, 提供的功能包括: 配置维护、名字服务、分布式同步、组服务等.

zookeeper 本身也集群, 只要集群里有半数以上, 就能正常为我们服务. 所以 zookeeper 适合安装在是奇数台的集群中.

zookeeper 集群角色:

- leader
- follower

zookeeper 角色不是配置出来的, 而是采用一个名为 Zab 的投票算法内部选举, 客户端向任意节点传数据, 数据都会被推送到 leader, leader 会将数据传到其它 follower.

> 补充知识: 投票算法比较有名的有个叫 PAXOS

更多 zookeeper 的细节可以参考: [zookeeper 原理](http://cailin.iteye.com/blog/2014486/), 实际上, 对于我们使用者来说, zookeeper 本质上只提供了两个功能:

- 数据保管
- 节点监听

说到节点, 就要提下 zookeeper 的目标结构, zookeeper 是个树状的层次化结构, 每个树节点叫做 znode, 并且有唯一的路径标识, znode 可以包含**数据**和**子节点** (ephemeral 节点除外), 客户端应用可以在节点上设置监听器.

znode 有四种形式的目录节点:

- persistent 永久节点
- persistent_sequential (带自增序号, 自增序号的使用主要用来对推断事件发生的顺序)
- ephemeral 临时节点, 客户端断开链接自删, 不允许建立子节点
- ephemeral_sequential


# 配置
直接去 [http://archive.apache.org/dist/](http://archive.apache.org/dist/) 下载回来解压就好, 参考 [Ubuntu 下 Hadoop 的安装](http://wiki.smallcpp.cn/Hadoop/%E6%90%AD%E5%BB%BA%20Hadoop%20%E5%88%86%E5%B8%83%E5%BC%8F%E5%AE%9E%E9%AA%8C%E7%8E%AF%E5%A2%83.html#3-hadoop).

首先把 `conf/zoo_sample.cfg` 拷贝一份并重命名为 `zoo.cfg`, 这就是 zookeeper 的配置文件. 关键配置:

- dataDir: 数据目录, 参考 hadoop 的数据目录设置
- `server.1~n=ip:port` (port 有两个 2888:3888, 2888 是 leader follower 通讯端口, 3888 是投票端口)
    + 如 server.1=192.168.1.156:2888:3888

服务端命令:

- bin/zkServer.sh start 启动 zk 集群
- bin/zkServer.sh status 查看 zk 集群状态

# 客户端工具
zookeeper 提供了一个 客户端工具 zkCli.sh, 通过命令 `zkCli.sh connect host:port` 就能连上 zk 集群.

常用命令: `ls`、`creae`、`get`、`set`、`delete`、`rmr`

在 get/ls 时注册 **watch**, **watch** 只生效一次, 被触发后就失效了.

# Java Api
连接 zookeeper 集群:<br>
`zk_obj=zookeeper(zk 集群的 ip:port, timeout, new Watcher(){})` (zookeeper 会开启个守护线程保持和 zk 的长链接).

在 Watcher 里监听事件并处理 (回调)

- event.getType
- event.getPath

需要注意一下, 有时我们拿到 zk\_obj 后, 由于 zk 环境还是准备后, 会导致后续的操作失败, 所以我们拿到 zk\_obj 后可以通过 zk\_obj.getState() 来判断下当前集群的状态, 当它为 CONNECTED 时才继续操作.

```
路径=zk_obj.create(路径, 数据, 权限, 节点模式)

zk_obj.getChildren(路径, 监听器)

节点元数据=zk_obj.exists(路径, 监听器)

zk_obj.getdata(路径, 监听器, null)

zk_obj.delete(路径, -1) 参数2 指定要删除指定版本, -1 表示删除所有版本

zk_obj.setData(路径, 数据, -1) 参数3 同上
```

# zookeeper 应用
zookeeper 虽然本质上只提供了两个功能: 数据保管和节点监听, 但是它提供了丰富的 API, 使用这个 API 我们就能写业务逻辑来实现诸多功能, 下面是两个例子.

## 洞察服务器上下线
**利用 zookeeper 实现客户端实时洞察服务器上下线的变化**

- 服务器上线就 -> zk 注册临时节点, 启动服务端业务功能
    + 服务端宕掉或业务功能异常就会和 zk 断开, 临时节点就会被删除
- 客户端获取 zk 节点并监听, 获取当前在线服务器列表, 根据规则(如果有)去挑选服务器
- 客户端监听到服务节点上下线事件通知重新获取列表并监听

## 共享锁
**利用 zookeeper 实现分布式共享锁**

- 客户程序启动 -> zk 注册带临时序号的节点 (假设为 uuid)
- 获取当前所有 uuid
- uuid 最小的先去访问资源
- 访问后将自己的 uuid 删掉, 并注册新的节点
- 其他客户程序收到事件变化, 重新获取当前所有 uuid 最小的去访问资源

## 高可用
**利用 zookeeper 实现高可用**

原理都差不多, 无非就是自写逻辑监听 zk 节点变化, 这里分析下 keepalived 与 zookeeper, 参考[知乎一篇不错的答案](https://www.zhihu.com/question/47632675/answer/127669517).

keepalived 与 zookeeper 都可以用来实现高可用, 另外常见的还有 DNS.

先看看优缺点, 就可以看出在实现高可用时的区别. 高可用一般跟负载均衡会一起考虑, 所以下面的比较也会提到负载均衡能力.

**Keepalived**:

- 优点: 简单, 基本不需要业务层面做任何事情, 就可以实现高可用, 主备容灾. 而且容灾的宕机时间也比较短.
- 缺点: 也是简单, 因为 VRRP、主备切换都没有什么复杂的逻辑, 所以无法应对某些特殊场景, 比如主备通信链路出问题, 会导致脑裂. 同时, keepalived 也不容易做负载均衡.

**zookeeper**:

- 优点: 可以支持高可用, 负载均衡. 本身是个分布式的服务.
- 缺点: 跟业务结合的比较紧密. 需要在业务代码中写好 ZK 使用的逻辑, 比如注册名字. 拉取名字对应的服务地址等.

**DNS**

- 优点: 不复杂, 同时与业务结合的不是很紧密, 通过简单的逻辑就可以实现负载均衡.
- 缺点: DNS 容灾是更新 DNS 服务器需要时间, 宕机时间比较长.

所以, 区别很明显:

- 从简单性来说: Keepalived 最简单, DNS 次之, ZK 最复杂.
- 从负载均衡能力来看, zookeeper 最强, DNS 次之, Keepalived 最弱.
- 从与业务的紧密程度来看: ZK 最紧密, DNS 次之, Keepalived 基本跟业务层面没有关系.

所以使用场景, 个人看法, 对于框架级别的业务可能会选择 ZK, 仅仅需要做容灾的用 Keepalived. DNS 的方法介乎两者中间.

另外, keepalive 只可以选出一台机器作为主机, 所以 keepalive 只能实现 M:1 的备份, zookeeper 可以选出 N 台机器作为主机, 它可以实现 M:N 的备份.

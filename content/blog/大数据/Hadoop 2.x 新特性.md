Title: 03. Hadoop 2.x 新特性
Author: HanXiao
Date: 2016-10-23 19:21
Summary: Hadoop 2.x 新特性

[TOC]

# Hadoop 1.x 问题
主要就是 NameNode 单点问题.

Hadoop 1.x 中, 一个集群就只有一个 NameNode, 这种架构虽然实现简单, 但会产生**单点**、**内存**瓶颈、**性能**
瓶颈等限制.

**首先**, 整个 Hadoop 集群的命名空间都归一个 NameNode 管理, 这样 HDFS 所能存储的文件数量会受到 NameNode 容量的限制;

**其次**, 当集群进行复杂运算时, 也只有一个 NameNode 在运作, 集群的运算性能也会受到 NameNode 的限制.

**最后**, 虽然集群有 Second NameNode 作为辅助节点, 但并不会完成自动切换, 当 NameNode 宕掉时, 还是需要人工去处理.

虽然仅仅在像 Yahoo 和 Facebook 返种规模的大公司才会面对这样的限制问题, 但在 Hadoop 2.x 中, 官方还是给出了解决方案.

# Hadoop 2.x 解决方案
Hadoop 2.x 提出了两个新特性用以解决以上问题:

- HDFS 联邦
- HDFS HA

Reference: [2.X 高可靠 HA 及 Federation (联盟)](http://www.smallcpp.cn/10-2x-gao-ke-kao-ha-ji-federation-lian-meng.html)

# HDFS 快照
在 2.x 终于实现了快照.

## 快照的作用是什么?
HDFS 2.x 中现在可以对目录创建 Snapshot, 创建之后不管后续目录发生什么变化, 都可以通过 snapshot 找回原来的文件和目录结构.

为了启用这种功能, 首先需要启用目标目录的 snapshot 功能, 可以通过 `hdfs dfsadmin -allowSnapshot` 命令来启用 snapshot 功能, 启用后, 并不会自动进行 snapshot 保存, 还需要先对现场手动创建一次 snapshot, 通过下面的命令来执行: `hdfs dfs -createSnapshot []`.

可以为相同的目录创建多个 snapshot, 不同的 snapshot 通过名字来区分, 默认是 `syyyyMMdd-HHmmss.SSS`, 例如 `/storage/WALs/.snapshot/s20140515-084657.639`.

## 实现原理
实现上是通过在每个目标节点下面创建 snapshot 节点, 后续任何子节点的变化都会同步记录到 snapshot 上. 例如删除子节点下面的文件, 并不是直接文件元信息以及数据删除, 而是将他们移动到 snapshot 下面. 这样后续还能够恢复回来.

另外 snapshot 保存是一个完全的现场, 不仅是删除的文件还能找到, 新创建的文件也无法看到. 后一种效果的实现是通过在 snapshot 中记录哪些文件是新创建的, 查看列表的时候将这些文件排除在外.

在 HDFS 中 INode 表示一个节点, 其中 INodeFile 表示文件, INodeDirectory 表示目录. INodeFileWithSnapshot 表示带有快照的文件, INodeDirectoryWithSnapshot 表示带有快照的目录, (INodeDirectorySnapshottable 表示可以创建快照的目录, INodeDirectoryWithSnapshot 不能创建新的快照, 只能将目录的变化记录到现有的快照里面) 相关的类结构如下:

![]({static}/images/Hadoop新特性/快照1.jpg)

图中红线表示的是关键类的引用关系, 其中最重要的是 DirectoryDiffList, 里面保存了一些快照和当前目录的差别. 每一个 DirectoryDiff 中包含快照以及儿子变化, 是实现快照功能的核心. ChilderenDiff 中 created list 保存的是从快照时间之后新创建的节点, deteled list 保存的新删除的节点. snapshot 中的 root 节点保存了 snapshot 的 name, 可以通过这个找到对应的快照.

## 例子分析
我们通过一个例子来分析整个 snapshot 的实现细节:

1\. 文件目录树如下图所示, 并且我们已经通过命令启动了 a 的 snapshot 功能, 结构如下图所示:

![]({static}/images/Hadoop新特性/快照2.jpg)

图中 .snapshot 是虚拟节点, 保存了所有的 snapshot 列表, 其中 diff 中还保存当前节点下面的变化, 一个 snapshot 对应于一个 diff. 要注意的是 snapshot 中可以被多个目录的 diff 引用, 后续会进行说明.

2\. 当我们执行 createSnapshot 命令时, 结果如下:

![]({static}/images/Hadoop新特性/快照3.jpg)

3\. 当删除文件 e 的时候, 不论是删除一个文件还是一个目录, 只要是直接子节点, 都会将节点转换为快照版本. 例如 e 会变成 INodeFileWithSnapshot, 在 a 的 DirectoryDiff 中 ChildDiff 中 deleted 列表中将会包含 e, 而在 a 的正常节点下会被删除. 目录节点的处理同样.

4\. 删除孙子节点是的情况

![]({static}/images/Hadoop新特性/快照4.jpg)

处理这种节点的原则是: 先将孙子节点转变为 Snapshot 版本, 然后将父节点变为 snapshot 版本, 同时将孙子节点版本加入到直接父节点的 diff 列表中. 为了能够通过同一个 snapshot 找到当时的文件, 需要将新的 diff 指向到老的 snapshot 版本上. 图中 d 节点是 INodeDirectoryWithSnapshot (不是 INodeDiretorySnapshottable, 本身不允许在 d 上创建 snapshot).

## 快照命令
- 设置一个目录为可快照:
    + `hdfs dfsadmin -allowSnapshot <path>`
- 取消目录可快照:
    + `hdfs dfsadmin -disallowSnapshot <path>`
- 生成快照:
    + `hdfs dfs -createSnapshot <path> [<snapshotName>]`
- 删除快照:
    + `hdfs dfs -deleteSnapshot <path> <snapshotName>`
- 列出所有可快照目录:
    + `hdfs lsSnapshottableDir`
- 比较快照之间的差异:
    + `hdfs snapshotDiff <path> <fromSnapshot> <toSnapshot>`

![]({static}/images/Hadoop新特性/快照.png)

## Refrences
[HDFS snapshot 占用空间吗](http://www.aboutyun.com/thread-14480-1-1.html)<br>
[HDFS Snapshot 原理](http://www.aboutyun.com/thread-14495-1-1.html)<br>
[HDFS 快照管理](http://blog.csdn.net/androidlushangderen/article/details/51282612)

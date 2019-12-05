Title: 04. 使用 Shell 操作 HDFS
Author: HanXiao
Date: 2016-10-23 20:25
Summary: 使用 Shell 操作 HDFS

[TOC]

# 基本用法
执行一个 HDFS 命令, 有下面两种写法:

- hadoop 1.x `hadoop fs -???`
- hadoop 2.x `hdfs dfs -???`

后面的 `???` 是一个具体的文件系统命令, 和 Linux 的文件系统命令很相似, 如查看当前 HDFS 文件系统中的文件:

```
HDFS dfs -ls hdfs://smallcpp01:9000/
```

这里要注意下 HDFS 文件系统和本地文件系统的区别, 由于 HDFS 是分布式文件系统, 是通过网络共享, 因此需要个协议, 类似网络共享的 `http`、`ftp` 协议等, 这里就是 `HDFS` 协议, 所以上面的 HDFS 由三部分组成:

| HDFS:// | smallcpp01:9000 | /                       |
| ------- | --------------- | ----------------------- |
| 协议    | 主机地址端口    | 目录结构 (这里是根结点) |

如果在 `core-site.xml` 里指定了 `defaultFS`, 那上面地址中的 协议 和 主机地址端口 可以省略, 简写个目录结构就可以了:

```
HDFS dfs -ls /
```

如果连目录结构都省略 `HDFS dfs -ls`, 这样默认访问的是 `hdfs://smallcpp01:9000/user/<current user>` 目录.

`ls` 命令的结果由 7 部分组成:

| -rw-r--r-- | 2                            | hanxiao | supergroup | 59   | 2016-10-16 21:30 | /words.txt |
| ---------- | ---------------------------- | ------- | ---------- | ---- | ---------------- | ---------- |
| 权限       | 副本<br>(如果是目录则为 \- ) | 创建者  | 所在组     | 大小 | 最后访问时间     | 文件路径   |

**当前目录?**

在 HDFS 提供的命令中, 是没有当前目录的概念的, 更没有 `cd` 命令.

**数据存在哪?**

从 OS 的角度, 数据被放在 DataNode 的 `/tmp/dfs/data/current/` 目录下, 当然从 OS 的角度, 是看不懂这里面的文件的, 打开后都是些二进制.

**帮助?**

```
hdfs dfs -help
hdfs dfs -help 具体命令
```

# 命令参考
更多命令参考: [hdfs 命令.doc](http://pan.baidu.com/s/1kUXcdxl)

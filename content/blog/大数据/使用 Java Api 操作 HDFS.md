Title: 05. 使用 Java Api 操作 HDFS
Author: HanXiao
Date: 2016-10-23 20:26
Summary: 使用 Java Api 操作 HDFS

[TOC]

以 Hadoop 权威指南 (第三版) 3.5.2 为例.

```java
import java.io.InputStream;
import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

public class FileSystemCat {
    public static void main(String[] args) throws Exception {
        String uri = args[0];
        FileSystem fs = FileSystem.get(URI.create(uri), new Configuration());
        InputStream in = null;
        try {
            in = fs.open(new Path(uri));
            IOUtils.copyBytes(int, System.out, 4096, false);
        } finally {
            IOUtils.closeStream(in);
        }
    }
}

```

代码就不解释了, 主要记录一下环境设置.

# 环境变量
如果你是参考我的 Wiki [搭建 Hadoop 分布式实验环境](http://wiki.smallcpp.cn/Hadoop/%E6%90%AD%E5%BB%BA%20Hadoop%20%E5%88%86%E5%B8%83%E5%BC%8F%E5%AE%9E%E9%AA%8C%E7%8E%AF%E5%A2%83.html#33) 搭建的实验环境, 那环境变量应该是已经配好了.

`vim ~/.bashrc`

```shell
export JAVA_HOME=/usr/java/jdk1.8.0_101
export HADOOP_HOME=/usr/smallcpp/hadoop-2.7.3
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

运行 `source ~/.bashrc` 刷新环境变量.

# Hadoop 类目录
这个类目录的作用是当运行 hadoop 或者 hdfs 的命令时, 命令的搜索目录.

首先到 Hadoop 的根目录下创建一个新目录:

```shell
cd /usr/smallcpp/hadoop-2.7.3/
mkdir myclass
```

然后 `vim hadoop-env.sh` 设置 `HADOOP_CLASSPATH`:

```shell
# Extra Java CLASSPATH elements.  Automatically insert capacity-scheduler.
export HADOOP_CLASSPATH=/usr/smallcpp/hadoop-2.7.3/myclass

for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do
  if [ "$HADOOP_CLASSPATH" ]; then
    export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f
  else
    export HADOOP_CLASSPATH=$f
  fi
done

```

这样当执行 `hdfs FileSystemCat` 的时候, 就会去 `/usr/smallcpp/hadoop-2.7.3/myclass` 找我们写好的 `FileSystemCat` 应用了.

# 编译源码
要将 Java 源码文件编译成 `.class` 文件才能被 Hadoop 识别, 编译 Hdfs 应用需要导入 Hadoop 的 jar 包, 这些包位于以下目录:

- /usr/smallcpp/hadoop-2.7.1/share/hadoop/common
- /usr/smallcpp/hadoop-2.7.1/share/hadoop/common/lib
- /usr/smallcpp/hadoop-2.7.1/share/hadoop/hdfs
- /usr/smallcpp/hadoop-2.7.1/share/hadoop/hdfs/lib

我们这里的例子用到的是 `/usr/smallcpp/hadoop-2.7.3/share/hadoop/common/hadoop-common-2.7.3.jar` 包, 执行 `javac` 命令时用 `-cp` 指定下就好.

```shell
javac -cp /usr/smallcpp/hadoop-2.7.3/share/hadoop/common/hadoop-common-2.7.3.jar FileSystemCat.java
```

然后 `/usr/smallcpp/hadoop-2.7.3/myclass` 下就多了个 `FileSystemCat.class` 文件.

这时执行 `hdfs FileSystemCat /xxx` 就能查看到 `xxx` 文件的内容啦, 类似 linux 的 `cat` 命令.

# ant
由于编译源码时需要指定 Hadoop 的 jar 包, 当引入的 jar 包多时, 这样就特别麻烦, 我们可以借用 ant 工具来编译源码, ant 可以在 `bulid.xml` 中设定 jar 包的所在目录, 这样就比较方便了.

这里仅作介绍, 因为我是使用 [Eclipse](http://www.smallcpp.cn/05-shi-yong-java-api-cao-zuo-hdfs.html#eclipse-hdfs) 进行开发的, 导入 jar 包相对于说, 还是比较方便的.

# 其他例子
## 例 1
读入本地文件系统一个大约一百多字节的文本文件, 并将其第 101-120 字节的内容写入 HDFS 成为一个新文件.

```java
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;


public class CopyLocalToHdfs {

    public static void main(String[] args) throws Exception {
        String local_uri = args[0];
        String hdfs_uri = args[1];
        InputStream in = new BufferedInputStream(new FileInputStream(local_uri));
        in.skip(100);
        FileSystem fs = FileSystem.get(URI.create(hdfs_uri), new Configuration(), "hanxiao");
        OutputStream out = fs.create(new Path(hdfs_uri));
        IOUtils.copyBytes(in, out, (long)20, true);
    }
}
```

## 例 2
例 1 的反向操作, 读入 HDFS 文件系统一个大约一百多字节的文本文件, 并将其第 101-120 字节的内容写入本地文件系统成为一个新文件.

```java
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;


public class CopyHdfsToLocal {

    public static void main(String[] args) throws Exception {
        String hdfs_uri = args[0];
        String local_uri = args[1];
        FileSystem fs = FileSystem.get(URI.create(hdfs_uri), new Configuration(), "hanxiao");
        InputStream in = fs.open(new Path(hdfs_uri));
        in.skip(100);
        OutputStream out = new BufferedOutputStream(new FileOutputStream(local_uri));
        IOUtils.copyBytes(in, out, (long)20, true);
    }
}
```

# 使用 Eclipse 开发 Hdfs 应用
参考我的 Wiki: [使用 Eclipse 开发 HDFS](http://wiki.smallcpp.cn/Hadoop/%E4%BD%BF%E7%94%A8%20Eclipse%20%E5%BC%80%E5%8F%91%20HDFS.html)

# Hdfs 源码分析
参考 [HDFS 2.6.0 源码分析](http://blog.csdn.net/lipeng_bigdata/article/category/6049177)

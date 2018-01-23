Title: 15、Redis 数据类型
Author: Martin
Date: 2016-03-28 12:37
Summary: 介绍 Redis 中不同的数据类型的命令使用.

[TOC]

命令速查: [http://doc.redisfans.com/](http://doc.redisfans.com/)

# Key 操作
redis 中不管保存什么类型的数据, 它都要对应一个 key, 先看看 key 的命令有哪些.

- __keys__: 返回所有符合给定模式(正则)的 key
    + 语法 keys regex
        * key \* 匹配所有字符
        * key ? 匹配一个任意字符
        * key \[\] 匹配字符组
        * key \x 匹配转义字符
- __exists__: 检测指定 key 是否存在
    + 语法 exists key
        * 存在返回 1
        * 不存在返回 0
- __type__: 返回相关 key 的 value 类型
    + 语法 type key
- __expire__: 设置 key 的过期时间, 单位秒
    + 语法 expire key seconds
    + set/getset 命令, 会清除 key 的过期时间
- __ttl__: 查看相关 key 的剩余时间, 单位秒
    + 语法 ttl key
        * 没有设置 key 的过期时间, 返回 -1
        * 如果 key 不存在, 返回 -2
- __expireat__: 设置 key 的过期时间点(在指定时间戳过期), 单位秒
    + 语法 expireat key timestamp
    + set/getset 命令, 会清除 key 的过期时间
- __pexpire__: 设置 key 的过期时间, 单位毫秒
    + 语法 pexpire key millisecond
    + set/getset 命令, 会清除 key 的过期时间
- __pttl__: 查看相关 key 的剩余时间, 单位毫秒
    + 语法 pttl key
        * 没有设置 key 的过期时间, 返回 -1
        * 如果 key 不存在, 返回 -2
- __pexpireat__: 设置 key 的过期时间点(在指定时间戳过期), 单位毫秒
    + 语法 pexpireat key timestamp
    + set/getset 命令, 会清除 key 的过期时间
- __persist__: 将 key 设置永久
    + 语法 persist key
- __del__: 删除指定 keys
    + 语法 del key1 key2
        * 返回删除 key 的数量
- __randomkey__: 随机取个 key
    + 语法 randomkey
- __rename__: 重命名 key
    + 语法 rename key newkey
        * 如果 newkey 与当前已有 key 重名, 会覆盖掉旧的 key
- __renamenx__: 重命名 key, 但 newkey 必须不存在时才生效
    + 语法 renamenx key newkey
- __dump__: 序列化给定的 key, 返回序列化之后的值
    + 语法 dump key
- __restore__: 反序列化
    + 语法 restore key millisecond value
        * 将 value 反序列化到一个 key 上
        * millisecond 为生存时间, 设为 0 表示不限制时间
- __move__: 将当前数据库中的 key 移动到另一个数据库
    + 语法 move key dbid
        * 如果另一个数据库已经有同名 key, 则不发生移动

# String
一个键最多存储 __512 MB__.

> 注意: 所有的 String 命令, 设置 value 时要用引号包起来(数字除外, 输入数字 redis 会自动在内部转化成 str)

- __set__: 设置相关 key 的 value
    + 语法 set key value
- __get__: 获取相关 key 的 value
    + 语法 get key
        * key 不存在返回  nil
        * key 持有非字符串 value 则返回一个错误
- __append__: 追加相关 key 中的 value
    + 语法: append key value
        * 如果 key 已经存在并且是一个字符串, 将 value 追加到 key 原来的值的末尾
        * 如果 key 不存在，就简单地将给定 key 设为 value, 就像执行 set key value 一样
        * 返回 key 中追加后的 value 长度
- __setrange__: 替换相关 key 的 value 中的一部分
    + 语法 setrange key offset value
        * 将原 value 中 \[offset 至 value 结束\] 的部分替换掉
        * 返回被替换部分的内容长度
        * 如果待替换部分的内容长度比要设置的新内容长度长, 则会以 \x00 填充
        * key 不存在时, 会生成新 key
- __getrange__: 返回字符串的一部分
    + 语法 getrange key start end
        * 下标从 0 开始
        * 支持负数, 表示从字符串末尾开始数(-1 表示最后一个)
- __getset__: 设置相关 key 的 value 并返回旧的 value
    + 语法 getset key value
        * key 不存在时, 返回 nil, 并新建 key
        * key 持有非字符串 value 则返回一个错误
- __mset__: 设置多个 key 的 value
    + 语法 mset key1 value1 key2 value2 ...
- __mget__: 获取个 key 的 value
    + 语法 mset key1 key2 ...
        * 返回多行字符串
- __strlen__: 获取相关 key 的 value 的长度
    + 语法 strlen key
        * key 不存在时, 返回 0
        * key 持有非字符串 value 则返回一个错误
- __setnx__: 仅当 key 不存在时才设置成功
    + 语法 setnx key value
- __setex__: 设置 key 的过期时间, 即 key 多久后自动销毁, 单位秒
    + 语法 setex key seconds value
        * 可用 __ttl__ key 查看 key 还剩多久, 单位秒
        * 可用 __expire__ key seconds 单独设置 key 的过期时间, 单位秒
- __msetnx__: 设置多个 key 的 value, 仅当所有的 key 都不存在时才设置成功
    + 语法 msetnx key1 value1 key2 value2
        * 成功返回 1, 失败返回 0
- __psetex__: 设置 key 的过期时间, 即 key 多久后自动销毁, 单位毫秒
    + 语法 psetex key millisecond value
        * 可用 __pttl__ key 查看 key 还剩多久, 单位毫秒
        * 可用 __pexpire__ key seconds 单独设置 key 的过期时间, 单位毫秒
- __set 扩展语法__: 设置相关 key 的 value
    + 语法 set key value 扩展参数
        * ex seconds: 等同于 setex
        * px millisecond: 等同于 psetex
        * nx: 等同于 setnx
        * xx: 只有键已经存在才可以设置成功
- __incr__: 对 key 中存储的数字 +1
    + 语法 incr key
        * 如果 key 不存在, 则会先初始化为 0, 再进行 incr 操作
        * 如果 key 的 value 不是数字(指数字型字符串), 则会报错
- __incrby__: 对 key 中存储的数字加上指定 __int__ 值
    + 语法 incrby key increment
        * increment 必须是 int 型
        * 如果 key 不存在, 则会先初始化为 0, 再进行 incr 操作
        * 如果 key 的 value 不是数字(指数字型字符串), 则会报错
- __incrbyfloat__: 对 key 中存储的数字加上指定 __float__ 值
    + 语法 incrby key increment
        * increment 可以是 int 、float 型
        * 如果 key 不存在, 则会先初始化为 0, 再进行 incr 操作
        * 如果 key 的 value 不是数字(指数字型字符串), 则会报错
- __decr__: 对 key 中存储的数字 -1
    + 语法 decr key
        * 如果 key 不存在, 则会先初始化为 0, 再进行 decr 操作
        * 如果 key 的 value 不是数字(指数字型字符串), 则会报错
- __decrby__: 对 key 中存储的数字减去指定 __int__ 值
    + 语法 decrby key decrement
        * decrement 必须是 int 型
        * 如果 key 不存在, 则会先初始化为 0, 再进行 incr 操作
        * 如果 key 的 value 不是数字(指数字型字符串), 则会报错
        * decr 系列没有 __decrbyfloat__ 命令

# Hash
Redis Hash 其实是 key 的 value 中保存的是一个 HashMap, 如果该 Map 的成员数比较少, 则会采用类似一维线性的紧凑格式来存储该 Map, 即省去了大量指针的内存开销, 这个参数控制对应在 redis.conf 配置文件中下面 2 项:

- hash-max-zipmap-entries 64
- hash-max-zipmap-value 512

entries 的含义是当 value 中的 Map 内部不超过多少个成员时会采用线性紧凑格式存储, 默认是 64, 超过该值自动转成真正的 HashMap.

value 的含义是当 value 中的 Map 内部的每个成员值长度不超过多少字节就会采用线性紧凑存储来节省空间.

以上 2 个条件任意一个条件超过设置值都会转换成真正的 HashMap, 也就不会再节省内存了, 那么这个值是不是设置的越大越好呢, 答案当然是否定的, HashMap 的优势就是查找和操作的时间复杂度都是O(1)的, 而放弃 Hash 采用一维存储则是O(n)的时间复杂度，如果成员数量很少, 则影响不大, 否则会严重影响性能, 所以要权衡好这个值的设置, 一般默认即可.

- __hset__: 设置相关 key 中保存的 Hash 的 field 的值
    + 语法 hset key field value
- __hget__: 获取相关 key 中保存的 Hash 的 field 的值
    + 语法 hget key field
        * key 或者 field 不存在, 返回 nil
- __hsetnx__: 设置相关 key 中保存的 Hash 的 field 的值, field 不存在时才设置成功
    + 语法 hsetnx key field value
- __hmset__: 设置相关 key 中保存的 Hash 的多个 field 的值
    + 语法 hmset key field1 value1 field2 value2 ...
- __hmget__: 获取相关 key 中保存的 Hash 的多个 field 的值
    + 语法 hmget key field1 field2 ...
        * 返回多行字符串
- __hgetall__: 获取相关 key 中保存的 Hash 所有 field 和 value
    + 语法 hgetall key
        * 返回多行字符串
            - 奇数序号是 field
            - 偶数序号是 value
- __hkeys__: 获取相关 key 中保存的 Hash 所有 field
    + 语法 hkeys key
- __hvals__: 获取相关 key 中保存的 Hash 所有 value
    + 语法 hvals key
- __hexists__: 检测相关 key 中保存的 Hash 的 field 是否存在
    + 语法 hexists key field
        * 存在返回 1
        * 不存在返回 0
- __hlen__: 获取相关 key 中保存的 Hash 的 field 的数量
    + 语法 hlen key
- __hincrby__: 对 key 中保存的 hash 的 field 存储的数字上指定 __int__ 数值
    + 语法 hincrby key field increment
        * increment 只能是 int 型
- __hincrbyfloat__: 对 key 中保存的 hash 的 field 存储的数字上指定值
    + 语法 hincrbyfloat key field increment
        * increment 可以是 int 和 float 型
- __hdel__: 删除 key 中保存的 hash 的 fields
    + 语法 hdel key field field
        * 返回被删除 field 的数量

# List
List 型的 value 最多存储 (2^32 - 1) 个元素

List 类型的数据的弊端和常规 List 一样 \-\- 通过下标(索引)来访问, 效率很低.

```
list 就是数据结构中的双向链表, 因此它的内存空间可以是不连续的, 通过指针来进行数据的访问, 这个特点使得它的随即存取变的非常没有效率, 但它的 插入/删除、取首/尾数据 效率高.
```

使用 Rdies List, 可以简单实现 __MQ__ 功能.

注意, 列表的 __左端__ 的下标为 0, 即为列表头.

- __lpush__: 向左端添加元素(一个或多个)
    + 语法 lpush key value1 value2 ...
        * 如果 key 不存在, 则新建
        * 如果 key 中原有 value 不是 list, 则报错
        * 返回插入后的 List 长度
- __rpush__: 向右端添加元素(一个或多个)
    + 同 lpush
- __lpushx__: 向左端添加元素(一个)
    + 语法 lpushx key value
        * 必须 key 已经存在时才添加成功, 不存在返回 0
- __rpushx__: 向左端添加元素(一个)
    + 语法 rpushx key value
        * 必须 key 已经存在时才添加成功, 不存在返回 0
- __lpop__: 弹出左端的第一个元素
    + 语法 lpop key
        * 返回元素
        * key 不存在, 返回 nil
- __rpop__: 弹出右端的第一个元素
    + 同 lpop
- __llen__: 获取列表的长度(元素数量)
    + 语法 llen key
        * key 不存在, 返回 0
- __lrange__: 获取列表片段
    + 语法 lrange key start end
        * 下标从 0 开始
        * 支持负数, 表示从字符串末尾开始数(-1 表示最后一个)
- __ltrim__: 截取列表片段(类似字符串截取)
    + 语法 ltrim key start end
- __lrem__: 删除列表中 N 个指定的值的元素
    + 语法 lrem key count value
        * 删除列表中值为 value 的元素, 移除 count 个
        * count > 0, 从列表__左向右__开始删除 count 个, 即从__列表头__开始删
        * count < 0, 从列表__右向左__开始删除 count 个, 即从__列表尾__开始删
        * count = 0, 删除所得符合条件的元素
- __lindex__: 获得指定索引元素的值
    + 语法 lindex key index
        * index 超出范围, 返回 nil
- __lset__: 设置指定索引元素的值
    + 语法 lset key index value
- __linsert__: 插入元素
    + 语法 linsert key before/after pivot value
        * 在列表中值为 pivot 的元素前或者后插入新元素 value
            - 如果列表中没有值为 pivot 的元素, 则不进行插入, 返回 -1
            - 如果 key 不存在, 返回 0
- __rpoplpush__: 将元素从一个列表右端弹出, 插入另一个列表左端
    + 语法 rpoplpush key1 key2
        * 返回操作元素的值
        * 如果 key1 == key2, 则相当于把一个元素从列表头移到列表尾
        * 注意, 没有 __lpoprpush__
- __blpop__: lpop 的阻塞版本, 但它支持多个 key
    + 语法 blpop key1 key2 ... timeout
        * 如果给定列表中没有元素, 则该命令不会返回, 直到 timeout 或者有元素可 pop(即有另一个客户端对列表执行 push 命令)
        * timeout 设为 0 表示永久等待
        * 多个 key 参数时, 按参数 key 的先后顺序依次检查各个列表, 弹出第一个非空列表的头元素
            - 返回多行字符串
            - 第一行表示是哪个 key 返回的
            - 第二行表示返回的值
- __brpop__: rpop 的阻塞版本, 但它支持多个 key
    + 同 blpop
- __brpoplpush__: rpoplpush 的阻塞版本
    + 语法 brpoplpush source destination timeout
        * 当列表 source 为空时, brpoplpush 命令将阻塞连接, 直到等待超时, 或有另一个客户端对 source 执行 push 命令为止
        * timeout 设为 0 表示永久等待

# Set
可以理解成一种特殊的 list.

但和 List 类型不同的是, Set 集合中不允许出现重复的元素, 这一点和 C++ 标准库中的 set 容器是完全相同的.

和 List 类型相比, Set 类型在功能上还存在着一个非常重要的特性, 即完成多个 Set 之间的聚合计算操作, 如并集、差集.

例如做 QQ号 好友推荐功能, 两个 QQ号 的好友都用集合来存储, 就可以通过集合的差集功能.

- __sadd__: 向集合中添加元素
    + 语法 sadd key member1 member2 ...
        * 返回添加元素的个数
- __scard__: 返回集合中元素个数
    + 语法 scard key
        * 集合不存在, 返回 0
- __smembers__: 查看集合中的元素
    + 语法 smembers key
        * 返回多行字符串
- __sismember__: 检测 member 是否是集合中的成员
    + 语法 sismember key member
- __srem__: 删除集合中的一个或多个成员
    + 语法 srem key member1 member2 ...
        * 返回成功删除的元素个数
- __spop__: 弹出集合中的随机元素
    + 语法 spop key
- __srandmember__: 返回集合中的随机元素(注意, 不是弹出)
    + 语法 srandmember key count
        * count 指定返回元素的个数
            - count > 0, 返回指定个数的元素, 返回的元素不重复
            - count < 0, 返回指定个数的元素, 返回的元素可重复
- __smove__: 将一个集合中的元素移动到另一个集合
    + 语法: smove source destination member
        * 将集合 source 中的元素 member 移动到集合 destination 中
- __sdiff__: 返回集合间的差集
    + 语法 sdiff key1 key2 ...
        * key 的顺序很重要, 谁在前面, 就返回谁的差集
            - 如 key1 = [1, 2, 3], key2 = [2, 3, 4]
            - sdiff key1 key2
                + 返回 1
            - sdiff key2 key1
                + 返回 4
- __sinter__: 返回集合间的交集
    + 语法 sinter key1 key2 ...
- __sunion__: 返回集合间的并集
    + 语法 sunion key1 key2 ...
- __sdiffstore__: 将差集结果保存到指定集合中
    + 语法 sdiffstore destination key1 key2 ...
        * 将 key1 key2 集合的差集保存到集合 destination 中
        * destination 也可以中 key1/key2 本身
- __sinterstore__: 将交集结果保存到指定集合中
    + 语法 参考 sdiffstore
- __sunionstore__: 将并集结果保存到指定集合中
    + 语法 参考 sdiffstore

# Sorted Set
相当于给 set 中的元素都关联一个权值, SortedSet 根据权值可以为集合进行排序.

- __zrank__: 获取元素的排名(下标)
    + 语法: zrank key member
        * 所谓排名, 就是这个元素在集合中的下标
        * 按权值从__小到大__排序, 所以下标 0 就是权值最小的元素
- __zrevrank__: 获取元素的排名(下标)
    + 语法: zrank key member
        * 所谓排名, 就是这个元素在集合中的下标
        * 按权值从__大到小__排序, 所以下标 0 就是权值最大的元素
- __zdd__: 将元素及其分数添加到集合中
    + 语法  zdd key score1(权值) member1(元素) score2 member2 ...
        * 返回添加的成员数量
        * score1 可以是 +inf(正, 无穷大) -inf(负, 无穷小)
- __zscore__: 获取指定元素的权值
    + 语法 zscore key member
        * key 或 member 不存在, 返回 nil
- __zcard__: 获取集合中元素的数量
    + 语法 zcard key
- __zcount__: 获取指定权值内的元素数量
    + 语法 zcount key min max
        * __\(__score 表示不包含 score, 参考下面的 zrangebyscore
- __zrange__: 获取一段区间内的元素, 从小到大
    + 语法 zrange start end
        * 对 zrange 来说, 按权值从小到大排序, 所以下标 0 就是权值最小的元素
        * 如果元素权值相同, 对元素的值按字典序排序
        * 可选参数 __withscores__, 表示返回元素的权值
- __zrevrange__: 获取一段区间内的元素, 从大到小
    + 语法 zrevrange start end
        * 对 zrevrange 来说, 按权值从大到小排序, 所以下标 0 就是权值最大的元素
        * 其他的同 zrange
- __zrangebyscore__: 获取指定权值范围内的元素, 从小到大
    + 语法 zrangebyscore key min max \[withscores\] \[limit offset count\]
        * 单独的写 score 表示包含 score
            - 如 zrangebyscore key 80 90 表示权值包含 80 和 90
        * __\(__score 表示不包含 score,
            - 如 zrangebyscore key 80 __\(__90 表示权值包含 80, 但不包含 90
            - 如 zrangebyscore key __\(__80 90 表示权值不包含 80, 但包含 90
        * 可选参数 __withscores__, 表示返回元素的权值
        * 可选参数 __limit__, 表示从返回的结果中从 offset 处截取 count 个元素
- __zrevrangebyscore__: 获取指定权值范围内的元素, 从大到小
    + 参考 zrangebyscore
- __zincrby__: 增加元素的权值, 可以是负数
    + 语法 zincrby key increment member
        * 返回操作后的权值
- __zrem__: 删除一个或多个元素
    + 语法 rem key member1 member2 ...
        * 返回删除元素的个数
- __zremrangebyrank__: 删除指定下标范围内的元素
    + 语法 zremrangebyrank key start end
        * 按权值从__小到大__排序, 所以下标 0 就是权值最小的元素
- __zremrangebyscore__: 删除指定权值范围内的元素
    + 语法 zremrangebyscore key min max
        * __\(__score 表示不包含 score, 参考 zrangebyscore
- __zinterstore__: 返回集合间的交集
    + 语法 zinterstore destination numkeys key1 key2 \[weight weight1 weight2 ...\] \[aggregate SUM | MIN | MAX\]
        * 返回 destination 元素的个数
        * 计算给定的一个或多个有序集的交集, 并将该交集(结果集)储存到 destination
        * 给定 key 的数量必须以 numkeys 参数指定
        * 默认情况下, destination 成员的权值为所有给定集合下该成员权值之和(可通过 aggregate 指定)
        * 可选参数 weight
            - 使用 weight 选项, 可以为每个给定集合分别指定一个乘法因子(multiplication factor), 每个给定集合的所有成员的权值在传递之前都要先乘以该集合的乘法因子
            - 如果没有指定 weight 选项，乘法因子默认设置为 1
        * 可选参数 aggregate
            - 使用 aggregate 选项，可以指定 destination 中元素权值的计算方式
            - SUM, 默认使用的参数, 即求和
            - MIN, 取所有集合中最小的权值
            - MAX, 取所有集合中最大的权值
- __zunionstore__: 返回集合间的并集
    + 参考 zinterstore

# HyperLogLog
这是 Redis 在 2.8.9 版本新添加的类型.

```
需求:
记录网站每天获得的独立 IP 数量

2.8.9 的解决方案:
使用集合来储存每个访客的 IP, 通过集合性质（集合中的每个元素都各不相同）来得到多个独立 IP,
然后通过调用 SCARD 命令来得出独立 IP 的数量.
```

使用上面的方式来解决这个问题, 随着集合记录的 ip 越来越多, 消耗的内存也会越来越大.

为了更好地解决像独立 IP 地址计算这种问题，引了 __HyperLogLog__ 类型.

HyperLogLog 可以接受多个元素作为输入, 并给出输入元素的基数估算值

- 基数
    + 集合中不同元素的数量
        * 比如 {'apple', 'banana', 'cherry', 'banana', 'apple'} 的基数就是 3
- 估算值
    + 算法给出的基数并不是精确的, 可能会比实际稍微多一些或者稍微少一些，但会控制在合理的范围之内

HyperLogLog 的__优点__是, 即使输入元素的数量或者体积非常非常大, 计算基数所需的空间总是固定
的、并且是很小的.<br>
但是, 因为 HyperLogLog 只会根据输入元素来计算基数, 而不会储存输入元素本身, 所以
HyperLogLog 不能像集合那样, 返回输入的各个元素.

__也就是说, 如果业务关心的是元素的数量而不是元素本身, 就使用 HyperLogLog__

下表列出了使用 HyperLogLog 记录不同数量的独立 IP 时，需要耗费的内存数量:

| 独立 IP 数量 |   一天  |  一个月  | 一年(使用 HyperLogLog) | 一年(使用set) |
|--------------|---------|----------|------------------------|---------------|
| 一百万       | 12 KB   | 360 KB   | 4.32 MB                | 5.4 GB        |
| 一千万       | 120 KB  | 3600 KB  | 43.2 MB                | 54 GB         |
| 一亿         | 1200 kb | 36000 KB | 432 MB                 | 540 GB        |

<br>

HyperLogLog 的具体命令请自行搜索, 不在这里记录了.

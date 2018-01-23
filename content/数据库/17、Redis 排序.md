Title: 17、Redis 排序
Author: Martin
Date: 2016-03-28 12:39
Summary: 除了现有的有序集合实现了排序, 还也可以自定义排序功能(针对 list 和 set 类型).

[TOC]

### sort key
- sort key: 对指定 key 的 value 进行排序
    + value 必须是数字, 如果是字符串, 需要用到可选参数
    + sort key 升序
    + sort key desc 降序

```redis
redis> LPUSH today_cost 30 1.5 10 8
(integer) 4
redis> SORT today_cost
1) "1.5"
2) "8"
3) "10"
4) "30"
```

### sort key alpha
- sort key alpha
    + 如果指定 key 的 value 是字符串, 需要加下 alpha 参数来进行排序
    + sort key alpha 升序
    + sort key alpha desc 降序

### sort key limit offset count
- sort key limit offset count
    + 对排序后的结果进行截取, 截取从 offset 处开始的 count 个元素
    + sort key limit offset count 升序
    + sort key limit offset count desc 降序

### sort key by
- sort key by
    + 通过外部其它 key 的 value 来排序, 前提是当前 key 中的元素与外部 key 中的 value 有某种联系
    + 如: sort uid by user\_level\_\*
        * \* 是一个占位符, 它先取出 uid 中的值, 再用这个值替换 user\_level\_\* 中的星号, 然后根据替换后的 key 的 value 来排序
        * 比如在对 uid 列表进行排序时, 就会先取出 uid 的值 2、 4、 1、 3, 然后使用 user\_level\_2、 user\_level\_4、 user\_level\_1 和 user\_level\_3 的值作为排序 uid 的权重
    + 如果 by 后面的 key 不存在, 那么就会直接返回 uid 的元素(不排序)

### sort key get
- sort key get
    + 取出与当前 key 中元素相关联的外部 key 的 value
    + 如: sort uid get user\_level\_\*
        * 先对 uid 的值进行排序, 1、2、3、4, 然后取出 user\_level\_1、 user\_level\_2、 user\_level\_3 和 user\_level\_4 的值
    + get 可以批量操作
        * sort uid __get__ user\_level\_\* __get__ user\_name\_\*
    + get __#__ 可以取出当前 key 的元素, 而不是与之关联的外部 key 的 value, 这个例子中就是 1、2、3、4

### sort key by get
- sort key by get
    + 通过组合使用 by 和 get, 可以让排序结果以更直观的方式显示出来
        * 如 sort uid by user\_level\_\* get user\_name\_\*
            - 先按 user\_level\_\{uid\} 来排序 uid 列表
            - 再取出相应的 user\_name\_\{uid\} 的值

```redis
redis 127.0.0.1:6379> sort uid by user_level_* get user_name_*
1) "jack"       # level = 10
2) "peter"      # level = 25
3) "mary"       # level = 70
4) "admin"      # level = 9999
```

现在的排序结果要比只使用 sort uid by user\_level\_\* 要直观得多

- __特殊用法__
    + 在不排序的情况下获取多个与当前 key 中元素相关联的外部 key 的 value
        * by 一个不存在的 key
        * 如 sort uid __by__ noExists __get__ user\_name\_\* __get__ user\_level\_\*
            - 先按 noExists 来排序 uid 列表
                + 因为 noExists 不存在, 所以不排序, 直接返回当前 uid 列表
            - 再取出相应的 user\_name\_\{uid\} 的值
        * 功能相当于 mysql 中的联结查询

### get/by hash
上面介绍的 get 和 by 参数, 其外部 key 还可以是 hash, 其语法类似指针.

假设 user\_1、user\_2、user\_3 都保存的是 hash, 该 hash 中的 field 是 level, 现在想根据 hash 中的 level 来排序, 可以这么写:

```
sort uid by user_*->level
```

### sort key store destination
- sort key store destination
    + 将排序结果保存在 destination 中

### 注意事项
sort 命令较耗内存, 其时间复杂度为 O(N+M*log(M)), N 为要排序的列表或集合内的元素数量, M 为要返回的元素数量

- 尽可能地减少待排序 key 中 List/Set 的长度 (减小 N)
- 擅用 limit 参数 (减少 M)

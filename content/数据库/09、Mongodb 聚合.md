Title: 09、Mongodb 聚合
Author: Martin
Date: 2016-04-12 13:26
Summary: MongoDB 中聚合(aggregate)主要用于处理数据(如统计平均值、求和等), 并返回计算后的数据结果.

MongoDB 中聚合(aggregate)主要用于处理数据(如统计平均值、求和等), 并返回计算后的数据结果, 这样我们就可能利用 Mongdb 直接去处理一些数据, 而不用先把数据拿到本地再运算.

[TOC]

# 1. count
count 是最简单的聚合工具, 返回集合中的 Document 数量.

```js
db.col.count()
0
db.col.insert({'x': 1})
db.col.count()
1
db.col.insert({'x': 2})
db.col.count()
2
```

count 和 find 一样, 也接受条件:

```js
db.col.count({'x': 1})
1
```

从结果可以看出，只有符合条件的文档参与了计算.

# 2. distinct
distinct 用来统计集合中给定 key 所有不同的值.

插入 4 条测试数据(请留意Age字段):

```js
db.test.insert({'name': 'Ada', 'age': 20})
db.test.insert({'name': 'Fred', 'age': 35})
db.test.insert({'name': 'Andy', 'age': 35})
db.test.insert({'name': 'Susan', 'age': 60})
```

distinct 命令必须指定集合名称和需要统计的字段, 如: age

```js
db.runCommand({"distinct":"test", "key":"age"})
{
        "values" : [
                20,
                35,
                60
        ],
        "stats" : {
                "n" : 4,
                "nscanned" : 4,
                "nscannedObjects" : 4,
                "timems" : 0,
                "cursor" : "BasicCursor"
        },
        "ok" : 1
}
```


# 3. group
## 3.1 group 基础
group 聚合工具有些复杂:<br>
先选定分组所依据的键, 此后 MongoDB 就会将集合中的数据, 依据 __选定键的值的不同__ 分成若干组(即选定键的值相同的为一组), 然后可以通过聚合(运算)每一组内的文档, 产生一个结果文档.

> 有点类似 _05、Mongodb Cursor_ 中提到的 __forEach()__ 方法和 __map()__ 方法, 不同的是 group 会先根据指定 key 对要聚合的 Documents 进行分组, 而且它的运算也更复杂.

先插入一点测试数据:

```js
db.test.insert({'day': '2016-04-20', 'time': '2016-04-20 03:20:40', 'price': 4.23})
db.test.insert({'day': '2016-04-21', 'time': '2016-04-21 11:28:00', 'price': 4.27})
db.test.insert({'day': '2016-04-20', 'time': '2016-04-20 05:00:00', 'price': 4.10})
db.test.insert({'day': '2016-04-22', 'time': '2016-04-22 05:26:00', 'price': 4.30})
db.test.insert({'day': '2016-04-21', 'time': '2016-04-21 08:34:00', 'price': 4.01})
```

我们先分析下这几条测试数据:<br>
根据 __day__ 的不同, 上面插入的测试数据可以分为三组, 即: '2016-04-20'、'2016-04-21' 和 '2016-04-22', 然后:<br>
__'2016-04-20'__ 这一组里, __time__ 最新的为 __'2016-04-20 05:00:00'__<br>
__'2016-04-21'__ 这一组里, __time__ 最新的为 __'2016-04-21 11:28:00'__<br>
__'2016-04-22'__ 这一组里, __time__ 最新的为 __'2016-04-22 05:26:00'__<br>

那么, Mongodb 的 __group__ 工具就可以完成上面的这种功能.<br>
可以将 __day__ 作为 __group__ 的分组键, 然后取出 __time__ 键值为最新时间的文档, 同时也取出该文档的 __price__ 键值.

```js
db.test.group({
    'key': {'day': true}, // 如果是多个字段, 可以为 {'f1': true,'f2': true}
    'initial': {'time': '0'}, // initial 表示 $reduce 函数参数 prev 的初始值
    '$reduce': function(doc, prev) { // $reduce 方法接受两个参数, doc 正在迭代的当前 document, prev 表示上一次迭代的结果 document
        if (doc.time > prev.time) {
            prev.day = doc.day;
            prev.price = doc.price;
            prev.time = doc.time;
        }
    }
})

// 下面是 group 的返回结果, 可以看到就是 $reduce 方法中最终 prev 的数据
[
    {
        'day': '2016-04-20',
        'time': '2016-04-20 05:00:00',
        'price': 4.1
    },
    {
        'day': '2016-04-21',
        'time': '2016-04-21 11:28:00',
        'price': 4.27
    },
    {
        'day': '2016-04-22',
        'time': '2016-04-22 05:26:00',
        'price': 4.3
    }
]
```


在某些时候, 你还可以使用 __condition__ 参数 (也可以用 __cond__ 参数 或者 __q__ 参数, 功能是一样的) 来过滤要运算的文档, 就像 __find()__ 方法的 __query__ 一样.

例如, 我现在只想运算 __price > 4.1__ 的文档:

```js
db.test.group({
    'key': {'day': true},
    'initial': {'time': '0'},
    '$reduce': function(doc, prev) {
        if (doc.time > prev.time) {
            prev.day = doc.day;
            prev.price = doc.price;
            prev.time = doc.time;
        }
    },
    'condition': {'price': {'$gt': '4.1'}} // 只运算 price > 4.1 的文档
})
```

## 3.2 完成器
通过上面已经知道 __group__ 工具最终会返回一个结果文档, 但有的时候, 我们可能不需要整个结果文档, 而是需要对这个结果再运算, 然后得到一个值, 可以是字符串, 可以是数字, 我们只想要这个结果值, 那怎么办?<br>
或者有的时候, 我们是想要在结果文档中添加一个新字段, 那又该怎么办?

__group__ 工具的 __finalize__ (完成器) 参数就是用来对 __group__ 返回的结果文档再加工的...

```js
db.test.group({
    key: { day: true},
    initial: {count: 0},
    reduce: function(obj, prev) {
        prev.count++;
    },
    finalize: function(out) { // $finalize 方法接受一个参数, 即 $reduce 返回的结果文档, 这里做测试用, 仅在结果文档中新增一个键
        out.scaledCount = out.count * 10
    }
})

[
    {
        "day" : "2012-08-20",
        "count" : 2,
        "scaledCount" : 20
    },
    {
        "day" : "2012-08-21",
        "count" : 2,
        "scaledCount" : 20
    },
    {
        "day" : "2012-08-22",
        "count" : 1,
        "scaledCount" : 10
    }
]
```

## 3.3 将函数做为分组依据
在 3.1 和 3.2 中我们都是用 __day__ 来做为分组依据的, 但在某些情况下, 单纯的使用字段来做为分组依据可能实现不了我们实际想要的功能.

例如, 假设存在一个保存了文章列表的集合, 集合里面有个 __tag__ 字段, 用来标识文章的标签, 此时我们应该忽略 tag 值的大小写, 因为 AAA 和 aaa 表示的都是同一个标签...但如果直接用 __tag__ 做分组依据, AAA 和 aaa 就会被分为不同组....

为了消除这个问题, 就要定义一个__函数__来确定文档分组的依据, 定义分组函数要用到 __$keyf__, 注意, 不是 __key__.

```js
db.blog.group({
    '$keyf' : function(x) { // $keyf 方法接收一个参数, 表示当前集合的文档, 要返回一个值, 表示分组依据, 这里就把 tag 转成小写后的 值做为分组依据
        return x.tag.toLowerCase();
    },
    ......
})
```


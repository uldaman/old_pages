Title: 04、Mongodb 索引
Author: Martin
Date: 2016-04-08 18:32
Summary: 本节笔记记录 Mongodb 索引(index) 的设计, 让操作数据库获得更好的性能.

本节笔记记录 Mongodb 索引(index) 的设计, 让操作数据库获得更好的性能.

[TOC]

索引的重要性可参考字典的设计, 如想要在新华字典中找某一个字, 可以先在字典的索引区找到这个字的页码, 这种功能就相当于数据库中的索引, 可以很方便的让你索引到数据库中的数据.

所有的 MongoDB 集合默认都有一个唯一索引在字段 __\_id__ 上, 如果应用程序没有为 __\_id__ 列定义一个值, MongoDB 将创建一个带有 ObjectId 值的列.

## 创建索引
__ensureIndex()__ 方法可以创建一个新的索引.

```
db.COLLECTION_NAME.ensureIndex({KEY: 1})
```

语法中 Key 值为你要创建的索引字段, __1__ 为指定按升序创建索引, 如果你想按降序来创建索引指定为 __-1__ 即可.

__复合索引__

__ensureIndex()__ 方法中也可以设置使用多个字段创建索引(关系型数据库中称作复合索引), 如:

```
db.col.ensureIndex({'title': 1, 'description': -1})
```

该索引被创建后, 基于 __title__ 和 __description__ 的查询将会用到该索引, 或者是基于 __title__ 的查询也会用到该索引, 但是只是基于 __description__ 的查询将不会用到该复合索引;<br>
因此可以说, 如果想用到复合索引, 必须在查询条件中包含复合索引中的前 N 个索引列...

ensureIndex() 接收__可选参数__

|     Parameter      |      Type     |                                                                 Description                                                                  |
|--------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| background         | Boolean       | 建索引过程会阻塞其它数据库操作, background 可指定以后台方式创建索引, 即增加 "background" 可选参数.  "background" 默认值为 false.             |
| unique             | Boolean       | 建立的索引是否唯一. 指定为 true 创建唯一索引. 默认值为 false.                                                                                |
| name               | string        | 索引的名称. 如果未指定, MongoDB 会通过连接索引的字段名和排序顺序(1/-1)生成一个索引名称.                                                      |
| dropDups           | Boolean       | 在建立唯一索引时是否删除重复记录, 指定 true 创建唯一索引. 默认值为 false.                                                                    |
| sparse             | Boolean       | 对文档中不存在的字段数据不启用索引; 这个参数需要特别注意, 如果设置为 true 的话, 在索引字段中不会查询出不包含对应字段的文档.. 默认值为 false. |
| expireAfterSeconds | integer       | 指定一个以秒为单位的数值, 完成 TTL 设定, 设定集合的生存时间.                                                                                 |
| v                  | index version | 索引的版本号. 默认的索引版本取决于 mongod 创建索引时运行的版本.                                                                              |
| weights            | document      | 索引权重值, 数值在 1 到 99,999 之间, 表示该索引相对于其他索引字段的得分权重.                                                                 |
| default_language   | string        | 对于文本索引, 该参数决定了停用词及词干和词器的规则的列表.  默认为英语                                                                        |
| language_override  | string        | 对于文本索引, 该参数指定了包含在文档中的字段名, 语言覆盖默认的language, 默认值为 language.                                                   |

## 查询索引
__getIndexes()__ 该当可以查询当前已有的索引信息, 以之前创建的 col 集合为例:

```
db.col.getIndexes()
[
        {
                "v" : 1,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "runoob.col"
        }
]
```


返回值分析:

- v: 索引的版本号, 暂时发现无叼用
- key: 索引对应的 field, 后面的数字表示排序
- name: 索引的名称, 如果未指定, MongoDB 会通过连接索引的字段名和排序顺序(1/-1)生成一个索引名称
- ns: 索引所属的数据库和集合

## 删除索引
__dropIndex()__ 方法用来删除索引

- db.tab.dropIndex(<indexname\>) 删除指定索引, 有两种方式
    + db.tab.dropIndex('age\_1') age\_1 为 getIndexes() 看到的 name
    + db.tab.dropIndex({age: 1}) {age: 1} 为创建索引时的参数
- db.tab.dropIndexes() 删除所有索引

## explain
explain() 方法是一个对查询非常有用的工具, 可以用来查看查询命令的详情, 例如是否使用了索引、消耗了多久, 以及扫描了多少文档才得到结果.

先看一个没有走索引的例子:

```js
db.col.find().explain()
{
    "cursor": "BasicCursor",
    "indexBounds": [],
    "nscanned": 64,
    "nscannedObjects": 64,
    "n": 64,
    "millis": 0,
    "allPlans": [
        {
            "cursor": "BasicCursor",
            "indexBounds": []
        }
    ]
}
```

重点返回值:

- cursor: BasicCursor, 这个表示没有使用索引, 等下会演示下使用了索引的情形.
- nscanned: 64, 数据库查找了多少个文档
- n: 64, 返回了多个少文档, 即查询结果
- millis: 0, 耗时

```js
db.col.find({age: {$gt: 20, $lt: 30}}).explain()
{
    "cursor": "BtreeCursor age_1",
    "indexBounds": [
        [
            {
                "age": 20
            },
            {
                "age": 30
            }
        ]
    ],
    "nscanned": 14,
    "nscannedObjects": 12,
    "n": 12,
    "millis": 1,
    "allPlans": [
        {
            "cursor": "BtreeCursor age_1",
            "indexBounds": [
                [
                    {
                        "age": 20
                    },
                    {
                        "age": 30
                    }
                ]
            ]
        }
    ]
}

```

重点返回值:

- cursor: BtreeCursor age\_1, 表示使用了索引 age\_1
- allPlans: 包含所有可能用到的索引尝试, 这个例子很明确的表示只有 age\_1 可用

## hint
hint() 方法可以强制查询使用某个索引, 这在需要指定搜索顺序时比较有用.

假设已有 {'username': 1, 'age': 1} 和 {'age': 1, 'username': 1} 两个索引, 你可以通过 hint() 指定使用哪条索引, 通常 Mongodb 自身会帮你选择.

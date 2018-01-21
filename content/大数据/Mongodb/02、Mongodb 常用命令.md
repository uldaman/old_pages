Title: 02、Mongodb 常用命令
Author: Martin
Date: 2016-04-08 12:46
Summary: 本节笔记记录 Mongodb 的常用命令, 包括创建数据库(文档)、删除数据库(文档) 以及增删改查.

本节笔记记录 Mongodb 的常用命令, 包括创建数据库(文档)、删除数据库(文档) 以及增删改查.

[TOC]

首先, 要先进入 Mongodb Client 交互环境:

```
> mongo
MongoDB shell version: 3.0.6
connecting to: test
...
```
<br>

## 创建数据库(文档)
**命令格式:**

```
use DATABASE_NAME
```
<br>
如果数据库不存在, 则创建数据库并切换过去, 否则直接切换到指定数据库.

**实例:**

```
> use runoob
switched to db runoob
> db
runoob
>
```
<br>
现在我们创建一个新数据库 runoob, 然后 db 命令查看当前所在的数据库, 就会当前环境看到已经切换到 runoob 数据库中了..

使用 **show dbs** 命令可以查看所有已存在的数据库:

```
> show dbs
local  0.078GB
test   0.078GB
>
```
<br>
但是, 我们发现刚创建的数据库 runoob 并不在数据库的列表中, 要显示它, 我们需要向 runoob 数据库插入一些数据, 关于如何插入数据, 请参考下面的笔记.

## 删除数据库(文档)
**命令格式:**

```
db.dropDatabase()
```
<br>
删除当前所在数据库

**实例:**<br>
首先, 查看所有数据库:

```
> show dbs
local   0.078GB
runoob  0.078GB
test    0.078GB
```
<br>
切换到待删除数据库 runoob:

```
> use runoob
switched to db runoob
>
```
<br>
执行删除命令:

```
> db.dropDatabase()
{"dropped": "runoob", "ok": 1}
```
<br>
最后, 再通过 show dbs 命令数据库是否删除成功:

```
> show dbs
local  0.078GB
test   0.078GB
>
```
<br>

## 插入数据
**命令格式:**<br>
MongoDB 使用 **insert()** 或 **save()** 方法向**集合**中插入文档:

```
db.COLLECTION_NAME.insert(document)
```
<br>
这里提到一个**集合** 和 **document** 的概念.

什么是**集合**?<br>
用常规的思维来说, **集合**对应的就是数据库中的**表**, 当我们插入数据的时候, 是向"表"中插入数据.<br>
现在可以总结出 Mongodb 与 MySQL 对照关系如下:

| Mongodb | MySQL  |
|---------|--------|
| 文档    | 数据库 |
| 集合    | 表     |

OK, 现在知道什么是**集合**了, 那什么是 **document**?

- 文档的数据结构和 JSON 基本一样
- 所有存储在集合中的数据都是 **BSON** 格式
    + BSON 是类 json 的一种二进制形式的存储格式, 即 Binary JSON

对于常用 Python 的我来说, 更喜欢把它说成是一种 **Dict** 结构.

**实例:**<br>
首先, 创建一个新数据库:

```
> use runoob
switched to db runoob
> db
runoob
>
```
<br>
然后向 **runoob** 数据库的 **col** 集合中插入数据:

```
>db.col.insert({name: 'MongoDB 教程', age: 18})
```
<br>
**col** 是我们的集合名, 如果该集合不在当前所处的数据库中, MongoDB 会自动创建该集合并插入文档.

MongoDB 数据中的**字段都是字符串格式的**, 但是 MongoDB 做了优化, 通常我们可以可以省略引号.

每个已插入的数据, MongoDB 都会为它分配一个 **\_id** 字段, 当然, 也可以在插入数据时**显示**的指定 **\_id** 字段, 但是要注意, **\_id** 字段是不可重复的, 如果使用 **insert()** 插入相同 **\_id** 的数据, 会报错, 不过可以使用 **save()** 方法:

- 如果不指定 **\_id** 字段 save() 方法类似于 insert() 方法
- 如果指定 **\_id** 字段, 则会更新该 **\_id** 的数据
    + 如果指定 **\_id** 不存在, 也类似于 insert() 方法

现在可以通过 **find()** 命令查看已插入的数据, 关于**查询**的命令详细用法请继续参考下面的笔记, 这里仅测试下 **\_id** 字段...

```
> db.col.find()
{"_id": ObjectId("56064886ade2f21f36b03134"), "name": "MongoDB 教程", "age": 18}
>
```
<br>
可以看到刚才插入的数据有了一个 **\_id** 字段, 使用该字段可以对数据进行 删、改、查.

## 删除文档
**remove()** 方法用来移除集合中的数据

**命令格式:**

```
db.collection.remove(
   {query},
   {justOne}
)
```
<br>

参数说明:

- query: 匹配条件条件, 如 {name: '张三'}
- justOne: 可选, 如果设为 true 或 1, 则只删除一个文档, 默认删除所有匹配文档, 如 {justOne: true}

如果想删除所有数据, 可以使用以下方式:

```
db.col.remove({})
```
<br>
## 修改数据
可以使用 **update()** 和 **save()** 方法来更新集合中的文档.

- **update()** 用于更新已存在的文档, 当然它也支持插入新文档, 但它的本质还是更新
- **save()** 通过传入的文档来替换已有文档, 它的本质是用新文档覆盖掉旧文档

**update()**<br>

```
db.collection.update(
   {query},
   {update},
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```
<br>
参数说明:

- query: 匹配条件, 直接写 {} 表示匹配所有
- update: 更新内容, 支持多种操作符
    + $set: {$set: {field: value}} 为 field 设置新值, 如果 field 不存在, 则为文档添加 field
    + $unset: {$unset: {field: value}} 删除 field, 这里 value 为 true 或 1
    + $inc: {$inc: {field: value}} field 的值加上 value, 支持负数
    + $max: {$max: {field: value}} 增量修改, 只有 value 大于原有的 value 时, 才会修改成功
    + $min: {$min: {field: value}} 减量修改, 只有 value 小于原有的 value 时, 才会修改成功
    + $rename: {$rename: {old\_field\_name: new\_field\_name}} 字段重命名
    + $setOnInsert: {$setOnInsert: {field: value}} 只有当是新插入时才执行, 所以要配合 upsert 使用
- upsert: 可选, {upsert: bool} 如果匹配失败, 是否插入新数据, 默认是 false, 不插入
- multi: 可选, {multi: bool} 是否更新多条数据, 默认是 false, 只更新找到的第一条记录, 如果这个参数为 true, 就把按条件查出来多条记录全部更新
- writeConcern: 可选, 抛出异常的级别

**save()**<br>

```
db.collection.save(
   {document},
   {
     writeConcern: <document>
   }
)
```
<br>
参数说明:

- document: 文档数据
- writeConcern: 可选, 抛出异常的级别

## 查询数据
### 基础查询
**命令格式:**<br>
MongoDB 使用 **find()** 或 **findOne()** 方法从**集合**中插查询数据:

```
>db.COLLECTION_NAME.find()
>db.col.find().pretty()
```
<br>
find() 方法以**非结构化**的方式来显示所有文档, 如果需要以易读的**结构化**方式来读取数据, 可以使用 **pretty()** 方法.

**实例**<br>
查询 col 集合中的数据:

```
> db.col.find().pretty()
{
        "_id" : ObjectId("56063f17ade2f21f36b03133"),
        "name": "MongoDB 教程",
        "age": 18
}
```
<br>
细心同学可能已经发现, 上面查询结果中字段都是**字符串**格式(\_id、name、age 都用引号包起来了).

### 过滤返回字段
通过 find() 的第二个参数可以指定返回的字段.

例如, 只想返回 name 字段:

```
> db.col.find({}, {'name': 1}).pretty()
{
        "_id" : ObjectId("56063f17ade2f21f36b03133"),
        "name": "MongoDB 教程",
}
```
<br>
注意, \_id 总是返回的.

或者指定哪些字段不返回:

```
> db.col.find({}, {'_id': 0}).pretty()
{
        "name": "MongoDB 教程",
        "age": 18
}
```
<br>
可以看到, 这种方式可以过滤掉 \_id 字段.

### 条件查询
MongoDB 的 **find()** 和 **findOne()** 都支持条件语句的查询, 它们与 SQL 语句的对应关系如下表:

> 注意, MongoDB 的条件也是 document 类型(Dict)

|   操作   |            格式           |                    范例                    |           SQL           |
|----------|---------------------------|--------------------------------------------|-------------------------|
| 等于     | {<key\>: <value\>}        | db.col.find({'name': '菜鸟教程'}).pretty() | where name = '菜鸟教程' |
| 小于     | {<key\>: {$lt:<value\>}}  | db.col.find({'age': {$lt:50}}).pretty()    | where age < 50          |
| 小于等于 | {<key\>: {$lte:<value\>}} | db.col.find({'age': {$lte:50}}).pretty()   | where age <= 50         |
| 大于     | {<key\>: {$gt:<value\>}}  | db.col.find({'age': {$gt:50}}).pretty()    | where age > 50          |
| 大于等于 | {<key\>: {$gte:<value\>}} | db.col.find({'age': {$gte:50}}).pretty()   | where age >= 50         |
| 不等于   | {<key\>: {$ne:<value\>}}  | db.col.find({'age': {$ne:50}}).pretty()    | where age != 50         |

<br>
### 嵌套条件查询
因为 MongoDB 中存储的数据是 document(Dict), 所以有些 key 中保存的 value 可能是另一个 document(Dict), 此时, 我们可以用**嵌套条件**来查询到嵌套在 value 中的子 document(Dict), 语法格式就是**点号**.

先插入一条嵌套数据:

```
>db.col.insert({name: '张三', age: 18, school: {name: '交通大学', city: '上海'}})
```
<br>
如果想要根据学校名字来查询数据, 就可以用下面这种嵌套条件:

```
db.col.find({'school.name': '交通大学'}).pretty()
```
<br>
### 不包含字段查询
这种查询是查询集合中**没有某个字段**的数据.

先插入两条数据:

```
>db.col.insert({name: '张三', age: 18)
>db.col.insert({name: '李四')
```
<br>
现在需求查询没有 age 字段的数据, 方法如下:

```
>db.col.find({'age': {$exists:false}})
```
<br>
### 复合条件查询

#### OR 条件
OR 条件语句使用了关键字 **$or**, 语法格式如下:

```
>db.col.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```
<br>
#### IN 条件
in 条件语句, 也是一种或者逻辑, 使用了关键字 **$in**, 但它与 or 不同, or 是在不同的 field 之间或者, 而 in 是在同一个 field 间或者, 并且支持对**数组**型元素进行查询

```
>db.col.find({key1: {$in: [value1, value2]}}).pretty()
```
<br>
匹配 key1 的值为 value1 或者 value2 的元素, 或者匹配包含有 value1 / value2 的数组元素.

#### AND 条件
OR 条件语句可以使用了关键字 **$and**, 也可以直接在条件 document 中可以传入多个键(key), 每个键(key)以**逗号**隔开.

```
>db.col.find(
   {
      $and: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()


>db.col.find({key1:value1, key2:value2}).pretty()
```
<br>
#### ALL 条件
ALL 条件用来对数组中的元素进行全匹配, 使用了关键字 **$all**.

```
>db.col.find({key1: {$all: [value1, value2]}}).pretty()
```
<br>
首先, key1 要是个数组, 如 [value1, value2 ...]<br>
该语句匹配同时包含元素 value1 和 value2 的数组.

#### 正则查询
MongoDB 的查询也是支持正则的, 但是正则查询的效率是比较低的, 建议只对建立了索引的 field 进行正则.

#### 投影
投影意思是只查询必要的字段而不是查询所有的字段, 例如一个文档有 5 个字段, 需要显示的只有 3 个, 此时就可以用投影.

find() 方法的第二个可选参数是要投影的字段列表, 在该参数中设置的字段列表值 1 或 0

- 1 用来显示字段
- 0 用来隐藏字段

语法:
find() 方法具有投影基本语法如下

```
db.COLLECTION_NAME.find({}, {KEY1: 1, KEY1: 0})
```
<br>
请注意 **\_id** 字段始终显示, 如果不想这个字段, 那么需要将其设置为 0:

```
db.COLLECTION_NAME.find({}, {KEY: 1, _id: 0})
```
<br>
#### 分页
MongoDB 的分页功能需要用到两个方法: **Limit()** 和 **Skip()**

##### Limit()
limit() 方法接受一个数字参数, 该参数指定读取的记录条数.

```
db.COLLECTION_NAME.find().limit(number)
```
<br>
##### Skip()
skip() 方法用来跳过指定数量的数据, skip() 方法同样接受一个数字参数作为跳过的记录条数

```
db.COLLECTION_NAME.find().skip(number)
```
<br>
配合 **Limit()** 和 **Skip()** 就能实现分页查询的功能, 例如每页面显示 10 条数据, 想显示第 5 页的数据:

```
db.COLLECTION_NAME.find().skip(4 * 10).limit(10)
```
<br>
#### 排序
**命令格式:**

```
db.COLLECTION_NAME.find().sort({KEY: 1})
```
<br>
Key 可以设为 1 或者 -1, 1 用于升序排列, 而 -1 用于降序.

**注意:** 排序是一个耗性能的操作, 建议只对建立了**索引**的 key 进行排序.

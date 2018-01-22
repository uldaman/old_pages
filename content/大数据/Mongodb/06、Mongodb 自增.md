Title: 06、Mongodb 自增
Author: Martin
Date: 2016-04-09 23:34
Summary: MongoDB 原生是没有 SQL 那种可以让 Field 自动增长的功能, 在某些情况下, 可能需要这样的功能, 好在 MongoDB 官方给出解决方案, 可以让 MongoDB 的 Field 自动增长.


MongoDB 原生是没有 SQL 那种可以让 Field 自动增长的功能, 在某些情况下, 可能需要这样的功能, 好在 MongoDB 官方给出解决方案, 可以让 MongoDB 的 Field 自动增长.

[官方参考文档](https://docs.mongodb.org/manual/tutorial/create-an-auto-incrementing-field/)

这篇笔记我只个搬运工...

官方提供了两种方法 __Use Counters Collection__ 和 __Optimistic Loop__, 以 \_id 为例来说明下这两种方法.

[TOC]

##  Use Counters Collection
1\. Insert into the counters collection, the initial value for the userid:

```javascript
db.counters.insert(
   {
      _id: "userid",
      seq: 0
   }
)
```


2\. Create a __getNextSequence__ function that accepts a name of the sequence. The function uses the findAndModify() method to atomically increment the seq value and return this new value:

```javascript
function getNextSequence(name) {
   var ret = db.counters.findAndModify(
          {
            query: { _id: name },
            update: { $inc: { seq: 1 } },
            new: true // true 表示返回 update 后的结果, false 表示返回 update 前的结果
          }
   );

   return ret.seq;
}
```


3\. Use this __getNextSequence()__ function during insert().

```javascript
db.users.insert(
   {
     _id: getNextSequence("userid"),
     name: "Sarah C."
   }
)

db.users.insert(
   {
     _id: getNextSequence("userid"),
     name: "Bob D."
   }
)
```

## Optimistic Loop
1\. Create a function named __insertDocument__ that performs the "insert if not present" loop. The function wraps the insert() method and takes a __doc__ and a __targetCollection__ arguments.

```js
function insertDocument(doc, targetCollection) {

    while (1) {

        var cursor = targetCollection.find( {}, { _id: 1 } ).sort( { _id: -1 } ).limit(1);

        var seq = cursor.hasNext() ? cursor.next()._id + 1 : 1;

        doc._id = seq;

        var results = targetCollection.insert(doc);

        if( results.hasWriteError() ) {
            if( results.writeError.code == 11000 /* dup key */ )
                continue;
            else
                print( "unexpected error inserting data: " + tojson( results ) );
        }

        break;
    }
}
```


2\. Use the __insertDocument()__ function to perform an insert:

```js
var myCollection = db.users2;

insertDocument(
   {
     name: "Grace H."
   },
   myCollection
);

insertDocument(
   {
     name: "Ted R."
   },
   myCollection
)
```


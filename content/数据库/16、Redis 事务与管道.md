Title: 16、Redis 事务与管道
Author: Martin
Date: 2016-03-28 12:38
Summary: 事务可以理解为一个打包的批量执行脚本, 将一串的命令发送给 redis 排队, 等待 redis 去执行.

[TOC]

# 事务
事务可以理解为一个打包的批量执行脚本, 将一串的命令发送给 redis 串行化地执行.

需要注意的是, redis 的事务要么不执行, 要执行就一定会执行完, 哪怕中间某条命令出错, 它也不会暂停或者回滚, 而是继续向后执行剩下的命令, 所以在事务执行的过程中, 是不能得到返回值的, 要等到 redis 执行完这个事务后一次性返回.

## multi
__multi__: 开启事务, 事务块中的多条语句会按照顺序放入对列中

![](http://i63.tinypic.com/1sbaeh.jpg)

执行 multi 后, 进入事务模式, 后面输入的所有命令都会被放入队列当中, 直到运行 exec/discard 命令.

## exec
__exec__: 执行队列中的事务

![](http://i64.tinypic.com/2wg6rfc.jpg)

执行完事务后, 一次性返回所有命令的结果.

## discard
__discard__: 取消事务, 放弃执行事务块内的所有命令.

## watch/unwatch
__watch__: 监视一个或多个 key, 如果在执行事务之前, 这个 key 如果被其它客户端改动, 那么执行 exec 时会返回 nil(相当于事务被取消了).

所谓的监视, 就是要保证, 在执行事务前, 没有其他客户端更改我们监视的 key.

__unwatch__: 取消对所有 key 的监视, 需要注意, 如果 watch 后, exec/discard 了事务, 那么相当于自动 unwatch 了, 不需要再次 unwatch.

## 错误处理
### 语法错误
如, 命令不存在, 参数错误等等, 这种情况下, exec 后, 会直接返回错误, 事务不会被执行.

### 运行时错误
事务开启后, 一定会执行完, 中间某条命令出错, 也不会暂停或者回滚, 而是继续向后执行剩下的命令, 等到全部执行完后, 才看得到错误信息.

# 管道
pipelining: 管道, 可以理解成阉割版的事务

事务具有原子性, 一个事务中的命令要么都执行, 要么都不执行. 即可以说:<br>
__事务同命令一样, 都是 Redis 的最小执行单位__

而管道, 它也可以一次性发送多条命令, 并在执行完后一次性将结果返回, 管道通过减少客户端与 Redis 的通信次数来实现降低往返时延, __但它不具备原子性__.

Redis 本身没有提供 pipelining 相关的命令, 它由使用 Redis 的客户端程序决定, 如 __redis-py__

```python
import redis
r = redis.StrictRedis(host = '127.0.0.1', port = 6379, db = 0)

pipe = r.pipeline() # 此为事务, 管道的使用方式和事务相同, 创建时加上参数 transaction = False
pipe.set('foo', 'bar')
pipe.get('foo')
result = pipe.execute()

print result # [True, 'bar']
```

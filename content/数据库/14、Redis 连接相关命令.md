Title: 14、Redis 连接相关命令
Author: Martin
Date: 2016-03-28 12:36
Summary: 连接相关的命令大多用来测试客户端与服务端的连接情况.

- ping
    + 测试与服务器是否有效, 有效则返回  PONG
- echo
    + 打印信息, 功能同上
- quit/exit
    + 请求服务器关闭与当前客户端的连接
- shutdown
    + 请求关闭服务器
- select index
    + 切换到指定的数据库, 数据库索引号 index 用数字值指定, 以 0 作为起始索引值, 默认使用 0 号数据库.
- auth
    + 身份验证, 如果服务器设置了 requirepass(获取客户端动态 config set requirepass), 那么就需要使用 auth 命令来进行认证后, 才能继续操作
    + 也可以在客户端连接时就指定密码, redis-cli -a pwd

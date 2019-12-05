Title: 配置 SSH 免密码登录
Author: HanXiao
Date: 2016-11-03 22:30

![]({filename}/images/SSH/免密码登录原理.png)

`cd ~
` 进入根目录

`ls -la
` 查看下当前目录文件, 可以看到有个隐藏的 `.ssh` 文件夹 (点开头就是隐藏的)

`cd .ssh/
` 进入 `.ssh` 目录, `ls` 一下, 看看该目录下有没有 `id_rsa`、`id_rsa.pub` 两个文件, 如果没有, 就生成一对:
`ssh-keygen -t(加密类型) rsa`
--四个回车--
然后就会在 `.ssh` 下生成两个文件 `id_rsa`、`id_rsa.pub`

`cp id_rsa.pub authorized_keys`
此时不需要密码就能启动/停止 hadoop 了...

如果要向其他主机发送自己的公钥: `ssh-copy-id xxx(ip)`

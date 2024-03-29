Title: Github 常用功能
Author: HanXiao
Date: 2017-08-26 21:28

[TOC]

# Watch、star、fork
![]({static}/images/github/watch.png)

如上图所示, 每个 github 项目的右上角, 都有三个按钮: `Watch`、`star`、`fork`.

## Watch
这个单词在调试程序时经常遇到, 意为监视, 当把某个变量添加到监视后, 就可以实时看到变量的值的变化.

Github 中的 `Watch` 也是类似的功能, 当你监视某个项目后, 如果项目发生变动, 如有人提交了 pull request、发起了 issue 等等情况, 都会在自己的个人通知中心收到一条通知消息, 如果设置了个人邮箱, 那么还可能收到相应的邮件.

点击 `Watch` 按钮后会出现三个选项:

- Not watching, 不监视, 将不会收到与我无关的通知, 只会关注与我有关的动态 (我发起的、主动参与的或被 @ 的)
- Watching, 监视, 关注这个项目的所有动态
- Ignoring, 彻底忽略这个项目的动态, 那意味着连与我有关的重要消息也收不到了

通常只会在 `Not watching` 和 `Watching` 中选择.

## star
集`点赞`与`收藏`功能于一体...

点击 github 个人头像, 选择 `your stars` 可以查看 `star` 过的列表.

然后就没啥好说的了...

## fork
当对别人的项目进行 `fork` 后, 就会在自己的仓库生成一份源项目的拷贝, 当然这个拷贝只是 `fork` 发生时的项目文件, 如果后续源项目文件发生改变, 必须通过 [pull request](http://www.smallcpp.cn/%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/Github%20%E5%B8%B8%E7%94%A8%E5%8A%9F%E8%83%BD.html#pull-request) 去同步.

`fork` 应该只在需要对开源项目做贡献时才使用, 很多人会把 `fork` 当成收藏，这是不对的, 收藏应该使用 [star](http://www.smallcpp.cn/%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/Github%20%E5%B8%B8%E7%94%A8%E5%8A%9F%E8%83%BD.html#star) 功能.

`fork` 别人的源项目后, 应该谨遵 [pull request](http://www.smallcpp.cn/%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/Github%20%E5%B8%B8%E7%94%A8%E5%8A%9F%E8%83%BD.html#pull-request) 的建议去贡献自己的代码.

# issue
![]({static}/images/github/issues.png)

问题列表, 可当该项目的 **todolist** 使用, 可以选择 issue 的类型, 如 feature、bug 等.

另外，在 commit 中可以通过 `#issue_id` 与某个 issue 关联, 比如 `commit message title, #1`, 还可以指定对 issue 的操作:

- `commit message title, closed #1`
- `commit message title, fixed #1`
- `commit message title, resolved #1`

不过在此之前, 需要检查下你的 Github 的注册邮箱与 `git config --list` 中设置的 `user.email` 是否一致, **只有一致了才能通过 commit 操作 issue**, 如果不一致, 需要设置下:

```
git config --global user.email "email@example.com"

# 如果设置了 config --local, 则需要再检查下
git config --local user.email "email@example.com"
```

issue 中还可以通过指定 `Assignee` 则可以将 issue 分配到某位项目成员身上, 为**团队协作**提供可能.

最后, issue 是开放的, 作为一个路人, 你可以通过 issue 给别人的项目提 bug.

# Pull Request
> 首先, 要注意一点, 对于 fork 的项目, 最好永远不要直接在 master 分支上进行修改, 因为 fork 的源项目随时会发生更改, 当收到 fork 源更新的通知时, 需要在自己的仓库发起同步 Pull Request, 如果之前直接在 master 上修改了代码, 此时就会出现冲突问题. 所以在 master 分支上应该只用来发起同步 Pull Request.

当 [fork](http://www.smallcpp.cn/%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/Github%20%E5%B8%B8%E7%94%A8%E5%8A%9F%E8%83%BD.html#fork) 了一个开源项目后, 应该:

- clone 自己仓库的项目到本地
- 在本地仓库中新建一个专门的开发分支进行修改
- push 开发分支的修改到自己的 github 仓库
- 从开发分支向 fork 源的 master 分支发起推送 Pull Request
- fork 源项目的维护者合并功能到他的 master 分支
- 从 fork 源的 master 分支发起同步 Pull Request 到自己仓库项目的 master 分支
- 删除开发分支, Pull Request 工作流结束

![]({static}/images/github/newrequest.png)

点击 `New pull request` 按钮创建一个新请求.

![]({static}/images/github/comparing.png)

该请求是**双向**的:

- 当如上图所示, `base fork` 选择 fork 的源项目而 `head fork` 选择自己的项目时, 创建的请求是把自己项目的更新推送到 \-\> 源项目.
- 反过来, 如果 `base fork` 选择自己的项目而 `head fork` 选择 fork 的源项目时, 创建的请求是从源项目更新到 \-\> 自己的项目
- 如果无法选择 `base fork` 和 `head fork`, 可以点击 `compare across forks` 试试.

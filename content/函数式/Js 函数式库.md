Title: Js 函数式库
Author: HanXiao
Date: 2019-01-16 15:00

[TOC]

# Fantasy land

[Fantasy Land](https://github.com/fantasyland/fantasy-land) 是一套 [TypeClass](http://www.smallcpp.cn/han-shu-shi-guan-jian-gai-nian-Haskell-miao-shu.html#_7) 的 JS 描述, 包括但不限于 Functor, Applicative, Monad.

以下是几个常用的 TypeClass.

## Functor

Haskell 描述: [Functor](http://www.smallcpp.cn/han-shu-shi-guan-jian-gai-nian-Haskell-miao-shu.html#functor).

Js 描述差不多, 用 map 代替了 fmap.

`F.map(f)`

## Applicative

Haskell 描述: [Applicative](http://www.smallcpp.cn/han-shu-shi-guan-jian-gai-nian-Haskell-miao-shu.html#applicative-functor).

Js 中用 ap 代替了 <*>.

`A.ap(f)`

## Monad

Haskell 描述: [Monad](http://www.smallcpp.cn/han-shu-shi-guan-jian-gai-nian-Haskell-miao-shu.html#monda).

Js 中用 chain 代替了 >>=.

`M.chain(f)`

## Foldable

可折叠的类型, 对应 Haskell 中是实现了各种 fold 函数的 instance. 而 Js 中是实现了 reduce 的 instance.

`reduce :: Foldable f => f a ~> ((b, a) -> b, b) -> b`

这是 fantasy-land 的表示法, 与 Haskell 有些不同, 解释下:

```
reduce :: Foldable f => f a ~> ((b, a) -> b, b) -> b
'----'    '--------'    '-'    '--------------'   '-'
'           '            '       '                 ' - return type
'           '            '       '
'           '            '       ' - argument types
'           '            '
'           '            ' - method target type
'           '
'           ' - type constraints
'
' - method name
```

## Setoid

实现了 equals 相等性判断的 instance, 类似 Haskell 中的 Eq TypeClass.

`equals :: Setoid a => a ~> a -> Boolean`

## Semigroup

实现了 concat 的 instance, 连接两个 Semigroup.

`concat :: Semigroup a => a ~> a -> a`

注意, 与 Haskell 的 concat 不同, Haskell 中 concat 声明如下:

`concat :: [[a]] -> [a]`

```bash
ghci> concat ["foo", "bar", "car"]
"foobarcar"

ghci> concat [[3, 4, 5], [2, 3, 4], [2, 1, 1]]
[3, 4, 5, 2, 3, 4, 2, 1, 1]
```

## ChainRec

这个类型我找到的资料比较少.

`chainRec :: ChainRec m => ((a -> c, b -> c, a) -> m c, a) -> m b`

在声明上没有看到 ~>, 是在 [type representative](https://github.com/fantasyland/fantasy-land#type-representatives) 上进行调用.

该函数接收两个参数 `(f, i)`, f 是一个函数, 这个函数有三个参数:

- 参数 1, next 函数
- 参数 2, done 函数, 与 next 具有相同类型的返回值
- 参数 3, value, 累计值, 与 next 的参数类型相同

chainRec 调用时, 将 i 做第三个参数调用 f, f 的逻辑需要有分支判断, 用来处理是 next, 还是 done, 以下是 sanctuary-maybe 的例子:

```js
const Maybe = require("sanctuary-maybe")
const Just = Maybe.Just
const Nothing = Maybe.Nothing

Maybe['fantasy-land/chainRec'] (
    (next, done, x) =>
        x <= 1 ? Nothing : Just (x >= 1000 ? done (x) : next (x * x)),
        // sanctuary-maybe 内置函数 done, next 两个函数,
        // 不用管它, 把 done 和 next 的逻辑像上面那样写在函数体内就可以了.
    1
)
// Nothing
```

## Traversable

`traverse :: Applicative f, Traversable t => t a ~> (TypeRep f, a -> f b) -> f (t b)`

将返回值为 Applicative 类型的函数映射到一个 Traversable 上, 然后将结果由 Traversable of Applicative 转换为 Applicative of Traversable. 相当于先 chain 再 反转.

```js
const Maybe = require("sanctuary-maybe")
const Just = Maybe.Just
const Nothing = Maybe.Nothing
const safeDiv = n => d => d === 0 ? Nothing() : Just(n / d)

R.chain(safeDiv(10), [2, 4, 5])
// [ Just (5), Just (2.5), Just (2) ]

R.traverse(Just, safeDiv(10), [2, 4, 5])
// Just ([5, 2.5, 2])
```

# Fantasy land 的实现

有许多的库让 JS 支持函数式风格编程, 大体上它们分为两大类:

- 提供诸多高阶函数的工具库
  + Ramda
  + Lodash-FP
  + Underscore
- 提供了 Fantasy land 中 TypeClass 的实现
  + Folktale
  + Ramda-Fantasy (已废弃)
  + Fluture
  + Sanctuary

这里有一些推荐:

* Maybe: [sanctuary-js/sanctuary-maybe](https://github.com/sanctuary-js/sanctuary-maybe)
* Either: [sanctuary-js/sanctuary-either](https://github.com/sanctuary-js/sanctuary-either)
* Future: [fluture-js/Fluture](https://github.com/fluture-js/Fluture)
* State: [fantasyland/fantasy-states](https://github.com/fantasyland/fantasy-states)
* Tuple: [fantasyland/fantasy-tuples](https://github.com/fantasyland/fantasy-tuples)
* Reader: [fantasyland/fantasy-readers](https://github.com/fantasyland/fantasy-readers)
* IO: [fantasyland/fantasy-io](https://github.com/fantasyland/fantasy-io)
* Identity: [sanctuary-js/sanctuary-identity](https://github.com/sanctuary-js/sanctuary-identity)

|          | Functor | Applicative | Monad  | Foldable | Setoid | Semigroup | ChainRec | Traversable |
| -------- | :-----: | :---------: | :----: | :------: | :----: | :-------: | :------: | :---------: |
| Maybe    | **✔︎**  |   **✔︎**    | **✔︎** |  **✔︎**  | **✔︎** |  **✔︎**   |  **✔︎**  |   **✔︎**    |
| Either   | **✔︎**  |   **✔︎**    | **✔︎** |          | **✔︎** |           |  **✔︎**  |   **✔︎**    |
| Future   | **✔︎**  |   **✔︎**    | **✔︎** |          |        |           |  **✔︎**  |             |
| Identity | **✔︎**  |   **✔︎**    | **✔︎** |          | **✔︎** |           |  **✔︎**  |   **✔︎**    |
| Reader   | **✔︎**  |   **✔︎**    | **✔︎** |          |        |           |          |             |
| Tuple    | **✔︎**  |             |        |          | **✔︎** |  **✔︎**   |          |             |
| State    | **✔︎**  |   **✔︎**    | **✔︎** |          |        |           |  **✔︎**  |             |
| IO       | **✔︎**  |   **✔︎**    | **✔︎** |          |        |           |  **✔︎**  |             |

# Tutorials

[实例讲解 JS 函数式编程 (第一部分)](http://www.xiaojichao.com/post/functional-programming-in-js-with-practical-examples-part-1.html)

本部分讲解了 Fantasy Land 规范, 以及两个示例:

- 示例 1, 使用 **ramda-fantasy.Maybe** 处理空检查, 使用 **ramda.curry** 处理全局依赖, 使用 **ramda.path** 取出对象给定路径上的值.
- 示例 2, 使用 **ramda-fantasy.Either** 抛出错误信息.

[实例讲解 JS 函数式编程 (第二部分)](http://www.xiaojichao.com/post/functional-programming-in-js-with-practical-examples-part-2.html)

本部分讲解了两个示例:

- 示例 1, 使用 **Maybe Applicative** 处理多参函数中多个参数的空检查.
- 示例 2, 使用 **Validation Applicative** 抛出多个错误, 使用 **ramda.curryN** 让函数调用多次后才真正触发.

[函数式 TypeScript](https://linux.cn/article-7842-1.html)

本文讲解了以下几项技术:

- 使用函数代替简单值
- 数据转换过程管道化 (filter, map, reduce 的运用)
- 提取通用函数 (非公共模式, 而是与当前函数域无关的逻辑)

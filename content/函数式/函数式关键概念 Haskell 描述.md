Title: 函数式关键概念 Haskell 描述
Author: Martin
Date: 2018-12-03 18:00

学习 Haskell 过程中接触到的 FP (functional programming) 的一些概念, 并不是 FP 的全部 (PS: 为了容易理解, 尽可能的忽略了数学描述, 而改用开发容易理解的字眼, 所以某些概念可能会描述的并不准确).

[TOC]

# 模式匹配

# 柯里化

# 函数组合

# 柯里化, 函数组合 与 lambda 的关系

# 函数式

函数式编程中的函数式指的是**数学函数**, 即我们要编写具有数学函数性质的函数.

数学中的函数, 为两集合间的一种对应关系, 输入值集合中的每项元素 x, 对其施加某个法则 f, 皆能对应**唯一**一项输出值集合中的元素 y, 记作: `y = f(x)`.

而在编程中, 意味着我们要创建仅依赖输入就可以完成自身逻辑的函数, 并且对于同一个给定输入, 函数的执行结果总是相同的, 这一属性被称为**引用透明性**, 而这样的函数则被称为**纯函数**.

对于纯函数, 我们可以应用**代换模型** (数学中的函数推导), 这让代码具有可推导性, 遵循这一原则, 可以产出**可测试**, **可并发**以及**可缓存**的代码.

# 声明式 & 抽象

对于一个问题, 通常分解为两部分:

1. 要做什么?
2. 如何去做?

以 js 举例来说, 假设有一个数组, 我想要打印出它的每个元素.

对于这个问题, 很容易知道"要做什么"指的是: 打印数组元素, 即 `console.log()`, 现在我们告诉编译器如何去做:

```js
var array = [1, 2, 3]
for (i=0; i<array.length; i++) {
  console.log(array[i])
}
```

这就是命令式编程, 大部分的代码都在指明**如何去做**.

而函数式不同, 其重心是在声明**要做什么**, 至于如何去做则被**抽象**到一些高阶函数中:

```js
var array = [1, 2, 3]
array.forEach(e => console.log(e))
```

这就是函数式, 它主张**声明式**编程和编写**抽象**的代码. 这就要求选用的编程语言必须支持函数是一等公民.

把"如何去做"**抽象**为函数是函数式编程的核心思想, 这一过程其实就是**公共模式**的提取, 上例的 `forEach` 是 js 的内置函数, 当然我们也可以自己进行抽象, 参考 [计算机程序的构造与解释 - 高阶抽象和公共模式](http://www.smallcpp.cn/ji-suan-ji-cheng-xu-de-gou-zao-yu-jie-shi.html#_9).

# 代数数据类型

代数数据类型 (ADT, Algebraic data type), 代数数据类型是一种复合类型, 即通过组合其他类型形成的类型.

之所以叫**代数**, 是因为类型间的组合形式可以是**和**或者**积**, 例如:

- 和: `data Pair = I Int | D Double`,  此时 Pair 取值范围就是 Int 的范围 `+` Double 的范围, 例如 `I(10)`, `D(5.5)`
- 积: `data Pair = P Int Double`,  此时 Pair 取值范围就是 Int 的范围 `*` Double 的范围, 例如 `P(10, 5.5)`, `P(10, 5.6)`

> 上面的定义中, `I`, `D`, `P` 是**值构造子**(/器),  而 `Pair` 是**类型构造子**(/器).
> 类型构造子也是可以有参数的, 那被称为类型参数, 参见下节的*类型变量*.

用**ADT**以及**递归**两者结合实现一个保存 int 型数据的 binary trees:

```hs
data Tree = Empty | Leaf Int | Node Tree Tree
let tree = Leaf 10

:t tree
tree :: Tree
```

建立 ADT 只是开始, 我们要做的是对它们使用**模式匹配**.

# 类型变量

类型变量 (type variable), 是对类型的抽象, 它只是一个抽象, 并不具有实际分配的内存空间.

一个普通的变量, 例如 int, 它表示任意一个合法范围内的整数, 而一个类型变量, 则表示它可以取任何一种类型, 可以是 int, 可以是 string.

FP 中, 它被用来支持参数多态 (parametric polymorphism) 以方便用户可以编写与类型无关的通用功能. 例如 head 函数:

```hs
:t head
head :: [a] -> a  -- 可以看到 head 的实现与具体类型无关
```

类型变量还可以用在 **ADT** 中, 此时它可以被称作**类型参数**, 例如 Maybe 类型:

```hs
data Maybe a = Nothing | Just a
```

`Maybe` 是**类型构造子**(/器), 而 a 就是一个类型参数, 即传递给 Maybe 一个类型, 就能拿到一个新的类型回来, 例如给它 Char 就可以得到一个 `Maybe Char` 的新类型;

再例如, 用**类型变量**, **ADT**以及**递归**三者结合实现 List:

```hs
data List a = Empty | Cons a (List a)
```

是的, 没错, type variable 就是**泛型编程**的基础.

# 类型类

## what is

类型类 (type class), 是在参数多态 (parametric polymorphism) 中为类型变量定义约束, 可以联想面向对象中接口对类的行为约束, 接口定义一类必须实现了某些行为, 而类型类定义了必须为类型变量实现某些行为.

我们针对类型变量进行泛型编程, 但我们的"通用"逻辑只针对某些类型生效, 而不是全部, 例如 `(==)`, 这个函数只能接收可以比较大小的类型为参数, 看看它在 haskell 中的定义:

```hs
:t (==)
(==) :: Eq a => a -> a -> Bool
```

`Eq` 就是一个类型类, 它约束了类型变量 a 的一些行为, 现在来看看 `Eq` 定义的行为:

```hs
class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
```

它表示一个 Eq 类型必须实现了 `==` 和 `/=` 操作.

## Functor

```hs
class Functor f where
  fmap :: (a -> b) -> f a -> f b
```

很简单的定义, 只要一个类型实现 `fmap` 操作, 那它就是一个 Functor.

很多语言中, Functor 就是那些支持 **map** 操作的集合/容器, 如 List.

## Applicative Functor

Functor 定义了把一个普通函数应用在 Functor 上的操作, 但如果函数也被包裹在 Functor 内, 那就无法应用, Applicative Functor 就是解决这个问题的:

```hs
class Applicative f where
  pure :: a -> f a
  (<*>) :: f (a -> b) -> f a -> f b
```

Applicative 的使用场景我遇到的很少...这里就不过多介绍了.

## Monda

```hs
class Monda m where
  return :: a -> m a
  (>>=) :: m a -> (a -> m b) -> m b
  ... -- 其它不重要, 关键就是 >>=
```

在其它语言中, 这对应的就是 **flatMap** 操作, 这个 type class 应用的也蛮广泛, 因为在某些情况下, 函数会被设计成返回包裹的值用以封装异常/错误 (例如使用 Maybe), 如果此时对其使用 map 那返回的将是 `Maybe[Maybe]`, 换句话说, Functor 类型自动给结果包裹上 context, 而 Monda 则不会, 函数返回的是什么就是什么;

再次对比下两者的区别:

```hs
fmap :: (a -> b) -> f a -> f b
(>>=) :: m a -> (a -> m b) -> m b
```

可以看到 `fmap` 接收的函数其返回类型是 b, 但 fmap 自己却返回了 f b; 而 `>>=` 接收的函数其返回类型是 m b, 而其本身也就是返回了 m b.

对于 Monda 会有 `do` 语法糖来使代码更容易阅读:

```hs
Just 3 >>= (\x -> Just "!" >>= (\y -> Just (show x ++ y)))

do -- 与上面的代码等价
x <- Just 3
y <- Just "!"
Just (show x ++ y)
```

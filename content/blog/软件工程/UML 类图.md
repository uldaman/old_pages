author: HanXiao
date: 2015-02-15 14:17
title: UML 类图

![UML类图样例](http://img.blog.csdn.net/20150211193154259)

#### 类图和接口图

首先**动物**矩形框, 它就代表一个**类图**, 分三层:

- 第一层显示类的名称, 如果是**抽象类**, 则用斜体表示
- 第二层是类的属性
- 第三层是类的方法

注意前面的符号:

- ‘+’ –> public
- ‘-’ –> private
- ‘#’ –> protected

左下角的”飞翔”矩形框, 它是一个**接口图**, 它与类图的区别是顶端有**interface**显示, 然后它只有二层, 第二层是接口方法.

另外接口还有另一种表示法, 叫棒棒糖表示法, 看正下方的”唐老鸭”那个类, 它实现了一个”讲人话”的接口.

#### 类与类, 类与接口之间的关系

首先看 动物 –> 鸟 –> 鸭 –> 唐老鸭 这条线, 它们都是继承关系, 用**空心三角 +实线**来表示．

然后看 大雁 –> 飞翔, 大雁实现了飞翔接口, 用**空心三角 + 虚线**来表示.

再看 企鹅 –> 气候, 企鹅不继承气候, 也不实现气候, 但它需要知道气候的变化, 也就是说在企鹅这个类中需要引用到气候这个类, 这就是**“关联”**关系, 用**实线箭头**来表示.

```c++
class Penguin : public Bird {
public:
    Climate climage; // 企鹅类中引用到了气候对象
}
```

再看 雁群 –> 大雁, 大雁是群居动物, 每只大雁都属于一个雁群, 一个雁群可以有多只大雁, 就是**“聚合”**关系, 用**空心菱形 + 实线箭头**来表示.


> “聚合”是一种弱拥有关系, 体现的是A对象可以包含B对象, 但B对象又不是A对象的一部分

```c++
class WideGooseAggregate {
public:
    WideGoose[] arrayWideGoose; // 在雁群中有大雁数组对象
}
```

> 聚合是关联的一种，是强的关联关系, 在代码层面上，聚合和关联表现是一致的，只能从语义级别来区分；<br>
> 聚合关系是整体和个体的关系;<br>
> 普通关联关系的两个类处于同一层次上, 而聚合关系的两个类处于不同的层次，一个是整体，一个是部分.

现在看 鸟 –> 羽毛, 这是一种”合成”的强拥有关系, 体现了严格的部分和整体的关系, 部分和整体的生命同期一样, 它用**实心菱形 + 实线箭头**表示, 另外注意到合成关的连线下方有**数字**说明, 这被称为**基数**, 表明菱形这一端的类可以有几个箭头端的实例, 如果一个类可能有无数个实例, 则用’n’来表示.

> 关联 和 聚合 关系也可以有基数

```c++
class Bird {
public:
    Bird() {
        m_LeftWing = new Wing();
        m_RightWing = new Wing();
    }

protected:
    Wing m_LeftWing;
    Wing m_RightWing;
}
```

可以看到, 在 Bird 构造时同时构造翅膀.

最后看 动物 –> 氧气, 动物 –> 水, 动物中有新陈代谢方法, 而新陈代谢又需要用到氧气和水, 因此它们是一种依赖关系, 新陈代谢依赖于氧气和水**(换个角度说就是新陈代谢这个方法有两个参数 氧气和水).**

```c++
class Animal {
public:
    void Metabolism(Oxygen oxygen, Water water)
}
```

搞明白这些, 就能看懂大部分UML类图了.

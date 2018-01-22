Title: Python 高级特性之抽象类
Author: Martin
Date: 2016-03-31 13:32
Summary: Python 高级特性之抽象类

Python 中定义抽象类, 需要使用 __abc__ 模块, 该模块定义了一个元类(__ABCMeata__), 和装饰器 @__abstractmethod__、@__abstractproperty__ (目前貌似使用这两个中的任一个都可以...)

- 抽象类不能直接实例化
- 子类必须实现抽象类 __abstractmethod、abstractproperty__ 方法
- Python 中使用抽象功能会增大消耗, 所以大部分情况下都采用更宽松的作法, 即定义成正常的类, 通过编程规范来约束

```python
#!coding=utf-8
from abc import ABCMeta, abstractmethod, abstractproperty

class Foo:
  __metaclass__ = ABCMeta

  @abstractmethod
  def spam(self, a, b):
    pass

  @abstractproperty
  def name(self):
    pass

class Bar(Foo):
  def spam(self, a, b):
    print a, b

  def name():
    pass

b = Bar()
b.spam(1,2)
```

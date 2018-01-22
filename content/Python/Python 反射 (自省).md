Title: Python 反射 (自省)
Author: Martin
Date: 2017-09-15 19:20
Summary: 反射机制在 Python 中被称为自省 (不确定, 欢迎指证). 反射的主要功能就是通过字符串动态的导入包、实例化对象、调用方法以及访问属性.

[TOC]

首先说下, 反射在 Python 中被称为自省 (不确定, 欢迎指证). 反射的主要功能就是通过字符串动态的导入包、实例化对象、调用方法以及访问属性.

存在 `Person` 类:

```python
# person.py
class Person:
  def __init__(self):
    self.name = 'smallcpp'

  def getName(self):
    return self.name
```

# 动态导入模块
```python
module = __import__('person')
```

# 动态实例化对象
```python
module = __import__('person')
obj = getattr(module, 'Person')()
print obj.getName()
```

或者 (以下这种仅了解下, 通常使用上面的方式):

```python
from person import *
obj = globals()['Person']()
print obj.getName()
```

# 动态操作对象属性
Python 中与反射相关的方法有: `hasattr()`、`getattr()`、`setattr()`.

`hasattr(object, 'name')`<br>
判断实例对象里面是否有 name 属性或者 name 方法, 返回 BOOL 值, 有 name 返回 True, 否则返回 False.<br>
也可以判断 `module` 中是否有指定的类/函数/全局变量.

`getattr(object, 'name'[, default])`<br>
获取实例对象的属性或者方法, 如果存在返回出来, 如果不存在, 返回 None 或默认值 (如果指定了 default).<br>
也可以获取 `module` 中的类/函数/全局变量.

`setattr(object, 'name', values)`<br>
给实例对象的属性赋值, 若属性不存在, 先创建再赋值.

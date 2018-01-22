Title: Python 高级特性之 map( )
Author: Martin
Date: 2016-01-26 21:34
Summary: map() 函数接收两个参数, 一个是函数, 一个是序列, map() 将传入的函数依次作用到序列的每个元素.

map() 函数接收两个参数, 一个是函数, 一个是序列, map() 将传入的函数依次作用到序列的每个元素, 并把结果作为新的 list 返回.

例子, 求 1 到 10 每个数的乘阶:
```python
def fun(x):
	return x * x

map(fun, range(1, 11))
>>>[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

结合 lambda 会更简单:
```python
map(lambda x : x * x, range(1, 11))
>>>[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

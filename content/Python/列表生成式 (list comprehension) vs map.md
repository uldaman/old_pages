Title: 列表生成式 (list comprehension) vs map
Author: Martin
Date: 2018-08-08 11:35

Reference: [python-list-comprehension-vs-map](https://stackoverflow.com/questions/1247486/python-list-comprehension-vs-map)

总结一下:

- 如果已经有一个函数 `f`, 那么应该使用 `map`
- 如果还没有函数, 即需要在 `map` 中写 `lambda` 时, 那么应该使用 list comprehension

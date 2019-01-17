author: HanXiao
date: 2015-06-13 13:20
title: (二十二) Java 中的包装类

Java 为每个基本数据类型都提供了一个包装类, 这样我们就可以像操作对象那样来操作基本数据类型.

![](http://i59.tinypic.com/nmep83.jpg)

包装类主要提供了两大类方法:
*. 将本类型和其他基本类型进行转换的方法
*. 将字符串和本类型及包装类互相转换的方法

* * *

以 Integet 为例, 其它类似

Integer n1 = new Integer(5);
Integet n2 = new Integer(“5”);

![](http://i60.tinypic.com/14j4tpw.jpg)

* * *

JDK1.5 中引入了自动装箱和拆箱的机制

**装箱：**把基本类型转换成包装类，使其具有对象的性质，又可分为手动装箱和自动装箱;
![](http://i59.tinypic.com/20rttud.jpg)

**拆箱：**和装箱相反，把包装类对象转换成基本类型的值，又可分为手动拆箱和自动拆箱;
![](http://i61.tinypic.com/2vmtses.jpg)
???

Title: 07、UML 组件图
Author: HanXiao
Date: 2016-05-03 11:00
Summary: 描述代码构件的物理结构以及各种构建之间的依赖关系, 在组件图中, 构件时软件单个组成部分可以是一个文件、产品、可执行文件和脚本等.

描述代码构件的物理结构以及各种组件之间的依赖关系, 在组件图中, 组件可以是一个文件、产品、可执行文件或脚本等.

在 UML 2 中, 组件被认为是独立的, 在一个系统或子系统中的封装单位, 提供一个或多个接口.<br>
虽然 UML 2 规范没有严格地声明它, 但组件是呈现事物的更大的设计单元, 这些事物一般将使用可更换的组件来实现.<br>
主要思想是, 你能容易地在你的设计中重用或替换一个不同的组件实现, 因为一个组件封装了行为, 实现了特定接口.

在这里, 初学者很容易将组件图和类图搞混, 那么__组件图和类图__的区别如下:

- 类表示的是逻辑的抽象, 构件是存在于计算机中的物理抽象, 组件是可部署的, 而类不行
- 组件表示的是物理模块, 类是逻辑模块, 组件是由一组类协作而成的
- 类可以直接拥有操作和属性, 组件仅拥有可以通过其接口访问的操作

![](http://i68.tinypic.com/1zpidfd.jpg)

[参考文档](http://www.ibm.com/developerworks/cn/rational/rationaledge/content/feb05/bell/bell.html)

部署图和组件图:

- 部署图表现组件实例, 偏向于描述组件在节点中运行时的状态, 描述了组件运行的环境
- 组件图表现组件类型的定义, 偏向于描述构件之间相互依赖支持的基本关系

先有部署图还是组件图?
依照 top down 原则, 所以是从部署图到构件图, 实际上也应该如此, 因为我们在需求确定后, 一般就会确定大体的技术架构、程序模块划分, 而此时一般系统集成的工作也要相应的启动: 要买主机、网络设备;<br>所以要提供给系统集成人员相应的资料, 那么就需要先把部署图做出来, 然后再细化构件图.

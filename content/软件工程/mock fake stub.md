Title: mock fake stub
Author: Martin
Date: 2018-01-23 15:17

> 只有当**感知**和**分离**困难时，才需要使用这三个特殊 Object。Reference：《修改代码的艺术》。

##### Fake Object
仿对象，实现了依赖的接口，包含一些简单的数据处理逻辑，可对外部调用进行**感知**。

如果依赖的类很难构造，或无法进行感知时，可使用 Fake Object.

#### Mock Object
伪对象，Facke 的高级版，在内部进行了**断言**处理。

#### Stub Object
桩对象，仅实现了依赖接口，但无任务逻辑，只简单的“占坑”用。
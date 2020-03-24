
> [BuildContext](https://juejin.im/post/5c665cb651882562914ec153)
> [Key](https://juejin.im/post/5ca2152f6fb9a05e1a7a9a26)
> [RenderObject](https://book.flutterchina.club/chapter14/render_object.html)
> [闲鱼 Flutter](https://www.yuque.com/xytech/flutter)
> [Provider](https://juejin.im/post/5d00a84fe51d455a2f22023f)
> [Todos with flutter_bloc](https://medium.com/flutter-community/firestore-todos-with-flutter-bloc-7b2d5fadcc80)


InheritedWidet

Scoped Model <InheritedWidget> x

Redux 单向数据流 x

---------------------------------------

[Stream 流，响应式](https://juejin.im/post/5cc2acf86fb9a0321f042041#heading-4)

Bloc + [Rxdart](https://mcxiaoke.gitbooks.io/rxdocs/content/)

如果仅仅是单页面, 使用 Bloc 就行, 如果 Bloc 需要被共享, 则可配合下面的 Provider 一起使用.

---------------------------------------

Provider <InheritedWidget + ChangeNotifier>

目标是代替 StatefulWidget (但其实并不能完全代替, 共享非全局数据时, 为了避免重复生成, 需要用 statefulwidget 去缓存)

常用构造:

- Provider<T>.value
- ChangeNotifierProvider<T>.value
- StreamProvider<T>.value
- FutureProvider<T>.value
- ValueListenableProvider<T>.value
- MultiProvider -- 用来组合嵌套的 Provider

也有默认的构造 ??Provider<T>, 结合 Bloc 使用时, 可以用这种构造来释放资源.

child 获取数据:

- Provider.of<T>(context)
- Consumer?<T...>, 这是个工具类, 封装了 Provider.of 的方法, 同时还有局部刷新优化, **优先使用**.

怎么获取值，当多个类型相同时？并不行:

> if you use provider at the same time then when you access provider in child then you can receive the value of the closest provider only.

---------------------------------------

MVVM in flutter (what is viewmodel? is bloc?)

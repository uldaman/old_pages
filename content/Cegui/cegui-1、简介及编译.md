author: Martin
date: 2015-05-08 10:59
title: [CEGUI]. 1、简介及编译

CEGUI 是一个自由免费的 GUI 库, 基于LGPL协议, 使用C++实现, 完全面向对象设计.
CEGUI 开发者的目的是希望能够让游戏开发人员从繁琐的 GUI 实现细节中抽身出来, 以便有更多的开发时间可以放在游戏性上.
CEGUI 的渲染需要 3D 图形 API 的支持，如 OpenGL 或 Direct3D, 另外, 使用更高级的图形库也是可以的, 比如OGRE、Irrlicht和RenderWare等.

**编译:**
vs2013
Directx 9.0
cegui0.8.4
cegui-deps-0.8.x-src
cmake3.2.2

在安装 CEGUI 前, 先要安装 vs2013 和 Directx 9.0 SDK. 然后在 CEGUI 官网下载 CEGUI 源码包(cegui-0.8.4) 以及 CEGUI 依赖库(cegui-deps-0.8.x-src). 接着再去下载 cmake.
这里我已经都打包好了: [http://yunpan.cn/cwdGnStFtvGum ](http://yunpan.cn/cwdGnStFtvGum) 访问密码 d682

下载好后, 解压 cegui0.8.4 和 cegui-deps-0.8.x-src 到安装目录, 我选的是 E 盘.
接下来安装 cmake, 运行 camke, 拖动刚解压的 cegui-deps-0.8.x-src 文件夹下的 CMakeLists.txt 到 cmake 上.
![](http://i59.tinypic.com/2lxgoiw.jpg)

点击 cmake 界面下的 Configure 按钮, 然后选择当前编译器版本 vs2013, 最后点击 Finish 按钮, 此时会开始加载 CMakeLists.txt 文件, 等它加载完毕.
![](http://i62.tinypic.com/1127k8k.jpg)

![](http://i59.tinypic.com/2ntciuw.jpg)

再次点击 cmake 界面下的 Configure 按钮, 等界面变白后, 再点击 Generate 按钮.
![](http://i57.tinypic.com/n5pmya.jpg)

此时, 会在工程建立路径下生成 CEGUI-DEPS.sln, 打开后右键解决方案 –> 批生成 –> ALL_BUILD Debug|Win32  + ALL_BUILD Release|Win32 对依赖库进行编译.
![](http://i59.tinypic.com/a08fb4.jpg)

![](http://i57.tinypic.com/16kyqyu.jpg)

编译完成之后在 cegui-deps-0.8.x-src 文件夹下会出现 dependencies 文件夹, 将该文件夹移动到之前解压的 cegui-0.8.4 文件夹中, 然后这个 cegui-deps-0.8.x-src 文件夹就可以删掉了, 没啥用的样子.

接下来采用相同步骤对 cegui-0.8.4 进行编译, 此时需要手动设置 CEGUI的XML 解析器，即将 CEGUI_BUILD_XMLPARSER_EXPAT 设为 checked, 其他属性设置默认即可满足要求, 如下图:
![](http://i61.tinypic.com/8xikc3.jpg)

Congigure 完成之后 Generate, 生成 cegui.sln 文件, 打开 cegui.sln.
右键 ALL_BUILD, 选择[属性], 选择[VC++目录], 设置[包含目录][库目录]为 dependencies 文件夹下的 include 和 lib 文件夹.
然后右键解决方案 –> 批生成 –> ALL_BUILD Debug|Win32  + ALL_BUILD Release|Win32 进行编译.
![](http://i61.tinypic.com/ifobiq.jpg)

初次编译会报错.

![](http://i59.tinypic.com/2nsvqr9.jpg)

点击错误

定位到 Sample_FontDemo.cpp 文件
第133行：
将(encoded_char*)"+ - ? B I W Y f n t ℹ ⇦ ⇧ ⇨ ⇩ ⌘ ☎ ☐ ☑ ⚖ ⚙ ⚠ ⛏ ✎ ✑ ✓ ✔ ✕ ✖ ❝ ❞ ➡ ⬀ ⬁ ⬂ ⬃ ⬅ ⬆ ⬇ ⬈ ⬉ ⬊ ⬋                    "
修改为(encoded_char*)"+111111111111111111111111"
第147行：
将每个 "⬀ " 修改为"1"

定位到GameMenu.cpp文件
第691行：
将finalText += reinterpret_cast("❚")
修改为finalText += reinterpret_cast("d")
第717行：
将finalText += reinterpret_cast("❚")
修改为finalText += reinterpret_cast("d")
第749行：
将finalText += reinterpret_cast("❚")
修改为finalText += reinterpret_cast("d")

重新进行编译, 完成之后在 cegui-0.8.4 文件夹的 bin 文件夹下找到 CEGUISampleFramework-0.8.exe, 双击打开.
这时, 它会报个错:
![](http://i61.tinypic.com/e9b66f.jpg)

我们将 dependencies 文件夹的 bin 文件夹里的文件全部复制一份到 cegui-0.8.4 文件夹的 bin 文件夹下, 再重新打开 CEGUISampleFramework-0.8.exe.
![](http://i61.tinypic.com/hsne38.jpg)

![](http://i61.tinypic.com/2gy2dqc.jpg)
?

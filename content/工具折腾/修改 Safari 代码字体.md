Title: 修改 Safari 代码字体
Author: Martin
Date: 2019-01-17 12:56

工具: [油猴插件](https://tampermonkey.net/?browser=safari)

添加以下脚本:

```js
// ==UserScript==
// @name         使用等宽字体
// @namespace    https://github.com/uldaman/
// @version      1.0.0
// @description  强制修改网页中代码部分为等宽字体!
// @author       HanXiao
// @include      *
// @exclude      *.seedr.cc*
// @exclude      *console.cloud.google.com/cloudshell*
// @run-at       document-start
// @grant        unsafeWindow
// ==/UserScript==

(function () {
    'use strict';
    let element = document.createElement("link");
    element.rel = "stylesheet";
    element.type = "text/css";
    element.href = 'data:text/css, pre, code {font-family: Menlo !important;}';
    document.documentElement.appendChild(element);
    setTimeout(function () {
        let modStyle = document.querySelector('#modCSS_font');
        if (modStyle === null) {
            modStyle = document.createElement('style');
            modStyle.id = 'modCSS_font';
            document.body.appendChild(modStyle);
        }
        modStyle.innerHTML = 'pre, code {font-family: Menlo !important;}';
    }, 300);
})();

```

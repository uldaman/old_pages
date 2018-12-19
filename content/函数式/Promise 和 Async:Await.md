Title: Promise 和 Async/Await
Author: Martin
Date: 2018-12-16 19:00

> 转自 [Promise 处理回调以及 Async/Await 替代 Promise 的六大理由](https://blog.csdn.net/haley_guo/article/details/80069872)

[TOC]

# Promise 处理回调嵌套

## 什么是 Promise

Promise 通常用于处理函数的异步调用, 通过链式调用的方式, 使得代码更加直观, 举例来说:

```js
var myPromise = function(tag) {
return new Promise(function(resolve, reject){
    if(tag){
        resolve('success');
    }else{
        reject('filed');
    }})
}


myPromise(true).then(function(message) {
  console.log(message) // "success"
})
```

我们可以看到设置 Promise 只要 `new Promise()` 就可以, 并且接受一个函数, 该函数里面会执行 resolve 方法, 表示异步调用成功时执行, reject 表示异步调用失败时候调用.

在链式调用时候, then 后面接的第一个函数为成功之时调用的函数 \-\- resolve, 并且这里的默认参数等同于 Promise 中 resolve 中的初始参数.

## then 和 catch

**then**: 可以在 Promise 中实现链式调用, 在上文中已经介绍. 补充, then 里面的第二个函数, 为异步调用失败之时执行, 接上面的例子:

```js
myPromise(false).then(null, function(err) {
  console.log(err) // "filed"
})
```

**catch**: catch 方法, 相当于 `then(null, function(err) { console.log(err) }` 失败方法调用的一个缩写.

```js
myPromise(false).catch(function(err) { console.log(err) })  // "filed"
```

## Promise.all

Promise.all 可以接收一个元素为 Promise 对象的数组作为参数, 当这个数组里面所有的 Promise 对象都变为 resolve 时, 该方法才会返回.

```js
var p1 = new Promise(function (resolve) {
    setTimeout(function () {
        resolve("Hello");
    }, 3000);
});

var p2 = new Promise(function (resolve) {
    setTimeout(function () {
        resolve("World");
    }, 1000);
});

Promise.all([p1, p2]).then(function (result) {
    console.log(result); // ["Hello", "World"]
});
```

## Promise.race

Promise.all 可以接收一个元素为 Promise 对象的数组作为参数, 当这个数组里面最快的 Promise 对象变为 resolve 时, 该方法就会返回.

```js
var p1 = new Promise(function (resolve) {
    setTimeout(function () {
        resolve("Hello");
    }, 3000);
});

var p2 = new Promise(function (resolve) {
    setTimeout(function () {
        resolve("World");
    }, 1000);
});

Promise.race([p1, p2]).then(function (result) {
    console.log(result); // "World"
});
```

# 为什么 Async/Await 比 Promise 更好

## 简洁

使用 Promise 是这样的:
getJSON 函数返回一个 Promise, 这个 Promise 成功 resolve 时会返回一个 json 对象. 我们只是调用这个函数, 打印返回的JSON对象, 然后返回 "done".

```js
const makeRequest = () =>
  getJSON()
    .then(data => {
      console.log(data)
      return "done"
    })

makeRequest()
```

使用 Async/Await 是这样的:

```js
const makeRequest = async () => {
  console.log(await getJSON())
  return "done"
}

makeRequest()
```

函数前面多了一个 aync 关键字. await 关键字只能用在 aync 定义的函数内. async 函数会隐式地返回一个 Promise, 该 Promise 的 reosolve 值就是函数 return 的值. (示例中 reosolve 值就是字符串 "done"). `await getJSON()` 表示 console.log 会等到 getJSON 的 Promise 成功 reosolve 之后再执行.

## 错误处理

Async/Await 让 try/catch 可以同时处理同步和异步错误.

在下面的 Promise 示例中, try/catch 不能处理 JSON.parse 的错误, 因为它在 Promise 中. 我们需要使用 catch, 这样错误处理代码非常冗余. 并且, 在我们的实际生产代码会更加复杂.

```js
const makeRequest = () => {
  try {
    getJSON()
      .then(result => {
        // JSON.parse 可能会出错
        const data = JSON.parse(result)
        console.log(data)
      })
      .catch((err) => {
        // 处理异步代码的错误
        console.log(err)
      })
  } catch (err) {
    console.log(err)
  }
}
```

使用 aync/await 的话, catch 能处理 JSON.parse 错误:

```js
const makeRequest = async () => {
  try {
    // this parse may fail
    const data = JSON.parse(await getJSON())
    console.log(data)
  } catch (err) {
    console.log(err)
  }
}
```

## 回调嵌套

下面实例中, 通过判断返回数据来决定是直接返回, 还是继续获取更多的数据.

```js
const makeRequest = () => {
  return getJSON()
    .then(data => {
      if (data.needsAnotherRequest) {
        return makeAnotherRequest(data)
          .then(moreData => {
            console.log(moreData)
            return moreData
          })
      } else {
        console.log(data)
        return data
      }
    })
}
```

这些代码看着就头痛. 嵌套（6层）, 括号, return 语句很容易让人感到迷茫, 而它们只是需要将最终结果传递到最外层的Promise.

上面的代码使用 async/await 编写可以大大地提高可读性:

```js
const makeRequest = async () => {
  const data = await getJSON()
  if (data.needsAnotherRequest) {
    const moreData = await makeAnotherRequest(data);
    console.log(moreData)
    return moreData
  } else {
    console.log(data)
    return data
  }
}
```

## 模拟串行

你很可能遇到过这样的场景, 调用 Promise1, 使用 Promise1 返回的结果去调用 Promise2, 然后使用两者的结果去调用 Promise3. 你的代码很可能是这样的:

```js
const makeRequest = () => {
  return Promise1()
    .then(value1 => {
      return Promise2(value1)
        .then(value2 => {
          return Promise3(value1, value2)
        })
    })
}
```

使用 async/await 的话, 代码会变得异常简单和直观.

```js
const makeRequest = async () => {
  const value1 = await Promise1()
  const value2 = await Promise2(value1)
  return Promise3(value1, value2)
}
```

## 错误栈

下面示例中调用了多个 Promise, 假设 Promise 链中某个地方抛出了一个错误:

```js
const makeRequest = () => {
  return callAPromise()
    .then(() => callAPromise())
    .then(() => callAPromise())
    .then(() => callAPromise())
    .then(() => callAPromise())
    .then(() => {
      throw new Error("oops");
    })
}

makeRequest().catch(err => {
    console.log(err);
    // output
    // Error: oops at callAPromise.then.then.then.then.then (index.js:8:13)
})
```

Promise 链中返回的错误栈没有给出错误发生位置的线索. 更糟糕的是, 它会误导我们; 错误栈中唯一的函数名为 callAPromise, 然而它和错误没有关系. (文件名和行号还是有用的).

然而, async/await 中的错误栈会指向错误所在的函数:

```js
const makeRequest = async () => {
  await callAPromise()
  await callAPromise()
  await callAPromise()
  await callAPromise()
  await callAPromise()
  throw new Error("oops");
}

makeRequest().catch(err => {
    console.log(err);
    // output
    // Error: oops at makeRequest (index.js:7:9)
})
```

在开发环境中, 这一点优势并不大. 但是, 当你分析生产环境的错误日志时, 它将非常有用. 这时, 知道错误发生在 makeRequest 比知道错误发生在 then 链中要好.

## 调试

async/await 能够使得代码调试更简单. Promise 不能在返回表达式的箭头函数中设置断点, 如果在 then 代码块中设置断点, 使用 Step Over 快捷键, 调试器不会跳到下一个 then, 因为它只会跳过异步代码.

使用 await/async 时, 你不再需要那么多箭头函数, 这样你就可以像调试同步代码一样跳过 await 语句.

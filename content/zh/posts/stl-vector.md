---
title: 'C++ STL 之 不定长数组 vector'
date: 2018-02-20T16:19:04
categories: [编程语言]
tags: [CPP, STL]
original: true
csdn: 79339728
---

> 本文转载自我在 CSDN 的旧博客：[C++ STL 之 不定长数组 vector](https://blog.csdn.net/zkx981105/article/details/79339728)（写于 2018-02-20），迁移时整理了格式。

STL : Standard Template Library, C++ 标准模板库, 封装好了各种接口供我们调用。vector 是模板类，是容器的一种，是不定长的数组，可以在尾部增加删除元素，获取数组大小等。容器还有 set, map, list, stack, queue 等... 我们在算法竞赛中必定会用到。

<!--more-->

本文实例代码在 [https://github.com/zzxzzk115/STL_vector](https://github.com/zzxzzk115/STL_vector)

我们先来看看 vector 的使用方法：

先引入头文件

```cpp
#include <vector>
```

当然别忘了

```cpp
#include <iostream>
using namespace std;
```

再就是 vector 对象的创建, vector 模板类有很多构造函数，所以在创建对象时也有多种创建方法（在 main 中创建）：

```cpp
vector<int> v1;         //创建空vector
vector<int> v2(v1);     //从v1拷贝至新vector
vector<int> v3(5);      //创建含5个元素的vector
vector<int> v4(5,0);    //创建含5个0的vector
```

为了方便观察我们的 vector 对象中都有哪些元素，我们可以用迭代器来遍历 vector 对象，然后打印。为此我们先看 begin() 和 end() 的使用：（可以把迭代器理解为指针, begin() 指向 vector 对象的头部，end() 指向 vector 对象的尾部）

```cpp
void PrintVector(vector<int> ve)
{
    cout << "Vector中的数据为：";
    vector<int>::iterator veIterator;
    for (veIterator = ve.begin(); veIterator < ve.end(); veIterator++)
    {
        cout << *veIterator << " ";
    }
    cout << endl;
}
```

接下来可以愉快的玩耍了，pop_back() push_back() 顾名思义，向尾部增加、向尾部删除嘛, so easy.

在 main 函数中测试一下：

```cpp
v1.push_back(5);
v1.push_back(4);
v1.push_back(8);
PrintVector(v1);
```

结果是

![](/img/csdn/79339728-1.png)

如何访问某一位置的元素呢？用 [index] 或 at(index) 来访问，（index 是索引值, 从 0 开始）

```cpp
cout << v1[0] << endl;
cout << v1.at(1) << endl;
cout << v1[2] << endl;
```

结果是

![](/img/csdn/79339728-2.png)

我们还可以访问头尾的数据: back() front()

```cpp
cout << v1.back() << endl;
cout << v1.front() << endl;
```

结果是

![](/img/csdn/79339728-3.png)

max_size() 获取最大容纳量，size() 获取当前 vector 对象元素个数

```cpp
cout << "v1中的最大容量为：" << v1.max_size() << endl;
cout << "v1中的元素个数为：" << v1.size() << endl;
```

结果是

![](/img/csdn/79339728-4.png)

empty() 返回 1 即为空，返回 0 即不为空

```cpp
cout << "v1是否为空？" << v1.empty() << endl;
```

结果是

![](/img/csdn/79339728-5.png)

sort() 可对 vector 升序， reverse() 可对 vector 降序

```cpp
sort(v1.begin(), v1.end());
PrintVector(v1);
reverse(v1.begin(), v1.end());
PrintVector(v1);
```

结果是

![](/img/csdn/79339728-6.png)

swap() 可交换 vector 数据

```cpp
swap(v1, v4);
PrintVector(v1);
PrintVector(v4);
```

结果为

![](/img/csdn/79339728-7.png)

erase() 删除元素，insert() 插入元素，不过一定要用迭代器

先看 erase, insert 同理把 erase 换成 insert 是一样的

```cpp
PrintVector(v4);
vector<int>::iterator vErase = v4.begin();
vErase = vErase + 1;
v4.erase(vErase);
PrintVector(v4);
```

结果是

![](/img/csdn/79339728-8.png)

clear() 清空 vector 元素

```cpp
PrintVector(v4);
v4.clear();
cout << "v4是否为空？ " << v4.empty() << endl;
```

结果是

![](/img/csdn/79339728-9.png)

以下是文档:

[http://en.cppreference.com/w/cpp/container/vector](http://en.cppreference.com/w/cpp/container/vector)

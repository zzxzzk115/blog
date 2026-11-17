---
title: '算法——归并排序'
date: 2018-03-24T14:34:41
categories: [算法与数据结构]
tags: [排序]
original: true
csdn: 79677641
---

> 本文转载自我在 CSDN 的旧博客：[算法——归并排序](https://blog.csdn.net/zkx981105/article/details/79677641)（写于 2018-03-24），迁移时整理了格式。

“分而治之”

在了解了分治法与递归以后，就可以理解一种新的排序算法了。

它叫做 ：“**归并排序**”。

<!--more-->

对数组排序可以通过分治法来解决。我们把数组拆分成很多部分，直到数组元素为 1，然后使每一部分有序后再合并成新的有序数组，最后可以得到排序的结果。

下面通过代码简单看看归并排序

```cpp
#include <cstdio>
#include <iostream>
using namespace std;

/*
    函数 : 归并
    参数 : 待排序数组a, 待排序数组部分的起始下标s、中间下标m、末尾下标e, 临时数组tmp
    作用 : 将有序数组归并成新的有序数组
*/
void Merge(int a[], int s, int m, int e, int tmp[])
{
    //初始化游标
    int pb = 0;                     //指向tmp的游标pb初始化为0(最左边)
    int p1 = s, p2 = m+1;           //指向a左半部分的游标初始化为s(最左边)
                                    //指向a右半部分的游标初始化为m+1(最左边)

    //当游标都在各自数组范围内时, 也就是数组还没被归并完时
    while(p1 <= m && p2 <= e)
    {
        //把a左右部分中小的元素拷贝至tmp
        if(a[p1] < a[p2])
            tmp[pb++] = a[p1++];
        else
            tmp[pb++] = a[p2++];
    }

    //把剩余未归并的元素加入到tmp
    while(p1 <= m)
        tmp[pb++] = a[p1++];
    while(p2 <= e)
        tmp[pb++] = a[p2++];

    //此时tmp为归并后的结果, 将其赋值给a
    for(int i = 0; i < pb; i++)
        a[s+i] = tmp[i];
}


/*
    函数 : 归并排序
    参数 : 待排序数组a, 待排序数组部分的起始下标s、末尾下标e, 临时数组tmp
    作用 : 对a进行排序（分治思想）
*/
void MergeSort(int a[], int s, int e, int tmp[])
{
    if(s < e)
    {
        int m = s + (e-s)/2;        //m是中间下标
        MergeSort(a, s, m, tmp);    //排左边
        MergeSort(a, m+1, e, tmp);  //排右边
        Merge(a, s, m, e, tmp);     //归并
    }
}

int main()
{
    int a[10] = {1,4,7,2,4,78,42,23,76,34};
    int b[10];

    int size = sizeof(a)/sizeof(int);
    //cout << size << endl;

    MergeSort(a, 0, size -1, b);
    for(int i = 0; i < size; i++)
        cout << a[i] << " ";
    return 0;
}
```

结果是

```text
1 2 4 4 7 23 34 42 76 78
```

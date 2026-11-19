---
title: '算法——快速排序'
date: 2018-02-19T12:29:10
categories: [算法与数据结构]
tags: [排序]
original: true
csdn: 79336832
---

> 本文转载自我在 CSDN 的旧博客：[算法——快速排序](https://blog.csdn.net/zkx981105/article/details/79336832)（写于 2018-02-19），迁移时整理了格式。

在懂得递归过程、理解分治法原理后，理解快速排序是很简单的事情。

快速排序顾名思义：快、高效。不多 bb，上思路和代码。

<!--more-->

算法的基本思想是：

（1）先从数列中取出一个数作为基准数（常常选第一个数）；

（2）分区过程，小于或等于的数全放到它的左边,比这个数大的数放到它的右边;

（3）再对左右区间重复第二步，直到每个区间只有一个数为止，即左边界下标等于右边界下标；

简化描述为：

1.i= L, j=R,基准数即为 a[i]，保存起来;

2.j--,由后向前找比它小的数，找到后将此数放到 a[i] 中；

3.i++,由前向后找比它大的数，找到后将此数填入到 a[j] 中；

4.递归执行 2，3 两步，直到 i==j，最后将基准数填入 a[i] 中；

```cpp
#include <stdio.h>

void QuickSort(int *arr, int start, int end);
int Partition(int *arr, int start, int end);

int main()
{
    int array[7] = {3,6,0,9,4,2,100};

    QuickSort(array, 0, 6);

    for (int i = 0; i < 7; i++)
    {
        printf("%d ",array[i]);
    }//会输出0 2 3 4 6 9 100
}

void QuickSort(int *arr, int start, int end)
{
    if (start == end)
    {
        return;
    }

    int index = Partition(arr, start, end);

    if (index > start)
    {
        QuickSort(arr, start, index - 1);
    }

    if (index < end)
    {
        QuickSort(arr, index + 1, end);
    }
}

// 划分算法
int Partition(int *arr, int start, int end)
{
    //此时的x就是基准值；
    int i = start, j = end, x = arr[start];

    //下面的while循环表示一次分治，也就是进行一次排序；
    while (i < j)
    {
        //先从基准值右侧找出小于基准的值；
        while (i < j && arr[j] >= x)
        {
            j--;
        }
        if (i < j)
        {
            //交换顺序，i++；
            arr[i++] = arr[j];
        }
        //从基准值左侧找出大于基准的值；
        while (i < j && arr[i] < x)
        {
            i++;
        }
        if (i < j)
        {
            //交换顺序，j--;
            arr[j--] = arr[i];
        }
    }
    //把基准值放入arr[i]位置；
    arr[i] = x;

    return i;
}
```

![](/img/csdn/79336832-1.webp)

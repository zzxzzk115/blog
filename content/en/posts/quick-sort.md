---
title: 'Algorithms: Quick Sort'
date: 2018-02-19T12:29:10
categories: [Algorithms-Data-Structures]
tags: [Sorting]
original: true
csdn: 79336832
aiTranslated: true
---

> Reposted from my old CSDN blog: [算法——快速排序](https://blog.csdn.net/zkx981105/article/details/79336832) (written 2018-02-19); formatting tidied during migration.

Once you get how recursion works and understand the principle of divide and conquer, quick sort is easy to understand.

Quick sort is just what the name says: quick and efficient. No more talk, here's the idea and the code.

<!--more-->

The basic idea of the algorithm is:

(1) First pick a number from the sequence as the pivot (usually the first one);

(2) Partition: put every number less than or equal to it on its left, and every number greater than it on its right;

(3) Repeat step two on the left and right intervals until each interval has only one number, i.e. the left boundary index equals the right boundary index;

In short:

1. i = L, j = R, the pivot is a[i]; save it;

2. j--, search from back to front for a number smaller than it, and when found, put that number into a[i];

3. i++, search from front to back for a number larger than it, and when found, put that number into a[j];

4. Repeat steps 2 and 3 until i == j, then finally put the pivot into a[i];

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
    }// prints 0 2 3 4 6 9 100
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

// partition algorithm
int Partition(int *arr, int start, int end)
{
    // x here is the pivot;
    int i = start, j = end, x = arr[start];

    // the while loop below is one round of divide and conquer, i.e. one pass of sorting;
    while (i < j)
    {
        // first find a value smaller than the pivot from the right side;
        while (i < j && arr[j] >= x)
        {
            j--;
        }
        if (i < j)
        {
            // swap, i++;
            arr[i++] = arr[j];
        }
        // find a value larger than the pivot from the left side;
        while (i < j && arr[i] < x)
        {
            i++;
        }
        if (i < j)
        {
            // swap, j--;
            arr[j--] = arr[i];
        }
    }
    // put the pivot at arr[i];
    arr[i] = x;

    return i;
}
```

![](/img/csdn/79336832-1.png)

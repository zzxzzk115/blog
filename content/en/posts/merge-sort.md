---
title: 'Algorithms: Merge Sort'
date: 2018-03-24T14:34:41
categories: [Algorithms-Data-Structures]
tags: [Sorting]
original: true
csdn: 79677641
aiTranslated: true
---

> Reposted from my old CSDN blog: [算法——归并排序](https://blog.csdn.net/zkx981105/article/details/79677641) (written 2018-03-24); formatting tidied during migration.

"Divide and conquer"

Once you understand divide and conquer and recursion, you're ready to understand a new sorting algorithm.

It's called "**merge sort**".

<!--more-->

Sorting an array can be solved with divide and conquer. We split the array into smaller and smaller parts until each part has just 1 element, then make each part sorted and merge them into new sorted arrays, and in the end we get the sorted result.

Let's take a quick look at merge sort through some code.

```cpp
#include <cstdio>
#include <iostream>
using namespace std;

/*
    Function : merge
    Params   : array to sort a; start index s, middle index m, and end index e of the part being sorted; temp array tmp
    Purpose  : merge sorted arrays into a new sorted array
*/
void Merge(int a[], int s, int m, int e, int tmp[])
{
    // initialize the cursors
    int pb = 0;                     // cursor pb into tmp starts at 0 (leftmost)
    int p1 = s, p2 = m+1;           // cursor into the left half of a starts at s (leftmost)
                                    // cursor into the right half of a starts at m+1 (leftmost)

    // while both cursors are within their ranges, i.e. the arrays haven't been fully merged yet
    while(p1 <= m && p2 <= e)
    {
        // copy the smaller element of a's left/right parts into tmp
        if(a[p1] < a[p2])
            tmp[pb++] = a[p1++];
        else
            tmp[pb++] = a[p2++];
    }

    // append the remaining unmerged elements to tmp
    while(p1 <= m)
        tmp[pb++] = a[p1++];
    while(p2 <= e)
        tmp[pb++] = a[p2++];

    // tmp now holds the merged result; copy it back into a
    for(int i = 0; i < pb; i++)
        a[s+i] = tmp[i];
}


/*
    Function : merge sort
    Params   : array to sort a; start index s and end index e of the part being sorted; temp array tmp
    Purpose  : sort a (divide and conquer)
*/
void MergeSort(int a[], int s, int e, int tmp[])
{
    if(s < e)
    {
        int m = s + (e-s)/2;        // m is the middle index
        MergeSort(a, s, m, tmp);    // sort the left half
        MergeSort(a, m+1, e, tmp);  // sort the right half
        Merge(a, s, m, e, tmp);     // merge
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

The result is

```text
1 2 4 4 7 23 34 42 76 78
```

---
title: 'Algorithms: Bubble Sort'
date: 2018-02-19T12:14:07
categories: [Algorithms]
tags: [Algorithms, Sorting]
original: true
csdn: 79336722
aiTranslated: true
---

> Reposted from my old CSDN blog: [算法——冒泡排序](https://blog.csdn.net/zkx981105/article/details/79336722) (written 2018-02-19); formatting tidied during migration.

When we learn sorting algorithms, bubble sort is definitely one of the first. It's the simplest and easiest to understand, so when complexity isn't a concern it's a pretty commonly used sorting algorithm (I use it all the time; after all, it's just two nested for loops and a swap, really easy to remember). Next, let's look at how the algorithm works.

<!--more-->

Before anything else, let's talk about why it's called bubble sort.

Let's look at a cute illustration from *Aha! Algorithms* (《啊哈！算法》) to make it easier to understand.

![](/img/csdn/79336722-1.png)

Imagine the numbers in the array are in random order, and each number is like a bubble in water. We compare the sizes of two adjacent bubbles (numbers). Say the array is {12,35,99,18,76}; at the start we compare 12 and 35, find that 35 is bigger than 12, so 12 floats up (12 and 35 swap places). As shown in the picture, after one pass, 12 has floated to the surface (it's now at the very front), and from there we just repeat the operation in a loop. Since the ones already sorted don't need sorting again, each later pass does one fewer comparison. Actually, whether it floats to the surface or sinks to the bottom, it's the same idea.

To put it more formally:

(1) Compare two adjacent elements; if the front one is larger than the back one, swap them;

(2) After one pass over the array from element 0 to element N-1 this way, the largest element ends up in the last position, i.e. at index N-1 (it has sunk to the bottom).

(3) N = N-1; if N is not 0, repeat steps (1) and (2), i.e. traverse the array again from element 0 to element N-2; otherwise the sort is done;

The code is as follows:

```cpp
#include <stdio.h>

void Swap(int*, int*);
void BubbleSort(int*, int);

// swap the values of two numbers
void Swap(int *a, int *b){
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

// bubble sort
void BubbleSort(int arr[], int len){
    for(int i = 0; i < len; i++){
        for(int j = 1; j < len - i; j++){
            if(arr[j-1] > arr[j]){
                Swap(&arr[j-1], &arr[j]);
            }
        }
    }
}

int main(){
    int array[5] = {12,35,99,18,76};
    BubbleSort(array,5);
    for(int i = 0; i < 5; i++){
        printf("%d ",array[i]);
    }// prints 12 18 35 76 99
    return 0;
}
```

If you know bubble sort by heart, then in lots of cases where complexity doesn't matter you can write sorting code really quickly (of course, just including the algorithm library and calling sort() is even faster...)

Borrowing a chart here so you can compare:

![](/img/csdn/79336722-2.png)

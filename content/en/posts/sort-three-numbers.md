---
title: 'Common Ways to Sort Three Numbers'
date: 2017-11-14T10:32:58
categories: [Algorithms-Data-Structures]
tags: [Sorting, C]
toc: true
original: true
csdn: 78527343
aiTranslated: true
---

> Reposted from my old CSDN blog: [三个数的排序常用方法](https://blog.csdn.net/zkx981105/article/details/78527343) (written 2017-11-14); formatting tidied during migration.

Problem: say we have three numbers a, b, c; we want to sort them from smallest to largest. What's the simplest way to do it?

<!--more-->

----

### Idea:

Put the smallest number on the left and the largest on the right. The sorting can be done with three ifs.

----

### Implementation:

The three-if approach:

```c
//_3if.c
int main(){
	int a,b,c,temp;
	// read in three numbers
	scanf("%d %d %d",&a,&b,&c);
	// three ifs; a table walking through the process follows below
	if(a>b) temp=a,a=b,b=temp;
	if(b>c) temp=b,b=c,c=temp;
	if(a>b) temp=a,a=b,b=temp;
	// print the three sorted numbers
 	printf("%d %d %d",a,b,c);
	return 0;
}
```

----

## Step-by-step table:

| \ | a | b | c |
|--|--|--|--|
|Set 1 initial values|3|1|2|
|1st if|1|3|2|
|2nd if|1|2|3|
|3rd if|1|2|3|
|Set 2 initial values|7|6|5|
|1st if|6|7|5|
|2nd if|6|5|7|
|3rd if|5|6|7|
|Set 3 initial values|1|2|3|
|1st if|1|2|3|
|2nd if|1|2|3|
|3rd if|1|2|3|

----

## Summary:

As you can see, three passes of if can quickly sort three numbers. This is the fastest and simplest way to sort three numbers. Got it?

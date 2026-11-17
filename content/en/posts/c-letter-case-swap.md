---
title: 'A Simple Way to Swap Letter Case in C'
date: 2017-11-13T22:35:29
categories: [Programming Languages]
tags: [C]
toc: true
original: true
csdn: 78525672
aiTranslated: true
---

> Reposted from my old CSDN blog: [C 语言字母大小写互换的简单方法](https://blog.csdn.net/zkx981105/article/details/78525672) (written 2017-11-13); formatting tidied during migration.

# Swapping letter case is actually really simple

Go back to the most basic way data is stored and look at uppercase and lowercase letters as 8-bit binary: you'll find that their low four bits are the same, while their high four bits differ slightly.

<!--more-->

----

## Examples:

| ASCII | DEC | BIN |
|----|----|----|
| 'A' | 65 | 01000001 |
| 'a' | 97 | 01100001 |
| 'B' | 66 | 01000010 |
| 'b' | 98 | 01100010 |
| 'X' | 88 | 01011000 |
| 'x' | 120 | 01111000|

Look closely and you'll see it's the sixth bit that differs!

----

# How to swap case

- Since the low four bits are exactly the same, we only need to flip the sixth bit (in the high four bits) to swap case
- To flip one bit of the high four bits without changing the low four bits, bitwise XOR `^` comes to mind. For more on bitwise XOR, see [按位异或](https://baike.baidu.com/item/%E5%BC%82%E6%88%96/10993677?fr=aladdin)

- From what we know about bitwise XOR, we can look for a number such that XOR-ing any 8-bit binary number with it flips the sixth bit (0/1) in the high four bits and leaves the low four bits unchanged

- Back to our goal: if we want to turn `'A'` into `'a'`, we need to turn `01000001` into `01100001`, i.e. change the `0` in the sixth bit into a `1`.

- We've found that number! Its binary is `00100000`, and in decimal it's `32`

- `01000001^00100000=01100001`. Pretty magical, right? Likewise, to turn lowercase `'a'` into `'A'`, you just XOR it with 32 too~

----

```c
#include<stdio.h>
int main(){
	int i;
	char s[100];
	// read in a string
	gets(s);
	for(i=0;s[i]!='\0';i++)
	{
		if((s[i]>='A'&&s[i]<='Z')||(s[i]>='a'&&s[i]<='z'))
		s[i]^=32;// core statement: swaps the case of letters in the string
	}
	printf("%s",s);
	return 0;
}
```

Sample input ->

```text
Hello,Java!
```

Sample output ->

```text
hELLO,jAVA!
```

## Pretty magical, huh!

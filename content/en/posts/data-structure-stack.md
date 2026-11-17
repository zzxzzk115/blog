---
title: 'Data Structures: Stack'
date: 2017-11-25T15:45:25
categories: [Algorithms]
tags: [Data Structures]
toc: true
original: true
csdn: 78632278
aiTranslated: true
---

> Reposted from my old CSDN blog: [数据结构-栈](https://blog.csdn.net/zkx981105/article/details/78632278) (written 2017-11-25); formatting tidied during migration.

# The Stack Abstract Data Type

```text
ADT Stack
Data
	 Same as a linear list. Elements have the same type, and adjacent elements have predecessor/successor relationships.
Operation
	 InitStack(*S) : Initialization; create an empty stack S.
	 DestroyStack(*S) : If the stack exists, destroy it.
	 ClearStack(*S) : Empty the stack.
	 StackEmpty(S) : Return true if the stack is empty, otherwise false.
	 GetTop(S,*e) : If the stack exists and is non-empty, return the top element of S in e.
	 Push(*S,e) : If stack S exists, insert new element e into S as its top element.
	 Pop(*S,*e) : Delete the top element of stack S and return its value in e.
	 StackLength(S) : Return the number of elements in stack S.
endADT
```

<!--more-->

----

# Sequential Storage Structure of a Stack

## Structure definition:

```c
#define MAXSIZE 1000
typedef int SElemtype;
typedef struct
{
    SElemtype data[MAXSIZE];
    int top;
}SqStack;
```

## Push:

```c
Status Push (SqStack *S,SElemtype e)
{
    if (S->top == MAXSIZE - 1)
    {
        return ERROR;
    }
    S->top ++ ;
    S->data[S->top] = e;
    return OK;
}
```

## Pop:

```c
Status Pop (SqStack *S,SElemtype *e)
{
    if (S->top == -1)
    {
        return ERROR;
    }
    *e = S->data[S->top];
    S->top --;
    return OK;
}
```

----

# Linked Storage Structure of a Stack

## Structure definition:

```c
typedef struct StackNode
{
	SElemType data;
	struct StackNode *next;
}StackNode,*LinkStackPtr;

typedef struct LinkStack
{
	LinkStackPtr top;
	int count;
}LinkStack;
```

## Push:

```c
Status Push(LinkStack *S, ElemType e)
{
	LinkStackPtr s = (LinkStackPtr) malloc(sizeof(StackNode));
	s->data = e;
	s->next = S->top;
	S->top = s;
	S->count++;
	return OK;
}
```

## Pop:

```c
Status Pop(LinkStack *S, SElemType *e)
{
	LinkStackPtr p;
	if(StackEmpty(*S))
		return ERROR;
	*e = S->top->data;
	p = S->top;
	S->top = S->top->next;
	free(p);
	S->count--;
	return OK;
}
```

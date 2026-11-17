---
title: '数据结构-栈'
date: 2017-11-25T15:45:25
categories: [算法与数据结构]
tags: [C]
toc: true
original: true
csdn: 78632278
---

> 本文转载自我在 CSDN 的旧博客：[数据结构-栈](https://blog.csdn.net/zkx981105/article/details/78632278)（写于 2017-11-25），迁移时整理了格式。

# 栈的抽象数据类型

```text
ADT 栈(stack)
Data
	 同线性表。元素具有相同的类型，相邻元素具有前驱和后继关系。
Operation
	 InitStack(*S) : 初始化操作，建立一个空栈S。
	 DestroyStack(*S) : 若栈存在，则销毁它。
	 ClearStack(*S) : 将栈清空。
	 StackEmpty(S) : 若栈为空，返回true，否则返回false。
	 GetTop(S,*e) : 若栈存在且非空，用e返回S的栈顶元素。
	 Push(*S,e) : 若栈S存在，插入新元素e到栈S中并成为栈顶元素。
	 Pop(*S,*e) : 删除栈S中栈顶元素，并用e返回其值。
	 StackLength(S) : 返回栈S的元素个数。
endADT
```

<!--more-->

----

# 栈的顺序存储结构

## 结构定义：

```c
#define MAXSIZE 1000
typedef int SElemtype;
typedef struct
{
    SElemtype data[MAXSIZE];
    int top;
}SqStack;
```

## 进栈：

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

## 出栈：

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

# 栈的链式储存结构

## 结构定义：

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

## 进栈：

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

## 出栈：

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

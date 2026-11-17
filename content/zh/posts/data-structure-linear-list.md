---
title: '数据结构 - 线性表'
date: 2017-11-18T23:19:50
categories: [算法]
tags: [数据结构]
toc: true
math: true
original: true
csdn: 78572087
---

> 本文转载自我在 CSDN 的旧博客：[数据结构 - 线性表](https://blog.csdn.net/zkx981105/article/details/78572087)（写于 2017-11-18），迁移时整理了格式。

```text
ADT 线性表(List)
Data
	线性表的数据对象集合为{a1,a2,......,an},每个元素的类型均为DataType。其中，除第一个元素a1外，每一个元素都有一个直接前驱元素，除了最后一个元素an外，每一个元素都有一个直接后继元素。数据元素直接的关系是一对一的关系。
Operation
	InitList(*L) :   初始化操作，建立一个空的线性表。
	ListEmpty(L) :   若线性表为空，返回true,否则返回false。
	ClearList(*L) :    将线性表清空。
	GetElem(L,i,*e) :  将线性表L中的第i个位置元素值返回给e。
	LocateElem(L,e) :  在线性表L中查找与给定值e相等的元素，如果查找成功，返回该元素在表中序号以表示成功；否则，返回0表示失败。
	ListInsert(*L,i,e)  :    在线性表L中的第i个位置插入新元素e。
	ListDelete(*L,i,*e) :    删除线性表L中第i个位置元素，并用e返回其值。
	ListLength(L) :          返回线性表L的元素个数。
endADT
```

<!--more-->

## 线性表的顺序存储结构

![线性表的顺序存储结构](/img/csdn/78572087-1.jpg)

![线性表的顺序存储结构 2](/img/csdn/78572087-2.jpg)

线性表的顺序存储的结构代码:

```c
#include <stdlib.h>
#define OK 1
#define ERROR 0
#define TRUE 1
#define FALSE 0
#define MAXSIZE 20
					  /*存储空间初始分配量*/
typedef int Status;   /*Status是函数的类型，其值是函数结果状态代码，如OK等*/
typedef int ElemType; /*ElemType类型根据实际情况而定，这里假设为int*/
typedef struct
{
	ElemType data[MAXSIZE]; /*数组存储数据元素，最大值为MAXSIZE*/
	int length;              /*线性表当前长度*/
}SqList;
```

顺序线性表的初始化操作代码：

```c
/* 初始条件：顺序线性表L不存在。 */
/* 操作结果：生成顺序线性空表L。 */
Status InitList (SqList *L)
{
    L = (SqList *)malloc(sizeof(SqList));
    if (!L)
    {
	    exit(0);
	    return ERROR;
    }
    L->length = 0;
    return OK;
}
```

判断顺序线性表是否为空操作的代码：

```c
/* 初始条件：顺序线性表L已存在。*/
/* 操作结果：返回判断的值      */
Status ListEmpty (SqList L)
{
    if (L.length == 0)
        return TRUE;
    else
        return FALSE;
}
```

顺序线性表清空操作的代码：

```c
/* 初始条件：顺序线性表L已存在。*/
/* 操作结果：将L重置为空表     */
Status ClearList(SqList *L)
 {
   (*L).length = 0;
   return OK;
 }
```

顺序线性表获得元素操作的代码：

```c
/* 初始条件：顺序线性表L已存在，1<=i<=ListLength(L)*/
/* 操作结果：用e返回L中第i个数据元素的值*/
Status GetElem (SqList L,int i,ElemType *e)
{
	if (L.length==0 || i<1 || i>L.length)
		return ERROR;
	*e = L.data[i-1];
	return OK;
}
```

顺序线性表查找元素操作的代码：

```c
/* 初始条件：顺序线性表L已存在。*/
/* 操作结果：若找到与e相等的值，则返回序号，否则返回0代表失败*/
Status LocateElem (SqList L,ElemType e)
{
    ElemType k;
    for (k=0;k<L.length;k++)
    {
        if (L.data[k] == e)
        {
	        break;
            return k+1;
        }
    }
    return 0;
}
```

顺序线性表插入元素操作的代码：

```c
/* 初始条件：顺序线性表L已存在，1<=i<=ListLength(L)*/
/* 操作结果：在L中第i个位置之前插入新的数据元素e,L的长度加1*/
Status ListInsert (SqList *L,int i,ElemType e)
{
	int k;
	if (L->length==MAXSIZE)   /*线性表已满*/
		return ERROR;
	if (i<1 || i>L->length+1) /*i不在范围内*/
		return ERROR;
	if (i<=L->length)         /*插入数据不在表尾*/
	{
		for (k=L->length-1;k>=i-1;k--)
			L->data[k+1] = L->data[k];
	}
	L->data[i-1] = e;         /*将新元素插入*/
	L->length++;
	return OK;
}
```

顺序线性表删除元素操作的代码：

```c
/* 初始条件：顺序线性表L已存在，1<=i<=ListLength(L)*/
/* 操作结果：删除L的第i个数据元素，并用e返回其值，L的长度减1*/
Status ListDelete(SqList *L,int i,ElemType *e)
{
	int k;
	if (L->length==0)        /*线性表为空*/
		return ERROR;
	if (i<1 || i>L->length)  /*删除位置不正确*/
		return ERROR;
	*e = L->data[i-1];
	if (i<L->length)         /*如果删除不是最后位置*/
	{
		for (k=i;k<L->length;k++) /*将删除位置后继元素前移*/
			L->data[k-1] = L->data[k];
	}
	L->length--;
	return OK;
}
```

### 优缺点

-  优点
	-  无需为表示表中元素之间的逻辑关系而增加额外的存储空间
	-  可以快速地存取表中任意位置的元素
-  缺点
	-  插入和删除操作需要移动大量元素
	- 当线性表长度变化较大时，难以确定存储空间的容量
	- 造成存储空间的“碎片”

----

## 线性表的链式存储结构

### 单链表

![单链表](/img/csdn/78572087-3.jpg)

![单链表 2](/img/csdn/78572087-4.jpg)

线性表的单链表结构：

```c
/* 线性表的单链表存储结构 */
typedef struct Node
{
    ElemType data;
    struct Node *next;
}Node;
typedef struct Node *LinkList; /* 定义LinkList */
```

单链表的读取操作代码：

```c
/* 初始条件：单链表L已存在，1<=i<=ListLength(L) */
/* 操作结果：用e返回L中第i个数据元素的值 */
Status GetElem (LinkList L,int i,ElemType *e)
{
    int j;
    LinkList p;        	/* 声明一指针p */
    p = L->next;		/* 让指针p指向链表L的第一个节点 */
    j = 1;				/* j为计数器 */
    while (p && j<i)
    {
        p = p->next;
        ++j;
    }
    if (!p || j>i)
        return ERROR;
    *e = p->data;
    return OK;
}
```

单链表的插入操作代码：

![单链表插入](/img/csdn/78572087-5.jpg)

```c
/* 初始条件：单链表L已存在，1<=i<=ListLength(L) */
/* 操作结果：在L中第i个节点位置之前插入新的数据元素e，L的长度加1 */
Status ListInsert (LinkList *L,int i,ElemType e)
{
    int j;
    LinkList p,s;
    j = 1;
    while (p && j<i)
    {
        p = p->next;
        ++j;
    }
    if (!p || j>i)
        return ERROR;
    s = (LinkList)malloc(sizeof(Node));
    s->data = e;				/* 把新的数据元素存入s的数据域 */
    s->next = p->next;    /* 把p的后继节点赋值给s的后继 */
    p->next = s;				/* 把s赋值给p的后继 */
    return OK;
}
```

单链表的删除操作代码：

![单链表删除](/img/csdn/78572087-6.jpg)

```c
/* 初始条件：单链表L已存在，1<=i<=ListLength(L) */
/* 操作结果：删除L的第i个节点，并用e返回其值，L的长度减1 */
Status ListDelete (LinkList *L,int i,ElemType *e)
{
    int j;
    LinkList p,q;
    p = *L;
    j = 1;
    while (p && j<i)
    {
        p = p->next;
        ++j;
    }
    if (!p || j>i)
        return ERROR;
    q = p->next;				/* 将q指向p的后继 */
    p->next = q->next;		/* 将q的后继赋值给p的后继 */
    *e = q->data;			/* 将q中的数据给e */
    free(q);					/* 回收节点q，释放内存 */
    return OK;
}
```

单链表的整表创建：

- 头插法：

![头插法](/img/csdn/78572087-7.jpg)

```c
void CreateListHead (LinkList *L,int n)
{
    LinkList *p;
    int i;
    srand(time(0));
    *L = (LinkList)malloc(sizeof(Node));
    (*L)->next = NULL;
    for (i=0;i<n;i++)
    {
        p = (LinkList)malloc(sizeof(Node));
        p->data = rand()%100+1;
        p->next = (*L)->next;
        (*L)->next = p;
    }
}
```

- 尾插法：

![尾插法](/img/csdn/78572087-8.jpg)

```c
void CreateListTail (LinkList *L,int n)
{
    LinkList p,r;
    int i;
    srand(time(0));
    *L = (LinkList)malloc(sizeof(Node));
    r = *L;
    for (i=0;i<n;i++)
    {
        p = (Node*)malloc(sizeof(Node));
        p->data = rand()%100+1;
        r->next = p;
        r = p;
    }
    r->next = NULL;
}
```

单链表的整表删除

```c
Status ClearList (LinkList *L)
{
    LinkList p,q;
    p = (*L)->next;
    while (p)
    {
        q = p->next;
        free(q);
        p = q;
    }
    (*L)->next = NULL;
    return OK;
}
```

#### 单链表与顺序存储结构的优缺点对比

- 存储分配方式

	- 顺序存储结构用一段连续的存储单元依次存储线性表的数据元素

	- 单链表采用链式存储结构，用一组任意的存储单元存放线性表的元素

- 时间性能

	- 查找

		- 顺序存储结构 $O(1)$

		- 单链表 $O(n)$

	- 插入和删除

		- 顺序存储结构需要平均移动表长一半的元素，时间为 $O(n)$

		- 单链表在线出某位置的指针后，插入和删除时间仅为 $O(1)$

- 空间性能

	- 顺序存储结构需要预分配存储空间，分大了，浪费，分小了易发生上溢

	- 单链表不需要分配存储空间，只要有就可以分配，元素个数也不受限制

----

### 静态链表

**“用数组描述的链表叫做静态链表”**，结构体数组分别存放数据(data 域) 和游标(Cursor,为 0 时无指向)。

![静态链表](/img/csdn/78572087-9.jpg)

```c
#include <stdio.h>
#include <stdlib.h>

#define MAXSIZE 1000    /* 存储空间起始分配量 1000 */
#define OK 1
#define ERROR 0

typedef int ElemType;		/* 视具体情况而定 假定数组存int */
typedef int Status;

/* 线性表的静态链表存储结构 */
typedef struct
{
    ElemType data;
    int cur;
}Component,StaticLinkList[MAXSIZE];

/* 获得表长 */
int ListLength (StaticLinkList L)
{
    int j=0;
    int i=L[MAXSIZE-1].cur;
    while (i)
    {
        i = L[j].cur;
        j++;
    }
    return j;
}

/* 初始化 */
/* 将一维数组space中各分量链成一个备用链表，space[0].cur为头指针，"0"表示空指针 */
Status InitList (StaticLinkList space)
{
    int i;
    for (i=0;i<MAXSIZE-1;i++)
        space[i].cur = i+1;
    space[MAXSIZE-1].cur = 0;			/* 目前静态链表为空，最后一个元素的cur为0 */
    return OK;
}

/* 预分配空闲空间 */
/* 若备用空间链表非空，则返回分配的结点下标，否则返回0 */
int Malloc_SLL (StaticLinkList space)
{
    int i = space[0].cur;					/*返回的第一个备用空闲的下标 */

    if (space[0].cur)
        space[0].cur = space[i].cur;		/*把要用的元素的下一个分量用来做备用 */

    return i;
}

/*  将下标为k的空闲结点回收到备用链表 */
void Free_SSL (StaticLinkList space,int k)
{
    space[k].cur = space[0].cur;		/* 把第一个元素的cur值赋给要删除的分量cur */
    space[0].cur = k;					/* 把要删除的分量下标赋值给第一个元素的cur */
}

/*  在L中第i个元素之前插入新的数据元素e   */
Status ListInsert (StaticLinkList L,int i,ElemType e)
{
    int j,k,l;
    k = MAXSIZE-1;
    if (i<1 || i>ListLength(L)+1)
        return ERROR;
    j = Malloc_SLL(L);        /* 获得空闲分量的下标 */
    if (j)
    {
        L[j].data = e;
        for (l=1;l<=i-1;l++)    /* 找到第i个元素之前的位置 */
            k = L[k].cur;
        L[j].cur = L[k].cur;    /* 把第i个元素之前的cur赋值给新元素的cur */
        L[k].cur = j;           /* 把新元素的下标赋值给第i个元素之前元素的cur */
        return OK;
    }
    return ERROR;
}

/* 删除下标为i的元素 */
Status ListDelete (StaticLinkList L,int i)
{
    int j,k;
    if (i<1 || i> ListLength(L))
        return ERROR;
    k = MAXSIZE-1 ;
    for (j=1;j<i-1;j++)
        k = L[k].cur;
    j = L[k].cur;
    L[k].cur = L[j].cur;
    Free_SSL (L,j);
    return OK;
}

```

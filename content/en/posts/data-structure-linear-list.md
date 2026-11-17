---
title: 'Data Structures: Linear List'
date: 2017-11-18T23:19:50
categories: [Algorithms]
tags: [Data Structures]
toc: true
math: true
original: true
csdn: 78572087
aiTranslated: true
---

> Reposted from my old CSDN blog: [数据结构 - 线性表](https://blog.csdn.net/zkx981105/article/details/78572087) (written 2017-11-18); formatting tidied during migration.

```text
ADT List
Data
	The data object set of the linear list is {a1,a2,......,an}, and every element is of type DataType. Except for the first element a1, every element has exactly one direct predecessor; except for the last element an, every element has exactly one direct successor. The relationship between data elements is one-to-one.
Operation
	InitList(*L) :   Initialization; creates an empty linear list.
	ListEmpty(L) :   Returns true if the linear list is empty, otherwise false.
	ClearList(*L) :    Clears the linear list.
	GetElem(L,i,*e) :  Returns the value of the element at position i in list L via e.
	LocateElem(L,e) :  Searches list L for an element equal to the given value e; if found, returns that element's position in the list to indicate success; otherwise returns 0 to indicate failure.
	ListInsert(*L,i,e)  :    Inserts a new element e at position i in list L.
	ListDelete(*L,i,*e) :    Deletes the element at position i in list L and returns its value via e.
	ListLength(L) :          Returns the number of elements in list L.
endADT
```

<!--more-->

## Sequential Storage Structure of a Linear List

![Sequential storage structure of a linear list](/img/csdn/78572087-1.jpg)

![Sequential storage structure of a linear list 2](/img/csdn/78572087-2.jpg)

Structure code for sequential storage of a linear list:

```c
#include <stdlib.h>
#define OK 1
#define ERROR 0
#define TRUE 1
#define FALSE 0
#define MAXSIZE 20
					  /*Initial allocation size of the storage space*/
typedef int Status;   /*Status is the function return type; its value is a result status code such as OK*/
typedef int ElemType; /*ElemType depends on the actual situation; here we assume int*/
typedef struct
{
	ElemType data[MAXSIZE]; /*Array storing the data elements, max size MAXSIZE*/
	int length;              /*Current length of the linear list*/
}SqList;
```

Code for initializing a sequential linear list:

```c
/* Precondition: sequential linear list L does not exist. */
/* Result: creates an empty sequential linear list L. */
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

Code for checking whether a sequential linear list is empty:

```c
/* Precondition: sequential linear list L exists.*/
/* Result: returns the result of the check      */
Status ListEmpty (SqList L)
{
    if (L.length == 0)
        return TRUE;
    else
        return FALSE;
}
```

Code for clearing a sequential linear list:

```c
/* Precondition: sequential linear list L exists.*/
/* Result: resets L to an empty list     */
Status ClearList(SqList *L)
 {
   (*L).length = 0;
   return OK;
 }
```

Code for getting an element from a sequential linear list:

```c
/* Precondition: sequential linear list L exists, 1<=i<=ListLength(L)*/
/* Result: returns the value of the i-th data element of L via e*/
Status GetElem (SqList L,int i,ElemType *e)
{
	if (L.length==0 || i<1 || i>L.length)
		return ERROR;
	*e = L.data[i-1];
	return OK;
}
```

Code for finding an element in a sequential linear list:

```c
/* Precondition: sequential linear list L exists.*/
/* Result: if a value equal to e is found, returns its position; otherwise returns 0 for failure*/
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

Code for inserting an element into a sequential linear list:

```c
/* Precondition: sequential linear list L exists, 1<=i<=ListLength(L)*/
/* Result: inserts new data element e before position i in L; L's length increases by 1*/
Status ListInsert (SqList *L,int i,ElemType e)
{
	int k;
	if (L->length==MAXSIZE)   /*The linear list is full*/
		return ERROR;
	if (i<1 || i>L->length+1) /*i is out of range*/
		return ERROR;
	if (i<=L->length)         /*The insert position is not at the end of the list*/
	{
		for (k=L->length-1;k>=i-1;k--)
			L->data[k+1] = L->data[k];
	}
	L->data[i-1] = e;         /*Insert the new element*/
	L->length++;
	return OK;
}
```

Code for deleting an element from a sequential linear list:

```c
/* Precondition: sequential linear list L exists, 1<=i<=ListLength(L)*/
/* Result: deletes the i-th data element of L and returns its value via e; L's length decreases by 1*/
Status ListDelete(SqList *L,int i,ElemType *e)
{
	int k;
	if (L->length==0)        /*The linear list is empty*/
		return ERROR;
	if (i<1 || i>L->length)  /*Invalid delete position*/
		return ERROR;
	*e = L->data[i-1];
	if (i<L->length)         /*If the deleted position is not the last one*/
	{
		for (k=i;k<L->length;k++) /*Shift the elements after the deleted position forward*/
			L->data[k-1] = L->data[k];
	}
	L->length--;
	return OK;
}
```

### Pros and Cons

-  Pros
	-  No extra storage space is needed to represent the logical relationships between elements in the list
	-  Any element at any position in the list can be accessed quickly
-  Cons
	-  Insertion and deletion require moving a large number of elements
	- When the length of the linear list varies a lot, it's hard to decide the storage capacity
	- It causes "fragmentation" of the storage space

----

## Linked Storage Structure of a Linear List

### Singly Linked List

![Singly linked list](/img/csdn/78572087-3.jpg)

![Singly linked list 2](/img/csdn/78572087-4.jpg)

Singly linked list structure of a linear list:

```c
/* Singly linked list storage structure of a linear list */
typedef struct Node
{
    ElemType data;
    struct Node *next;
}Node;
typedef struct Node *LinkList; /* Define LinkList */
```

Code for reading from a singly linked list:

```c
/* Precondition: singly linked list L exists, 1<=i<=ListLength(L) */
/* Result: returns the value of the i-th data element of L via e */
Status GetElem (LinkList L,int i,ElemType *e)
{
    int j;
    LinkList p;        	/* Declare a pointer p */
    p = L->next;		/* Make p point to the first node of list L */
    j = 1;				/* j is a counter */
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

Code for inserting into a singly linked list:

![Singly linked list insertion](/img/csdn/78572087-5.jpg)

```c
/* Precondition: singly linked list L exists, 1<=i<=ListLength(L) */
/* Result: inserts new data element e before the i-th node in L; L's length increases by 1 */
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
    s->data = e;				/* Store the new data element in s's data field */
    s->next = p->next;    /* Assign p's successor to s's successor */
    p->next = s;				/* Assign s to p's successor */
    return OK;
}
```

Code for deleting from a singly linked list:

![Singly linked list deletion](/img/csdn/78572087-6.jpg)

```c
/* Precondition: singly linked list L exists, 1<=i<=ListLength(L) */
/* Result: deletes the i-th node of L and returns its value via e; L's length decreases by 1 */
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
    q = p->next;				/* Point q to p's successor */
    p->next = q->next;		/* Assign q's successor to p's successor */
    *e = q->data;			/* Give the data in q to e */
    free(q);					/* Reclaim node q and free its memory */
    return OK;
}
```

Creating a whole singly linked list:

- Head insertion:

![Head insertion](/img/csdn/78572087-7.jpg)

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

- Tail insertion:

![Tail insertion](/img/csdn/78572087-8.jpg)

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

Deleting a whole singly linked list

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

#### Singly Linked List vs. Sequential Storage Structure

- Storage allocation

	- The sequential storage structure stores the data elements of the linear list one after another in a contiguous block of storage units

	- The singly linked list uses a linked storage structure, storing the list's elements in an arbitrary set of storage units

- Time performance

	- Lookup

		- Sequential storage structure $O(1)$

		- Singly linked list $O(n)$

	- Insertion and deletion

		- The sequential storage structure has to move, on average, half the list's elements, so it takes $O(n)$

		- Once the singly linked list has found the pointer at a given position, insertion and deletion take only $O(1)$

- Space performance

	- The sequential storage structure needs storage space pre-allocated: allocate too much and it's wasted, allocate too little and it easily overflows

	- The singly linked list doesn't need storage pre-allocated; as long as there's space it can be allocated, and the number of elements isn't limited either

----

### Static Linked List

**"A linked list described using an array is called a static linked list"**: an array of structs stores the data (the data field) and the cursor (Cursor; 0 means it points nowhere) separately.

![Static linked list](/img/csdn/78572087-9.jpg)

```c
#include <stdio.h>
#include <stdlib.h>

#define MAXSIZE 1000    /* Initial storage allocation size: 1000 */
#define OK 1
#define ERROR 0

typedef int ElemType;		/* Depends on the situation; assume the array stores int */
typedef int Status;

/* Static linked list storage structure of a linear list */
typedef struct
{
    ElemType data;
    int cur;
}Component,StaticLinkList[MAXSIZE];

/* Get the list length */
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

/* Initialization */
/* Link all components of the 1-D array space into a spare list; space[0].cur is the head pointer, and "0" means a null pointer */
Status InitList (StaticLinkList space)
{
    int i;
    for (i=0;i<MAXSIZE-1;i++)
        space[i].cur = i+1;
    space[MAXSIZE-1].cur = 0;			/* The static linked list is currently empty; the last element's cur is 0 */
    return OK;
}

/* Pre-allocate free space */
/* If the spare space list is not empty, return the index of the allocated node; otherwise return 0 */
int Malloc_SLL (StaticLinkList space)
{
    int i = space[0].cur;					/*The index of the first spare free slot to return */

    if (space[0].cur)
        space[0].cur = space[i].cur;		/*Use the next component of the element being taken as the spare */

    return i;
}

/*  Reclaim the free node at index k into the spare list */
void Free_SSL (StaticLinkList space,int k)
{
    space[k].cur = space[0].cur;		/* Assign the first element's cur value to the cur of the component being deleted */
    space[0].cur = k;					/* Assign the index of the component being deleted to the first element's cur */
}

/*  Insert new data element e before the i-th element in L   */
Status ListInsert (StaticLinkList L,int i,ElemType e)
{
    int j,k,l;
    k = MAXSIZE-1;
    if (i<1 || i>ListLength(L)+1)
        return ERROR;
    j = Malloc_SLL(L);        /* Get the index of a free component */
    if (j)
    {
        L[j].data = e;
        for (l=1;l<=i-1;l++)    /* Find the position just before the i-th element */
            k = L[k].cur;
        L[j].cur = L[k].cur;    /* Assign the cur of the element before the i-th one to the new element's cur */
        L[k].cur = j;           /* Assign the new element's index to the cur of the element before the i-th one */
        return OK;
    }
    return ERROR;
}

/* Delete the element at index i */
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

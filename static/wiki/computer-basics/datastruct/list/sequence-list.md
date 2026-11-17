# 顺序表 Sequence List

> 顺序存储的线性表，在物理内存中连续存放。

## 定义

采用顺序存储结构的线性表成为顺序表。一般使用数组或指针实现。

## 使用数组实现

### 结构定义

![an-element](http://img.zhangkexuan.cn/markdown_20201113114338.png)

如图，顺序表使用数组实现时，顺序表的结构拥有两个数据域：Data和Length，Data是存放所有顺序表数据元素的数组，Length是存放顺序表的长度的整型变量。

使用C风格实现：

```cpp
#define MAX 100
typedef int ElemType;

typedef struct
{
    ElemType data[MAX];
    int length;
}SeqList;
```

### 初始化

初始化非常简单：

```cpp
void InitList(SeqList* L)
{
    if(L == NULL)
        return;
    L->length = 0;
}
```

### 得到长度

```cpp
int GetLength(SeqList* L)
{
    if(L == NULL)
        return 0;
    else
        return L->length;
}
```

### 根据索引得到数据

先判断给定的索引值是否合法，如果不合法，则返回INT_MIN，如果合法，则返回对应索引的数据值。由于顺序表的下标从1开始，而data数组下标从0开始，所以返回的是data[i-1]对应的值。

```cpp
ElemType GetData(SeqList* L, int i)
{
    if(i < 1 || i > L->length)
        return INT_MIN;
    return L->data[i-1];
}
```

### 插入

插入操作比较耗费性能，因为每次插入某元素到某位置时，该位置后面的所有元素需要整体往后移动，从尾部开始移动。

```cpp
bool Insert(SeqList* L, int i, ElemType e)
{
    if(i < 1 || i > L->length)
    	return false;
    else if(L->length >= MAX)
        return false;
    else
    {
        for(int k = L->length; k >= i; k--)
        {
            L->data[k] = L->data[k-1];
        }
        L-data[i - 1] = e;
        L->length++;
        return true;
    }
}
```

### 删除

删除和插入类似，均需要整体的移动。

```cpp
bool Delete(Seqlist* L, int i, ElemType& e)
{
    if(i < 1 || i > L->length)
        return false;
    e = L->data[i - 1];
    for(int k = i; k < L->length; k++)
    {
        L->data[k - 1] = L->data[k];
    }
    L->length--;
    return true;
}
```

### 查找

```cpp
int Locate(SeqList* L, ElemType e)
{
    for(int i = 1; i <= L->length; i+)
    {
        if(L->data[i - 1] == e)
            return i;
    }
    return 0;
}
```










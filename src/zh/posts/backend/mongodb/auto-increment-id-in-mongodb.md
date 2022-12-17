---
title: 在 MongoDB 中实现自增 ID
author: Lazy_V
date: 2022-11-27
category:
  - 后端
tag:
  - MongoDB
  - 数据库
isOriginal: true
---

在 MongoDB 中，每个文档都有一个 object id (Bson ID)。但有时我们创建新模型的时候，需要能够自增的 ID，并且 ID 应该是从 1 开始的整数。怎么解决这个问题呢？

<!-- more -->

## 怎么解决这个问题

为了解决这个问题，我们需要创建一个名为 AutoIncrementIdCollection 的新集合，其中我们插入一些有两个字段的模型（AutoIncrementIdModel）：

1. CollectionName --> 集合的名称
2. Sequence --> 集合当前的序列值，默认值为 0。

每次在将新的索引模型 M 插入集合 C 之前，我们都会找到一个 CollectionName 为 C 的 AutoIncrementIdModel，并将其序列加一，然后使用该序列创建 M（M 的 id 字段由序列初始化）并将其插入 C。
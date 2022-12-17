---
title: Implement automatically increase ids in MongoDB
author: Lazy_V
date: 2022-11-27
category:
  - Backend
tag:
  - MongoDB
  - Database
isOriginal: true
---

In MongoDB, every documents have an object id (Bson ID). But sometimes we need ids that can automatically increase when creating a new model. And the id should be an integer starts from 1. How to deal with the problem?

<!-- more -->

## How to solve the problem

To solve the problem, we have to create a new collection named AutoIncrementIdCollection, in which we insert some models (AutoIncrementIdModel) that have two fields: 

1. CollectionName --> The name of a collection.
2. Sequence --> The current sequence of a collection. The default value of it should be 0.

Everytime before inserting a new indexed model M to a collection C, we find a AutoIncrementIdModel whose CollectionName is C, and we increase its Sequence by one, then use that sequence to create M (M's id field be initialized by the sequence) and insert it to C.
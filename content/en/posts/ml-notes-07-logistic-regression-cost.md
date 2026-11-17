---
title: 'Machine Learning Notes (7): Logistic Regression Cost Function'
date: 2018-04-19T19:01:17
categories: [Machine Learning]
tags: [Deep Learning, Logistic Regression]
toc: true
original: true
csdn: 80009225
aiTranslated: true
---

> Reposted from my old CSDN blog: [机器学习笔记(7)——逻辑回归：代价函数](https://blog.csdn.net/zkx981105/article/details/80009225) (written 2018-04-19); formatting tidied during migration.

## Logistic Regression: Cost Function

To train the parameters w and b, we need to define a cost function.

<!--more-->

Overview:

![](/img/csdn/80009225-1.png)

(tips: ![](/img/csdn/80009225-2.png) is the i-th training example)

### Loss Function

The loss function computes the difference between the prediction ![](/img/csdn/80009225-3.png) and the desired output ![](/img/csdn/80009225-4.png). In other words, the loss function computes the error for a single training example.

![](/img/csdn/80009225-5.png)

- If ![](/img/csdn/80009225-6.png), then ![](/img/csdn/80009225-7.png) should be close to 1
- If ![](/img/csdn/80009225-8.png), then ![](/img/csdn/80009225-7.png) should be close to 0

### Cost Function

The cost function is the average of the loss function over the entire training set. We'll find the parameters w and b that make the cost function as small as possible.

![](/img/csdn/80009225-9.png)

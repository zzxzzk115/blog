---
title: 'Machine Learning Notes (5): Binary Classification'
date: 2018-04-16T23:08:55
categories: [Machine Learning]
tags: [Machine Learning]
original: true
csdn: 79968075
aiTranslated: true
---

> Reposted from my old CSDN blog: [机器学习笔记(5)——二分分类](https://blog.csdn.net/zkx981105/article/details/79968075) (written 2018-04-16); formatting tidied during migration.

## Binary Classification

In a binary classification problem, the result is a discrete-valued output.

<!--more-->

Example: cat vs. no cat

The goal is to train a classifier whose input is an image represented by a feature vector x, and to predict whether the corresponding label y is 1 or 0. In this case, that means whether the picture is one with a cat (1) or one without a cat (0).

![](/img/csdn/79968075-1.png)

An image stored in a computer is made up of three matrices, one for each of the red, green, and blue color channels. For example, if an image is 64 pixels \* 64 pixels, then the three RGB matrices are also 64\*64.

![](/img/csdn/79968075-2.png)

---
title: 'Machine Learning Notes (6): Logistic Regression'
date: 2018-04-19T18:34:30
categories: [Machine Learning]
tags: [Deep Learning, Logistic Regression]
original: true
csdn: 80008903
aiTranslated: true
---

> Reposted from my old CSDN blog: [机器学习笔记(6)——逻辑回归](https://blog.csdn.net/zkx981105/article/details/80008903) (written 2018-04-19); formatting tidied during migration.

## Logistic Regression

Logistic regression is a learning algorithm used for supervised learning problems where the output y is always either 0 or 1. The goal of logistic regression is to minimize the error between its predictions and the training data.

<!--more-->

Example: cat VS not a cat

Given an image represented by a feature vector x, the algorithm estimates the probability that the picture is a cat.

![](/img/csdn/80008903-1.png)

Parameters used in logistic regression:

- Input feature vector: ![](/img/csdn/80008903-2.png), where ![](/img/csdn/80008903-3.png) is the number of features
- Training label: ![](/img/csdn/80008903-4.png)
- Weights: ![](/img/csdn/80008903-5.png), where ![](/img/csdn/80008903-3.png) is the number of features
- Threshold: ![](/img/csdn/80008903-6.png)
- Output: ![](/img/csdn/80008903-7.png)
- Sigmoid function: ![](/img/csdn/80008903-8.png)

![](/img/csdn/80008903-9.png)

![](/img/csdn/80008903-10.png) is a linear function ![](/img/csdn/80008903-11.png), and we use the Sigmoid function to keep the probability within [0,1]

From the graph we can see:

- If z is a large positive number, then sigmoid(z) = 1
- If z is a large negative number, then sigmoid(z) = 0
- If z = 0, then sigmoid(z) = 0.5

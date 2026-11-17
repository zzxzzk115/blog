---
title: 'Machine Learning Notes (3): Supervised Learning'
date: 2018-04-16T22:32:55
categories: [Machine Learning]
tags: [Machine Learning]
original: true
csdn: 79967405
aiTranslated: true
---

> Reposted from my old CSDN blog: [机器学习笔记(3)——监督学习](https://blog.csdn.net/zkx981105/article/details/79967405) (written 2018-04-16); formatting tidied during migration.

## Supervised Learning with Neural Networks

In supervised learning, we're given a dataset and already know what the correct output should look like, with the idea that there's a relationship between the input and the output.

<!--more-->

Supervised learning problems fall into two categories: "regression" and "classification". In a regression problem, we try to predict results with a continuous output, which means we try to map the input variables to some continuous function. In a classification problem, we instead try to predict results with a discrete output. In other words, we try to map the input variables into distinct, discrete categories.

Here are some examples of supervised learning

![](/img/csdn/79967405-1.png)

There are several different kinds of neural networks. For example, the *Convolution Neural Network (CNN)* is often used for image recognition, while the Recurrent Neural Network (RNN) is used for one-dimensional sequence data, such as translating English into Chinese or turning audio into text. For self-driving cars, it's a hybrid neural network architecture.

Structured data vs. unstructured data

Structured data means things with numeric definitions, like price and age, while unstructured data means things like pixels, audio, and text.

![](/img/csdn/79967405-2.png)

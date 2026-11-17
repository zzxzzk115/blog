---
title: 'Machine Learning Notes (2): What Is a Neural Network'
date: 2018-04-16T22:00:18
categories: [Machine Learning]
tags: [Machine Learning]
toc: true
original: true
csdn: 79966886
aiTranslated: true
---

> Reposted from my old CSDN blog: [机器学习笔记(2)——什么是神经网络](https://blog.csdn.net/zkx981105/article/details/79966886) (written 2018-04-16); formatting tidied during migration.

## What Is a Neural Network?

It's a powerful learning algorithm inspired by the question of "how the brain works".

<!--more-->

##### Example 1 - A Single Neural Network

Given data on the floor area of houses on the real market, you want to find a suitable function that predicts a house's price. This is a linear regression problem, because the house price as a function of floor area is a continuous output.

We know a price can never be negative, so we'll build a function called a *Rectified Linear Unit (ReLU)*, which starts at 0.

![](/img/csdn/79966886-1.png)

The input is the floor area of the house (x)

The output is the price of the house (y)

The "neuron" in the figure below implements the ReLU function (the blue line)

![](/img/csdn/79966886-2.png)

##### Example 2 - A Multiple Neural Network

A house's price can be affected by other features such as floor area, number of bedrooms, zip code, and wealth (of the neighborhood). The job of the neural network is to predict the house price, and it will generate the hidden units automatically. All we need to provide is the input x and the output y.

![](/img/csdn/79966886-3.png)

(All of the above was translated by me at a level that hasn't even passed CET-4 yet. Good enough if you can understand it; if anything's wrong, feel free to point it out, thanks.)

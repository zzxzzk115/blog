---
lang: en-US
title: The algorithm framework for solving DP problems
author: Lazy_V
date: 2022-12-09
category:
  - Algorithms
tag:
  - Algorithms
  - Dynamic Programming
---

Dynamic Programming problems are the most complicated problems in algorithms. However, it is actually simple to solve if you understand the key concepts and the main algorithm framework of DP.

<!-- more -->

## What is Dynamic Programming (DP) ?

Dynamic Programming (DP) is a method for solving complex problems by breaking them down into smaller subproblems. It is a bottom-up approach, meaning it starts with solving the smaller subproblems and then uses those solutions to build up to a solution for the larger problem.

To solve a problem with DP, the problem must have the following properties:

1. Optimal substructure: The optimal solution to a problem can be constructed from optimal solutions to its subproblems.

2. Overlapping subproblems: A problem can be broken down into subproblems that are reused multiple times.

## A classic DP problem : Fibonacci

For an instance, when we calculate the Fibonacci sequence, we can use DP.

::: tip
The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding numbers, starting with 0 and 1. The sequence goes as follows: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, and so on. The sequence is named after Leonardo of Pisa, who was known as Fibonacci. He introduced the sequence to Western European mathematics in his book "Liber Abaci" in the year 1202.
:::

In general, for calculating the Fibonacci sequence, we use recursion functions, like the following:

```cpp
int Fibonacci(int n) {
  if (n == 0) {
		return 0;
	}
	if (n == 1 || n == 2) {
		return 1;
	}
	return Fibonacci(n - 1) + Fibonacci(n - 2);
}
```

The technique we use is just Recursion, not DP.

The function call tree has a lot of nodes, but many of them are duplicated.

I have an equation:

DP = Recursion + Memoization OR Tabulation + optional improvements.

What does it mean?

Well, Memoization and tabulation are two techniques used to improve the performance of algorithms that use Dynamic Programming.

Memoization is a technique that involves storing the results of intermediate calculations in a table, so that they can be reused later. This can help to reduce the overall time complexity of the algorithm by avoiding the need to recalculate the same subproblems multiple times. It's top-bottom.

Tabulation, on the other hand, is a technique that involves storing the final results of all the subproblems in a table. This allows the algorithm to avoid recomputing the solutions to the subproblems and simply look up the pre-computed results in the table. It's bottom-up.

Both memoization and tabulation can be used to speed up Dynamic Programming algorithms. The choice between the two techniques often depends on the specific problem being solved and the amount of available memory.

### Using Memoization

To use Memoization, we could define a look-up table or a cache table for saving calculated results. To define that table, we generally use a hash table.

In C++, we will use std::unordered_map.

For example, we can use Memoization to solve the Fibonacci problem:

```cpp
std::unordered_map<int, int> memo;

int Fibonacci(int n) {
  if (n == 0) {
		return 0;
	}
	if (n == 1 || n == 2) {
		return 1;
	}
  if (memo.count(n) > 0) {
    return memo[n];
  } else {
    memo[n] = Fibonacci(n - 1) + Fibonacci(n - 2);
  }
	return memo[n];
}
```

Now, all the duplicated nodes are gone, we calculate `Fibonacci(i)` just one time.

### Using Tabulation

We can also use Tabulation for solving the problem. To use Tabulation, we could define an array or a vector for saving results of sub-problems.

In C++, we will use std::vector.

Here is the implementation of Fibonacci by using Tabulation:

```cpp
int Fibonacci(int n) {
  if (n == 0) {
		return 0;
	}
	if (n == 1 || n == 2) {
		return 1;
	}
  std::vector<int> d(n + 1);
  for (int i = 3; i <= n; i++) {
    d[i] = d[i - 1] + d[i - 2];
  }
  return d[n];
}
```

### Optional improvements

There is an optional improvement called State Compression.

State compression is a technique used in Dynamic Programming to reduce the amount of memory needed to store the intermediate results of a calculation. It involves representing the state of a subproblem using a smaller data structure, such as a bit vector or a hash table, instead of a larger data structure like an array or a matrix. This can help to reduce the space complexity of the algorithm and make it possible to solve larger problems or problems with more complex subproblems.

In this case, we replace `d` with two integers: `pre` and `curr`:

```cpp
int Fibonacci(int n) {
  if (n == 0) {
		return 0;
	}
	if (n == 1 || n == 2) {
		return 1;
	}
  int pre = 1;
  int curr = 1;
  for (int i = 3; i <= n; i++) {
    int sum = pre + curr;
    pre = curr;
    curr = sum;
  }
  return curr;
}
```

## Framework

1. Find all the base cases.

    In Fibonacci problem, base cases are `n == 0` and `n == 1` and `n == 2`;

2. Find all the states.

    In Fibonacci problem, states are all the non-negative numbers.

3. Find the state transition equation.

    In Fibonacci problem, the state transition equation is : dp[i] = dp[i - 1] + dp[i - 2]

::: tip
A state transition equation is a mathematical equation that describes how the state of a system changes over time. In the context of Dynamic Programming, a state transition equation is an equation that describes how the optimal solution to a problem can be constructed from the optimal solutions to its subproblems. By using a state transition equation, it is possible to solve a problem by breaking it down into smaller subproblems and then combining the solutions to those subproblems to find a solution to the larger problem.
:::

4. Find selections and figure out how to define the DP table.
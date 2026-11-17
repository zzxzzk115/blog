---
title: "LeetCode-547: Friend Circles (Medium)"
date: 2020-12-24T13:05:12
categories: [Algorithms]
tags: [LeetCode, DFS, BFS, Union-Find-Sets]
aiTranslated: true
---

# LeetCode-547. Friend Circles

> Difficulty: Medium

## Problem Description

There are **N** students in a class. Some of them are friends, while some are not. Their friendship is transitive: if A is a friend of B, and B is a friend of C, then A is also considered a friend of C. A friend circle is a group of students who are all friends.

Given an **N \* N** matrix **M** representing the friend relationships between students in the class, if M[i][j] = 1, then the i-th and j-th students are known to be friends **with each other**; otherwise it's unknown. You must output the total number of known friend circles among all students.

## Sample Input and Output

Example 1:

```
Input:
[[1,1,0],
 [1,1,0],
 [0,0,1]]
Output: 2 
Explanation: Students 0 and 1 are known to be friends, so they are in one friend circle.
Student 2 is in a friend circle by himself. So return 2.
```

Example 2:

```
Input:
[[1,1,0],
 [1,1,1],
 [0,1,1]]
Output: 1
Explanation: Students 0 and 1 are friends, and students 1 and 2 are friends, so students 0 and 2 are also friends. All three are in one friend circle, so return 1.
```

Constraints:

- `1 <= N <= 200`
- `M[i][i] == 1`
- `M[i][j] == M[j][i]`

## Analysis

First, looking at the input: it's the adjacency matrix of an undirected graph. Finding the number of friend circles is the same as finding the number of connected components in that undirected graph.

Graph traversal can generally be done with Depth First Search or Breadth First Search. Since this problem involves classifying and merging sets, we can also use Union-Find Sets.

## Depth First Search (DFS)

How the DFS works: for i, j (0 to N-1), the current task is to find i's friends. If M\[i\]\[j\] == 1 (meaning i and j are friends) and j hasn't been visited yet, mark j as visited and recurse into the next DFS to find j's friends; otherwise, increment j up to N-1. Keep going until all of i's friends have been marked.

So we can loop i from 0 to N-1, and if i hasn't been marked, recurse with DFS and increment the friend circle count.

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& M) {
        int N = M.size();
        vector<int> visited(N, 0);
        int count = 0;
        for(int i = 0; i < N; ++i) {
            if(visited[i] == 0) {
                dfs(M, visited, i, N);
                ++count;
            }
        }
        return count;
    }

    void dfs(vector<vector<int>>& M, vector<int>& visited, int i, int N) {
        for(int j = 0; j < N; ++j) {
            if(M[i][j] == 1 && visited[j] == 0) {
                visited[j] = 1;
                dfs(M, visited, j, N);
            }
        }
    }
};
```

Time complexity: O(n2)

Space complexity: O(n)

## Breadth First Search (BFS)

BFS follows pretty much the same idea as DFS, except nodes are marked level by level. A queue does the job.

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& M) {
        int N = M.size();
        vector<int> visited(N, 0);
        int count = 0;
        queue<int> q;
        for(int i = 0; i < N; ++i) {
            if (visited[i] == 0) {
                q.push(i);
                while (!q.empty()) {
                    int s = q.front();
                    q.pop();
                    visited[s] = 1;
                    for (int j = 0; j < N; ++j) {
                        if (M[s][j] == 1 && visited[j] == 0)
                            q.push(j);
                    }
                }
                ++count;
            }
        }
        return count;
    }

};
```

Time complexity: O(n2)

Space complexity: O(n)

## Union-Find Sets

Initially there are N friend circles, one per person. Whenever two people are friends, perform a Merge operation; if the Merge succeeds, decrement the number of friend circles by one. The final number of friend circles is the answer.

Union-Find needs two methods: Find and Merge.

Find(x) finds the root of x. Merge(u, v) checks whether u and v can be merged; if so, it merges them and returns True, otherwise it returns False.

Find can be implemented on top of a one-dimensional array parent, optimized with path compression.

```cpp
int find(int x, vector<int>& parent) {
    int r = x;
    while(parent[r] != r) {
        r = parent[r];
    }
    while(parent[x] != x) {
        int t = parent[x];
        parent[x] = r;
        x = t;
    }
    return x;
}
```

Merge is simple; just implement it using Find:

```cpp
bool merge(int u, int v, vector<int>& parent) {
    int ru = find(u);
    int rv = find(v);
    if (ru == rv) {
        return false;
    }
    parent[ru] = rv;
    return true;
}
```

As preparation, the parent array needs to be initialized:

```cpp
void init(vector<int>& parent, int N) {
    parent.resize(N);
    for (int i = 0; i < N; i++) {
        parent[i] = i;
    }
}
```

The final code:

```cpp
class Solution {
private:
    int find(int x) {
        int r = x;
        while(parent[r] != r) {
            r = parent[r];
        }
        while(parent[x] != x) {
            int t = parent[x];
            parent[x] = r;
            x = t;
        }
        return x;
    }

    bool merge(int u, int v) {
        int ru = find(u);
        int rv = find(v);
        if (ru == rv) {
            return false;
        }
        parent[ru] = rv;
        return true;
    }

    void init(int N) {
        parent.resize(N);
        for (int i = 0; i < N; i++) {
            parent[i] = i;
        }
    }
    
    vector<int> parent;
public:

    int findCircleNum(vector<vector<int>>& M) {
        int N = M.size();
        int ans = N;
        init(N);
        for (int i = 0; i < N; ++i) {
            for (int j = i+1; j < N; ++j) {
                if (M[i][j] && merge(i, j)) {
                    ans --;
                }
            }
        }
        return ans;
    }
};
```

The for loop above is optimized: since the adjacency matrix of an undirected graph is symmetric about the diagonal, we only need to consider half of it.

Time complexity: O(n2)

Space complexity: O(n)

## Summary

This problem isn't hard, but it can be solved with several different algorithms, which makes it worth thinking about and a good practice problem.


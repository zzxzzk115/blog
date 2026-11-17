---
title: LeetCode-547:朋友圈（中等）
date: 2020-12-24T13:05:12
categories: [算法]
tags: [LeetCode, DFS, BFS, Union-Find-Sets]
---

# LeetCode-547. 朋友圈

> 难度：中等

## 问题描述

班上有 **N** 名学生。其中有些人是朋友，有些则不是。他们的友谊具有是传递性。如果已知 A 是 B 的朋友，B 是 C 的朋友，那么我们可以认为 A 也是 C 的朋友。所谓的朋友圈，是指所有朋友的集合。

给定一个 **N \* N** 的矩阵 **M**，表示班级中学生之间的朋友关系。如果 M[i][j] = 1，表示已知第 i 个和 j 个学生 **互为** 朋友关系，否则为不知道。你必须输出所有学生中的已知的朋友圈总数。

## 样例输入输出

示例 1:

```
输入：
[[1,1,0],
 [1,1,0],
 [0,0,1]]
输出：2 
解释：已知学生 0 和学生 1 互为朋友，他们在一个朋友圈。
第2个学生自己在一个朋友圈。所以返回 2 。
```

示例 2：

```
输入：
[[1,1,0],
 [1,1,1],
 [0,1,1]]
输出：1
解释：已知学生 0 和学生 1 互为朋友，学生 1 和学生 2 互为朋友，所以学生 0 和学生 2 也是朋友，所以他们三个在一个朋友圈，返回 1 。
```

提示：

- `1 <= N <= 200`
- `M[i][i] == 1`
- `M[i][j] == M[j][i]`

## 分析

首先分析输入数据，是无向图的邻接矩阵表示。找朋友圈个数也就是找该无向图中不同连通块的个数。

对于图的遍历，一般可以利用深度优先搜索(Depth First Search)、广度优先搜索(Breadth First Search) 来解决。对于此问题，由于涉及分类、合并集合，还可以应用并查集(Union-Find Sets)。

## 深度优先搜索 DFS

深搜的过程：对于 i，j (0 到 N-1)，当前任务是找 i 的朋友，如果 M\[i\]\[j\] == 1 (代表 i 和 j 是朋友)，并且 j 没有被访问过，则标记 j 已访问，递归进行下一次深搜，找 j 的朋友；否则， j 自增直到 N-1，如此一直找到 i 所有的朋友都被标记。

所以，可以让 i 从 0 到 N-1 遍历，如果 i 没有被标记过，则继续递归深搜，并且记录朋友圈数加一。

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

时间复杂度：O(n2)

空间复杂度：O(n)

## 广度优先搜索 BFS

广搜和深搜思路差不多，只不过标记的顺序是按层次来的。利用队列就可以解决。

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

时间复杂度：O(n2)

空间复杂度：O(n)

## 并查集 Union-Find Sets

刚开始，有 N 个朋友圈，每个人一个朋友圈。如果两个人是朋友，就进行一次 Merge（合并）操作，如果 Merge 成功，则朋友圈数量减一。最后的朋友圈数量就是需要的结果。

并查集需要实现两个方法，一个是 Find，另一个是 Merge。

Find(x) 用于查找 x 的根父节点。Merge(u, v) 判断 u 和 v 是否可以合并，如果可以，则合并 u 和 v，返回 True，否则返回 False。

Find 方法可以基于一个一维数组 parent 实现，使用路径压缩来优化。

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

Merge 方法很简单，利用 Find 来实现即可：

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

准备工作时，需要对 parent 数组进行初始化：

```cpp
void init(vector<int>& parent, int N) {
    parent.resize(N);
    for (int i = 0; i < N; i++) {
        parent[i] = i;
    }
}
```

最后的代码：

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

上面的 for 循环是优化后的，考虑到无向图的邻接矩阵对角线对称，只用考虑一半即可。

时间复杂度：O(n2)

空间复杂度：O(n)

## 总结

本题不算难，但是可以使用多种算法去解决，值得思考，值得作为练手题。


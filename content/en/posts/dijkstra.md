---
title: 'Algorithms: Shortest Paths with Dijkstra'
date: 2018-03-24T14:43:46
categories: [Algorithms]
tags: [Algorithms, Shortest Path]
original: true
csdn: 79677792
aiTranslated: true
---

> Reposted from my old CSDN blog: [算法——最短路径之 Dijkstra](https://blog.csdn.net/zkx981105/article/details/79677792) (written 2018-03-24); formatting tidied during migration.

For shortest-path problems with non-negative edge weights, Dijkstra's algorithm is a pretty good choice.

<!--more-->

No more talk, here's the template code.

I didn't write any comments, it's easy to follow.

```cpp
#include <cstdio>
#include <iostream>
#include <cstring>
#include <stack>
using namespace std;

const int N = 100;
const int INF = 1e7;

int map[N][N],dist[N],p[N],n,m;
bool flag[N];

void Dijkstra(int u)
{
    for(int i = 1; i <= n; i++)
    {
        dist[i] = map[u][i];
        flag[i] = false;
        if(dist[i] == INF)
        {
            p[i] = -1;
        }
        else
        {
            p[i] = u;
        }
    }

    dist[u] = 0;
    flag[u] = true;

    for(int i = 1; i <= n; i++)
    {
        int temp = INF, t = u;
        for(int j = 1; j <= n; j++)
        {
            if(!flag[j] && dist[j] < temp)
            {
                t = j;
                temp = dist[j];
            }
        }

        if(t == u)
        {
            return;
        }

        flag[t] = true;
        for(int j = 1; j <= n; j++)
        {
            if(!flag[j] && map[t][j] < INF)
            {
                if(dist[j] > dist[t] + map[t][j])
                {
                    dist[j] = dist[t] + map[t][j];
                    p[j] = t;
                }
            }
        }

    }

}

void findPath(int u)
{
    int x;
    stack<int>s;
    cout << "源点为 : " << u << endl;
    for(int i = 1; i <= n; i++)
    {
        x = p[i];
        while(x != -1)
        {
            s.push(x);
            x = p[x];
        }
        cout << "最短路径为 : ";
        while(!s.empty())
        {
            cout << s.top() << "->";
            s.pop();
        }
        cout << i << ", 最短距离为 : " << dist[i] <<endl;
    }
}

int main()
{
    int u,v,w,st;
    cout << "请输入节点个数 通路个数" << endl;
    cin >> n >> m;
    for(int i = 1; i <= n; i++)
    {
        for(int j = 1; j <= n; j++)
        {
            map[i][j] = INF;
        }
    }
    cout << "请输入三个数 u v w 代表从u到v到的路径为w" << endl;
    for(int i = 1; i <= m; i++)
    {
        cin >> u >> v >> w;
        map[u][v] = min(map[u][v], w);
    }
    cout << "请输入初始节点" << endl;
    cin >> st;
    Dijkstra(st);
    // for(int i = 1; i <= n; i++){
    //     cout << st << "->" << i << endl;
    //     if(dist[i] == INF){
    //         cout << "没有路可以走." << endl;
    //     }else{
    //         cout << "最短路径为 : " << dist[i] << endl;
    //     }
    // }
    findPath(st);
    return 0;
}
```

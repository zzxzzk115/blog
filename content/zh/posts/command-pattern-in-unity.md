---
title: '命令模式与其在 Unity 中的应用'
date: 2020-11-02T10:31:00
tags: [Unity, 设计模式]
categories: [游戏开发]
toc: true
---

命令模式（Command Pattern）在游戏开发中是经常用到的设计模式之一，例如游戏的输入键位设置、游戏 AI 命令流、撤销和重做等等都用到了命令模式。本篇文章讲解命令模式的原理及在 Unity 中的应用。

<!--more-->

> 设计模式是优化整个游戏程序框架的核心，本文基于《游戏编程模式》，将书中的原理应用于 Unity 实际项目中。

# 命令模式

> "将一个请求（request）封装成一个对象，从而允许你使用不同的请求、队列或日志将客户端参数化，同时支持请求操作的撤销和恢复。" ——GoF

上面是四人帮对命令模式的解释。我自己对命令模式的理解是：命令模式就是把命令封装成抽象类或者虚基类，进而可以衍生出各种不同的命令，它们对应完成各自不同的逻辑，并且可以根据需要，添加一些字段和方法，让命令可以撤销和重做。

我理解的最简单的命令类的原型：

```csharp
public class Command
{
    protected virtual void Execute() {  }
}
```

## 配置输入

我相信每个考虑周到的游戏的设置菜单中都有键位设置。键位设置，一般就是通过命令模式来完成的。

每个键对应一个 Command 对象，按什么键，就做那个键绑定的该做的事（调用 Command 的 Execute() 方法，即使可能什么事都没做）

以 FC 游戏《魂斗罗》为例，按 A 键发射子弹，按 B 键跳跃。这里用 Unity 实现。

### 定义 Command 基类和 Player 类

```csharp
public class Command
{
    public virtual void Execute(Player player) { }
}
```

Player 类中有 Shoot() 方法和 Jump() 方法，我这里就以 Debug 代替真正的逻辑。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public void Shoot()
    {
        Debug.Log("Shoot");
    }

    public void Jump()
    {
        Debug.Log("Jump");
    }
}
```

### 定义发射子弹命令类、跳跃命令类

发射子弹命令类：

```csharp
public class ShootCommand : Command
{
    public override void Execute(Player player)
    {
        player.Shoot();
    }
}
```

跳跃命令类：

```csharp
public class JumpCommand : Command
{
    public override void Execute(Player player)
    {
        player.Jump();
    }
}
```

### 定义输入处理类

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerInputHandler : MonoBehaviour
{
    private Player player;

    public static Dictionary<KeyCode, Command> keyBindDic = new Dictionary<KeyCode, Command>();

    private void Start()
    {
        player = GetComponent<Player>();
        InitBind();
    }

    private KeyCode currentKey;

    private void HandleInput()
    {
        if (Input.anyKeyDown)
        {
            Event e = Event.current;
            if (e.isKey)
            {
                currentKey = e.keyCode;
                if(currentKey.ToString()!="None")
                {
                    Debug.Log("你按下了" + currentKey + "键");
                }
                if (keyBindDic.ContainsKey(currentKey))
                {
                    keyBindDic[currentKey].Execute(player);
                }
            }
        }
    }

    private void InitBind()
    {
        keyBindDic.Add(KeyCode.A, new ShootCommand());
        keyBindDic.Add(KeyCode.B, new JumpCommand());
    }

    private void OnGUI()
    {
        HandleInput();
    }
}
```

按键与命令的映射通过 Dictionary 来存放，初始化时，绑定 A 为射击，B 为跳跃。

代码写完了，场景中创建空物体，把 Player.cs 和 PlayerInputHandler.cs 均拖拽到同一空物体上，然后运行进行测试：

![A-Shoot,B-Jump](/img/markdown_20201102104226.png)

后续还可以自由更改绑定关系，例如 A 改为跳跃，B 改为射击:

```csharp
keyBindDic[KeyCode.A] = new JumpCommand();
keyBindDic[KeyCode.B] = new ShootCommand();
```

![A-Jump,B-Shoot](/img/markdown_20201102104415.png)

甚至可以不要 A 按键处理任何事情，而是射击改为 C 键：

```csharp
keyBindDic.Remove(KeyCode.A);
keyBindDic.Add(KeyCode.C, new ShootCommand());
```

![B-Jump,C-Shoot](/img/markdown_20201102104518.png)

可以体会到，命令模式是多么有魅力！

## AI 命令流

待续哦
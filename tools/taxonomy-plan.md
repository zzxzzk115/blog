# 分类与标签整理方案

共 77 篇文章。分类 9 → 9，标签 78 → 78。
英文站使用右列的英文名。中英对应关系由三处共同保证，`--apply` 会一起生成：

1. 文章 front matter：名字里有 `#`、`+`、`/`、`*`、`&`、开头是 `.` 的，写成 URL 安全的键（`C#` → `CSharp`，`C++` → `CPP`，`.NET` → `DotNET`，`TCP/IP` → `TCP-IP`，`A*` → `AStar`，`异步 I/O` → `异步IO`）。
2. 这些键的显示名页面 `_index.md`：中英同名的放 `content/shared/`（两种语言共用），只有一种语言用的放 `content/zh/` 或 `content/en/`，其余旧的标签页全部删除，不留空标签页。
3. `data/terms.toml`：中英不同名的成对登记（多线程 = Multithreading），相关文章按它跨语言匹配，标签页的语言切换也靠它找到对应页。

试运行（应用 → 构建 → 恢复）的检查结果：174 个标签/分类页的语言切换全部指向对应语言的同名页，且两边文章一致；66 篇双语文章的相关文章仅 3 篇不同，均因《深入理解 Windows 线程》只有中文版。

## 分类

| 中文 | English | 篇数 |
|---|---|---|
| 编程语言 | Programming Languages | 17 |
| 系统编程 | Systems Programming | 9 |
| 后端与网络 | Backend & Networking | 8 |
| 算法与数据结构 | Algorithms & Data Structures | 9 |
| 游戏开发 | Game Development | 10 |
| 游戏引擎 | Game Engines | 5 |
| 复古掌机 | Retro Handhelds | 8 |
| 机器学习 | Machine Learning | 7 |
| 随笔 | Jottings | 4 |

## 标签

| 中文 | English | 篇数 |
|---|---|---|
| CLR | CLR | 12 |
| C# | C# | 11 |
| 多线程 | Multithreading | 8 |
| 深度学习 | Deep Learning | 7 |
| Win32 | Win32 | 6 |
| C | C | 5 |
| Unity | Unity | 5 |
| .NET | .NET | 4 |
| ClockworkPi | ClockworkPi | 4 |
| GameBoy | GameBoy | 4 |
| PocketChip | PocketChip | 4 |
| Python | Python | 4 |
| 排序 | Sorting | 4 |
| 网络编程 | Network Programming | 4 |
| API | API | 3 |
| C++ | C++ | 3 |
| GAMES104 | GAMES104 | 3 |
| GameShell | GameShell | 3 |
| GBDK | GBDK | 3 |
| Pilot | Pilot | 3 |
| Windows | Windows | 3 |
| 博客 | Blogging | 3 |
| Godot | Godot | 2 |
| TCP/IP | TCP/IP | 2 |
| 图论 | Graph Theory | 2 |
| 改装 | Modding | 2 |
| 造轮子 | Reinventing the Wheel | 2 |
| 逻辑回归 | Logistic Regression | 2 |
| A* | A* | 1 |
| AppDomain | AppDomain | 1 |
| Arduino | Arduino | 1 |
| BadUSB | BadUSB | 1 |
| BFS | BFS | 1 |
| bilibili | bilibili | 1 |
| CIL | CIL | 1 |
| DevTerm | DevTerm | 1 |
| DFS | DFS | 1 |
| DLL | DLL | 1 |
| Git | Git | 1 |
| GitHub | GitHub | 1 |
| Hexo | Hexo | 1 |
| Hugo | Hugo | 1 |
| LeetCode | LeetCode | 1 |
| Love2D | Love2D | 1 |
| Metasploit | Metasploit | 1 |
| MongoDB | MongoDB | 1 |
| Mono | Mono | 1 |
| OpenGL | OpenGL | 1 |
| OpenXR | OpenXR | 1 |
| Raspberry Pi | Raspberry Pi | 1 |
| RetroArch | RetroArch | 1 |
| Shields.io | Shields.io | 1 |
| Socket | Socket | 1 |
| STL | STL | 1 |
| TVCG | TVCG | 1 |
| Unix | Unix | 1 |
| XR | XR | 1 |
| 像素艺术 | Pixel Art | 1 |
| 内存布局 | Memory Layout | 1 |
| 内核对象 | Kernel Objects | 1 |
| 动态规划 | Dynamic Programming | 1 |
| 动画 | Animation | 1 |
| 匿名类型 | Anonymous Types | 1 |
| 学术 | Academia | 1 |
| 安全 | Security | 1 |
| 寻路 | Pathfinding | 1 |
| 并查集 | Union-Find | 1 |
| 异常处理 | Exception Handling | 1 |
| 异步 I/O | Async I/O | 1 |
| 接口 | Interfaces | 1 |
| 操作系统 | OS | 1 |
| 数据库 | Database | 1 |
| 最短路径 | Shortest Path | 1 |
| 汇编 | Assembly | 1 |
| 神经网络 | Neural Networks | 1 |
| 线程池 | Thread Pool | 1 |
| 设计模式 | Design Patterns | 1 |
| 跨平台 | Cross-Platform | 1 |

## 旧标签的去向

改名或并入（内容保留，只是统一了写法）：

| 旧 | 新 |
|---|---|
| AStar | A* |
| CPP | C++ |
| CSharp | C# |
| DotNET | .NET |
| TCP-IP | TCP/IP |

删除（文章类型、或与分类重复）：

异步IO

## 每篇文章（旧 → 新）

| 文章 | 旧分类 | 新分类 | 旧标签 | 新标签 |
|---|---|---|---|---|
| 关于 CLR 的 StructLayoutAttribute 控制类型的字段布局的探究 | 编程语言 | 编程语言 | CLR, CSharp, 内存布局 | CLR, C#, 内存布局 |
| 对<老熟人?>new 关键字的探究(已更新) | 编程语言 | 编程语言 | CSharp, CPP | C#, C++ |
| C 语言字母大小写互换的简单方法 | 编程语言 | 编程语言 | C | C |
| CLR：计算限制的异步操作 | 编程语言 | 编程语言 | CLR, CSharp, 多线程, 线程池 | CLR, C#, 多线程, 线程池 |
| CLR 关键章节 | 编程语言 | 编程语言 | CLR | CLR |
| 《CLR via C#》 Q&A(已更新) | 编程语言 | 编程语言 | CLR | CLR |
| 回顾 CLR(1)：基础部分 | 编程语言 | 编程语言 | CLR, CSharp | CLR, C# |
| 动态链接库 DLL 和.NET Framework 程序集的区别与联系 | 编程语言 | 编程语言 | DotNET, CLR, DLL | .NET, CLR, DLL |
| C# 匿名类型的同一性与相等性 | 编程语言 | 编程语言 | CLR, CSharp, 匿名类型 | CLR, C#, 匿名类型 |
| 对于《CLR via C#》中异常部分的整理 | 编程语言 | 编程语言 | CLR, CSharp, 异常处理 | CLR, C#, 异常处理 |
| 程序如何监视 AppDomain 的卸载 | 编程语言 | 编程语言 | CLR, CSharp, AppDomain | CLR, C#, AppDomain |
| 深入探究 C# 11 的静态抽象接口方法 | 编程语言 | 编程语言 | CSharp, DotNET, 接口 | C#, .NET, 接口 |
| 分享一个.NET 相关博主的博客地址 | 编程语言 | 编程语言 | DotNET | .NET |
| C++ STL 之 不定长数组 vector | 编程语言 | 编程语言 | CPP, STL | C++, STL |
| 《我大意了啊》之 CLR 中值类型调用 Equals 是否装箱的问题 | 编程语言 | 编程语言 | CLR, CSharp | CLR, C# |
| 类型对象的加载时机和类型初始化器的调用时机之间的关系 | 编程语言 | 编程语言 | CLR, CSharp | CLR, C# |
| [教程]VC++6.0 的简单使用 | 编程语言 | 编程语言 | C, CPP | C, C++ |
| [译]Windows 的 Handles 和 Objects | 系统编程 | 系统编程 | Windows, 内核对象 | Windows, 内核对象 |
| 《30 天自制操作系统》Day01 | 系统编程 | 系统编程 | 操作系统, 汇编 | 操作系统, 汇编 |
| Win32 多线程 API 和 C# 多线程 API 的对应关系 | 系统编程 | 系统编程 | Win32, 多线程, CSharp | Win32, 多线程, C# |
| Overlapped I/O：异步、非阻塞式 I/O 技术 | 系统编程 | 系统编程 | Win32, 多线程, 异步IO | Win32, 多线程, 异步 I/O |
| 《Win32 多线程程序设计》FAQ 整理 | 系统编程 | 系统编程 | Win32, 多线程 | Win32, 多线程 |
| 《Win32 多线程程序设计》读书笔记（一） | 系统编程 | 系统编程 | Win32, 多线程 | Win32, 多线程 |
| 《Win32 多线程程序设计》读书笔记（二） | 系统编程 | 系统编程 | Win32, 多线程 | Win32, 多线程 |
| 《Win32 多线程程序设计》读书笔记（三） | 系统编程 | 系统编程 | Win32, 多线程 | Win32, 多线程 |
| 深入理解 Windows 线程 | 系统编程 | 系统编程 | Windows, 多线程 | Windows, 多线程 |
| 关于服务器通过 Python 搭建 API 服务 | 后端与网络 | 后端与网络 | Python, API | Python, API |
| 轮子那点事儿(1)：获取 bilibili 粉丝数的 API 的制作 | 后端与网络 | 后端与网络 | Python, API, 造轮子, bilibili | Python, API, 造轮子, bilibili |
| 轮子那点事儿(2)：获取 GitHub Followers, Stars, Forks 的 API 的制作 | 后端与网络 | 后端与网络 | Python, API, 造轮子, GitHub | Python, API, 造轮子, GitHub |
| 在 MongoDB 中实现自增 ID | 后端与网络 | 后端与网络 | MongoDB, 数据库 | MongoDB, 数据库 |
| 开源项目——寝室助手 | 后端与网络 | 后端与网络 | Raspberry Pi, Arduino, Python | Raspberry Pi, Arduino, Python |
| Metasploit(1):记录一次 Win10 的渗透过程 | 后端与网络 | 后端与网络 | 安全, Metasploit, BadUSB, Windows | 安全, Metasploit, BadUSB, Windows |
| TCP/IP 笔记整理 | 后端与网络 | 后端与网络 | TCP-IP, 网络编程 | TCP/IP, 网络编程 |
| Unix 网络编程：套接字联网 API | 后端与网络 | 后端与网络 | TCP-IP, 网络编程, Socket, Unix | TCP/IP, 网络编程, Socket, Unix |
| 解决 DP 问题的算法框架 | 算法与数据结构 | 算法与数据结构 | 动态规划 | 动态规划 |
| 算法——冒泡排序 | 算法与数据结构 | 算法与数据结构 | 排序 | 排序 |
| 数据结构 - 线性表 | 算法与数据结构 | 算法与数据结构 | C | C |
| 数据结构-栈 | 算法与数据结构 | 算法与数据结构 | C | C |
| 算法——最短路径之 Dijkstra | 算法与数据结构 | 算法与数据结构 | 图论, 最短路径 | 图论, 最短路径 |
| LeetCode-547:朋友圈（中等） | 算法与数据结构 | 算法与数据结构 | LeetCode, 图论, DFS, BFS, 并查集 | LeetCode, 图论, DFS, BFS, 并查集 |
| 算法——归并排序 | 算法与数据结构 | 算法与数据结构 | 排序 | 排序 |
| 算法——快速排序 | 算法与数据结构 | 算法与数据结构 | 排序 | 排序 |
| 三个数的排序常用方法 | 算法与数据结构 | 算法与数据结构 | 排序, C | 排序, C |
| GBDK 简介 | 游戏开发 | 游戏开发 | GameBoy, GBDK | GameBoy, GBDK |
| GBDK 环境搭建 | 游戏开发 | 游戏开发 | GameBoy, GBDK | GameBoy, GBDK |
| 使用 GBDK 绘制简单的精灵 | 游戏开发 | 游戏开发 | GameBoy, GBDK | GameBoy, GBDK |
| GB/GBC 游戏开发：简介 | 游戏开发 | 游戏开发 | GameBoy | GameBoy |
| A* 算法及它在 Unity 中 2D 的 Demo 实现 | 游戏开发 | 游戏开发 | Unity, 寻路, AStar | Unity, 寻路, A* |
| 命令模式与其在 Unity 中的应用 | 游戏开发 | 游戏开发 | Unity, 设计模式 | Unity, 设计模式 |
| 无需头显，使用 Meta XR 仿真器，开发 OpenXR PC 原生应用 | 游戏开发 | 游戏开发 | OpenXR, XR | OpenXR, XR |
| 像素艺术动画学习：001-闪光 | 游戏开发 | 游戏开发 | 像素艺术, 动画 | 像素艺术, 动画 |
| Unity 网游实战(1)：最简单的网络程序 Echo | 游戏开发 | 游戏开发 | Unity, 网络编程 | Unity, 网络编程 |
| Unity 网游实战(2)：状态检测 Poll 和多路复用 Select | 游戏开发 | 游戏开发 | Unity, 网络编程 | Unity, 网络编程 |
| GodotSteam 等自编译版本在 macOS 上反复弹窗确认权限？几行命令就够了 | 游戏引擎 | 游戏引擎 | Godot | Godot |
| Unity 为什么能做到跨平台 | 游戏引擎 | 游戏引擎 | Unity, 跨平台, Mono, CIL, DotNET, CLR | Unity, 跨平台, Mono, CIL, .NET, CLR |
| 从 Pilot 引擎学知识(1)-在 Windows 上跑起来 | 游戏引擎 | 游戏引擎 | Pilot, GAMES104 | Pilot, GAMES104 |
| 从 Pilot 引擎学知识(2)-文件目录结构 | 游戏引擎 | 游戏引擎 | Pilot, GAMES104 | Pilot, GAMES104 |
| 从 Pilot 引擎学知识(3)-CMake 在 Pilot 中的作用(上) | 游戏引擎 | 游戏引擎 | Pilot, GAMES104 | Pilot, GAMES104 |
| GameShell 魔改大屏攻略 | 复古掌机 | 复古掌机 | GameShell, ClockworkPi, 改装 | GameShell, ClockworkPi, 改装 |
| GameShell 怎么玩(01) | 复古掌机 | 复古掌机 | GameShell, ClockworkPi | GameShell, ClockworkPi |
| DevTerm，一款开源复古便携终端设备 | 复古掌机 | 复古掌机 | DevTerm, ClockworkPi | DevTerm, ClockworkPi |
| Pocketchip 安装 Love2D 11.3 折腾分享 | 复古掌机 | 复古掌机 | PocketChip, Love2D | PocketChip, Love2D |
| PocketChip 开启 OpenGL 硬件加速 | 复古掌机 | 复古掌机 | PocketChip, OpenGL | PocketChip, OpenGL |
| PocketChip 安装 RetroArch | 复古掌机 | 复古掌机 | PocketChip, RetroArch | PocketChip, RetroArch |
| PocketChip 魔改加双扬声器 | 复古掌机 | 复古掌机 | PocketChip, 改装 | PocketChip, 改装 |
| 在 GameShell 上运行 Godot 游戏 | 复古掌机 | 复古掌机 | GameShell, ClockworkPi, Godot | GameShell, ClockworkPi, Godot |
| 机器学习笔记(1)——学习体系 | 机器学习 | 机器学习 | 深度学习 | 深度学习 |
| 机器学习笔记(2)——什么是神经网络 | 机器学习 | 机器学习 | 深度学习, 神经网络 | 深度学习, 神经网络 |
| 机器学习笔记(3)——监督学习 | 机器学习 | 机器学习 | 深度学习 | 深度学习 |
| 机器学习笔记(4)——为什么深度学习会兴起 | 机器学习 | 机器学习 | 深度学习 | 深度学习 |
| 机器学习笔记(5)——二分分类 | 机器学习 | 机器学习 | 深度学习 | 深度学习 |
| 机器学习笔记(6)——逻辑回归 | 机器学习 | 机器学习 | 深度学习, 逻辑回归 | 深度学习, 逻辑回归 |
| 机器学习笔记(7)——逻辑回归：代价函数 | 机器学习 | 机器学习 | 深度学习, 逻辑回归 | 深度学习, 逻辑回归 |
| Git 小徽章：Shields.io 与 Substats | 随笔 | 随笔 | Git, Shields.io, 博客 | Git, Shields.io, 博客 |
| hexo 搭建在阿里云服务器上(Ubuntu 20.04) | 随笔 | 随笔 | Hexo, 博客 | Hexo, 博客 |
| 用 Hugo 复活老博客 | 随笔 | 随笔 | Hugo, 博客 | Hugo, 博客 |
| IEEE TVCG 投稿指南 | 随笔 | 随笔 | TVCG, 学术 | TVCG, 学术 |

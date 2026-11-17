# Golang 使用go get命令速度慢的解决方案

身在国内，有苦说不出，经常会碰到各种速度慢的问题。初入Golang的时候，使用`go get -u -v` 一个github的repo的时候，发现根本没有反应，如果是我自己的电脑我可能直接挂科学上网工具了，但是如果是在服务端，shadowsocks懒得去配置，怎么搞呢？

实际上，go提供了代理功能，并且提供了免费的代理地址。采用如下方式即可永久配置代理。

## Linux/Unix

### 1. 启用Go Modules功能

为了一劳永逸，我们编辑`/etc/profile`，而不只是运行一次`export`命令，因为它会在系统启动后执行，每当开机，就自动设置好环境变量了。

```bash
sudo nano /etc/profile
```

往`/etc/profile`文件中添加一句

```bash
export GO111MODULE=on
```

### 2. 配置GOPROXY环境变量

还是继续在`/etc/profle`中添加`export`命令语句

```bash
export GOPROXY=https://goproxy.io
```

最后通过`source`命令来使配置生效：

```bash
source /etc/profile
```

然后go get就根本不卡了。

## Windows

如果是Windows，直接用go提供的代理命令即可：

```shell
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.io
```

## 代理网址收集

目前收集的国内比较好用的golang代理网址：

- https://goproxy.cn
- https://mirrors.aliyun.com/goproxy
- https://goproxy.io
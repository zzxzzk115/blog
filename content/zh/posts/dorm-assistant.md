---
title: '开源项目——寝室助手'
date: 2018-12-16T02:05:13
categories: [后端]
tags: [RaspberryPi, Arduino, Python, tutorial]
toc: true
original: true
csdn: 85023305
---

> 本文转载自我在 CSDN 的旧博客：[开源项目——寝室助手](https://blog.csdn.net/zkx981105/article/details/85023305)（写于 2018-12-16），迁移时整理了格式。

> 身为计算机专业的大学生，我们会自然而然地想办法用自己已有的资源和技术去让生活自动化、智能化。寝室助手这个项目不算创新项目，但是会是一个整理得比较完备的项目。它易于搭建，成本不算高，并且功能可以大大扩展。

<!--more-->

## 1. 寝室助手的功能

寝室助手目前可以实现寝室私有服务器、下载机、私有云盘、Samba 文件共享、DLNA 流媒体、内网开门、远程开门等功能。(语音助手或者监控功能预计以后会添加)

我来简单演示一下它的功能。

我的寝室的服务器主页(80 端口 /var/www/html/index.html) 域名解析为 `pi.code4world.cn`（域名现已失效）(懒得写 html+css+js/php，美观请谅解)

主页的 Aria2 和 Transmission 都是下载工具，可以实现外网访问和内网访问，也就是说可以进行远程下载和在寝室里下载文件到服务器。

云盘则是私有云，由后台管理员添加用户，可以进行文件的上传下载分享，通过安装插件，也可以实现代码的在线编辑、视频的在线播放、文档的在线预览以及压缩文件的在线解压等等。

Jack's Blog 则是我的个人博客（当时的域名 `zhangkexuan.cn` 已失效，如今的博客就是你正在看的这个）。

搭建好的 Aria2 是这样的:

![FadqaT.png](/img/csdn/85023305-1.png)

使用的是 Aria-Ng 的 Web-UI，可以下载文件到指定位置。

搭建好的 Transsmission 是这样的:

![FawSMR.png](/img/csdn/85023305-2.png)

默认开放端口为 9091，可以进行 BT 磁力链接和 BT Torrent(种子) 文件的下载。

搭建好的私有云是这样的:

![FaBUaV.png](/img/csdn/85023305-3.png)

![FaBDxJ.png](/img/csdn/85023305-4.png)

具有云盘的常用功能。

搭建好的 Samba 文件共享如下:

![FaBRIK.png](/img/csdn/85023305-5.png)

可以访问服务器开放的共享文件夹，若服务器开启读写权限，则访问的电脑可以对其进行任意读写操作。

关于 DLNA，我在此不阐述，因为我觉得它比较占用 CPU，我把它关了。hhh。

接下来是内网开门、远程开门:

我放一些照片和视频来进行演示:

门外结构:

![FarWge.jpg](/img/csdn/85023305-6.jpg)

门内结构:

![Farc4K.jpg](/img/csdn/85023305-7.jpg)

门外细节:

![Far29O.jpg](/img/csdn/85023305-8.jpg)

iOS APP 实现内网开门:

{{< video src="/video/dorm/door-app-1.mp4" >}}

{{< video src="/video/dorm/door-app-2.mp4" >}}

校园卡 RFID 开门:

{{< video src="/video/dorm/door-rfid.mp4" >}}

其实还有电脑端可执行程序开门、电脑端 Wox 插件开门和安卓端 APP 开门、web 端开门，这里不演示。

功能到这里就基本介绍完了。

## 2. 寝室助手的准备工作

### 知识储备：

1. Linux 基础
2. 电路基础
3. Python 基础
4. Android 开发(Java Android Studio)
5. iOS 开发(Swift Xcode)
6. 前端基础(HTML CSS JavaScript PHP)
7. 计算机网络基础(TCP Socket)

### 硬件准备：

1. [树莓派 3B](https://item.taobao.com/item.htm?spm=a230r.1.14.29.6f9b264ahLEp0H&id=527576110046&ns=1&abbucket=1#detail) * 1(3B 中国 不含配件 205 元)
2. [闪迪 16G TF 卡](https://detail.tmall.com/item.htm?spm=a230r.1.14.36.2a0d1344oqbldi&id=42229017792&ns=1&abbucket=1) * 1(25 元)
3. [读卡器](https://detail.tmall.com/item.htm?spm=a230r.1.14.36.462e6f49UlRNTp&id=552678446983&ns=1&abbucket=1&skuId=3845350154523) * 1(usb2.0 3.9 元，见第 5 条，若购买 All In One 硬盘盒，则此步跳过)
4. [树莓派配件套餐](https://item.taobao.com/item.htm?spm=a230r.1.14.15.55fa3d21t4sg9f&id=549543685632&ns=1&abbucket=1#detail) * 1(标配 任意颜色 35.8 元)
5. [All In One 硬盘盒](https://item.taobao.com/item.htm?spm=a230r.1.14.1.26245a3awm4nno&id=552755669439&ns=1&abbucket=1#detail) * 1(深蓝色 70 元，或者 [易驱线](https://item.taobao.com/item.htm?spm=a230r.1.14.234.417a7432qlXJi2&id=4228426141&ns=1&abbucket=1#detail) usb 2.0 全套 34 元 + [有源 USB HUB](https://detail.tmall.com/item.htm?spm=a230r.1.14.37.7cb1151f2KCfrb&id=523867459761&ns=1&abbucket=1&skuId=3187171743929) 17 元，共 51 元)
6. [二手 320G 台式 SATA 串口机械硬盘](https://item.taobao.com/item.htm?spm=a230r.1.14.1.571b6118A9gdFC&id=539985662270&ns=1&abbucket=1#detail) * 1(38 元 若有老台式或笔记本的任意硬盘，可以使用，无需购买)
7. Arduino Uno R3 * 1([意大利正版](https://item.taobao.com/item.htm?spm=a230r.1.14.47.4ea56988NOY6Rl&id=559353589432&ns=1&abbucket=1#detail)150 元，[国产版](https://item.taobao.com/item.htm?spm=a230r.1.14.27.4ea56988NOY6Rl&id=578122522913&ns=1&abbucket=1#detail)17 元，推荐正版，国产版不太稳定需要自己装驱动，都送串口线)
8. [UPS 不间断电源](https://item.taobao.com/item.htm?spm=a230r.1.14.20.4c0731e4U0tMeY&id=45032736149&ns=1&abbucket=1#detail) * 1(12V 9V 5V 三输出，带电源 11200mah 80 元，经测试，一整夜都有电)
9. [USB 延长线](https://detail.tmall.com/item.htm?spm=a230r.1.14.1.a76a2f30hYHBY8&id=542679911886&ns=1&abbucket=1&skuId=3895179393222) * 1(玫瑰金 3m 3 元)
10. [DC 延长线](https://detail.tmall.com/item.htm?spm=a230r.1.14.7.15434a98AGxoGb&id=569510599767&ns=1&abbucket=1&skuId=3654226961995) * 1(3m 16.8 元)
11. [杜邦线若干](https://detail.tmall.com/item.htm?spm=a230r.1.14.1.38466a52cXaYS4&id=41406801889&ns=1&abbucket=1&sku_properties=122216547:20213)(大约 5 元)
12. [蜂鸣器](https://item.taobao.com/item.htm?spm=a230r.1.14.36.4a69e385xsk3nU&id=573036291500&ns=1&abbucket=1#detail) * 1(0.39 元包邮)
13. [MG996R 金属舵机](https://item.taobao.com/item.htm?spm=a230r.1.14.1.606e2788nYP7lS&id=562628455699&ns=1&abbucket=1#detail) * 1(360 度，25 元)
14. [RC522 射频模块](https://detail.tmall.com/item.htm?spm=a230r.1.14.1.1cba64adNwsDsW&id=41286608549&ns=1&abbucket=1) * 1 (11 元包邮)
15. [电焊](https://detail.tmall.com/item.htm?spm=a230r.1.14.30.f8ce69c7heRqtJ&id=561103090586&ns=1&abbucket=1&skuId=3677288346527) * 1 (8.6 元包邮)
16. MacBook 任意款或者 Mac * 1(开个玩笑，但如果执意要 iOS 端开门 APP，并且资金充裕，则可以购买)
17. 电脑 * 1(CSer 必备，无需购买)
18. 寝室具备宽带和路由器支撑，架设有 UPS(若没有，则影响断点熄灯后的服务，需要额外 [UPS](https://item.taobao.com/item.htm?spm=a230r.1.14.20.4c0731e4U0tMeY&id=45032736149&ns=1&abbucket=1#detail) 则再+40-115 元，本人觉得 40 元的足矣，光猫和路由器的功耗比较低)

经过计算，最低成本为 400 元左右，不带 UPS，仅在寝室没断电的环境时工作。

如果只实现刷卡开门，不带 UPS，使用闲置充电宝供电，70 元左右即可。

标准成本应该在 500 元左右，带有 UPS，使用硬盘盒。

### 软件准备：

#### 1. 树莓派的初步启动

拿到淘宝来的树莓派，是一件振奋人心的事情。你一定会迫不及待想去使用它。

目前需要准备好的是树莓派、树莓派电源、TF 卡、读卡器和一台电脑，仅仅只需要这些。当然你必须保证你寝室有 WIFI 环境，保证你记得寝室 WIFI 名和密码(开个玩笑但也是实话)。

先将 TF 卡插入读卡器，注意插入的方向必须正确。再将读卡器插入电脑的 USB 口，若电脑能识别，则成功。

去 [树莓派官网](https://www.raspberrypi.org) 下载官方镜像：

https://www.raspberrypi.org/downloads/raspbian/

![FagMeH.png](/img/csdn/85023305-9.png)

为了避免以后下载一些包和一些常用软件，推荐下载第一个镜像

接下来怎么将镜像烧录到树莓派呢

推荐使用 [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/) ，点击 `Download` 下载

运行，按照以下顺序来操作:

![FagWm4.png](/img/csdn/85023305-10.png)

提示，如果是想备份系统镜像，则：

![Fag7p6.png](/img/csdn/85023305-11.png)

当进度达到 100 时，写入系统完成，电脑中有一个叫 boot 的设备。

接下来让树莓派开机前配置好需要连接的 WIFI（有网线并且长度够的，可以直接插网线 hhh)。

由于此时不具备显示器、鼠标键盘，我们如何让树莓派首次开机就连上 WIFI 呢？

进入 boot 设备，新建 `wpa_supplicant.conf ` 文件：

```ini
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="你的WiFi名"
psk="你的WiFi密码" #如果没有密码，此行不要
key_mgmt=WPA-PSK  #如果没有密码或者密码为WEP，则为 key_mgmt=NONE
priority=1
}
```

根据要求更改上面文件的参数，并将注释删掉以免 bug。

**重点：在 boot 上新建一个名为 ssh 的空文件，无后缀，才可默认开启 ssh，此步不要跳过!**

然后推出读卡器设备，拔出 TF 卡，按正确的方向插入树莓派。

树莓派接上电源，打开开关，当有指示灯时，说明已经开机。

到这里初步启动完成

#### 2. 使用 SSH 连接树莓派终端

首先，需要得到树莓派的内网 ip：

最简单的方法当然是进入路由器管理页面:

通常是 `192.168.1.1` 或者 `192.168.0.1`，具体是多少，宽带师傅肯定知道。

浏览器输入并进入路由器管理界面，例如我的管理网页是 `192.168.1.1`，我的路由器是 TP-link 的

![FafABD.png](/img/csdn/85023305-12.png)

匿名主机或者叫 pi 的主机就是我们寻找的对象

这样我的树莓派的 ip 就暂时是 `192.168.1.107`，以下所有 `191.168.1.107` 都应该代替为你自己树莓派的内网 ip。为什么是暂时，因为还没有设置静态 ip，一会儿我们再设置。

MacOS 或 linux 直接打开 `Terminal`，输入 `ssh pi@192.168.1.107`

输入初始密码 `raspberry ` 并回车，即可访问到树莓派的终端。

Windows 可以用 [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/) 连接树莓派的终端：

选择 SSH，

![FafyE4.png](/img/csdn/85023305-13.png)

`Host Name(or IP address)` 栏输入树莓派的内网 ip，端口默认 22。点击 `Open`，进入 ssh 页面：

![Faf4KK.png](/img/csdn/85023305-14.png)

`login as:` 输入 `pi`，因为 `pi` 是默认用户名

接下来输入密码 `raspberry` 并回车，进入树莓派终端：

![Faf7UH.png](/img/csdn/85023305-15.png)

此时 ssh 连接树莓派的工作就绪。

#### 3. 进行必要的设置

##### ①更换国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

用 `#` 注释掉原本的所有内容，并添加以下两行：

```bash
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
```

`Ctrl-O` 保存 `Ctrl-X` 退出，下同，(Windows 中使用 Putty 鼠标右键既是复制也是粘贴)

这样就更换为了清华的镜像源，接下来需要更新源列表:

```bash
sudo apt-get update
```

然后

```bash
sudo nano /etc/apt/sources.list.d/raspi.list
```

用 `#` 注释掉原本的所有内容，并添加以下两行：

```text
deb http://mirror.tuna.tsinghua.edu.cn/raspberrypi/ stretch main ui
deb-src http://mirror.tuna.tsinghua.edu.cn/raspberrypi/ stretch main ui
```

再次更新源列表:

```bash
sudo apt-get update
```

再比较索引清单更新依赖关系：

```bash
sudo apt-get upgrade -y
```

##### ②设置中文

安装中文字体：

```bash
sudo apt-get -y install ttf-wqy-zenhei
```

设置中文字体：

```bash
sudo raspi-config
```

此时进入了树莓派的系统设置界面：

![Fa46pR.png](/img/csdn/85023305-16.png)

上下选择到 `4 Localisation Options` 并回车，选择 `I1 Change Locale`，

去掉 `en_GB.UTF-8 UTF-8`，勾上：`en_US.UTF-8 UTF-8`、`zh_CN.UTF-8 UTF-8`、`zh_CN.GBK GBK`，下一屏幕默认语言选 `zh_CN.UTF-8`。

还有其他相关的设置，后面提到。`Tab` 或左右键移动到 `Finish`，并回车，提示立即重启，重启当即生效。

##### ③修改密码，开启 VNC，修改默认分辨率

![Fa46pR.png](/img/csdn/85023305-16.png)

选择第一项，进行密码的修改。

选择第五项，进入接口设置：

![Fa5BKP.png](/img/csdn/85023305-17.png)

选择 `VNC`，调整为 `Enabled`，提 `VNC` 是 `enabled` 以后，就开启了 `VNC`。

同理，其他接口也可以按需打开。

选择第七项，选择 `A5 Resolution`：

选择你想要的合适的分辨率，我推荐 1920x1080 高清分辨率。

#### 4. 使用 VNC Viewer 连接树莓派

[`VNC Viewer`](https://www.realvnc.com/en/connect/download/viewer/) 可以在官网获得，它有各个版本。

当树莓派开启了 `VNC` 以后，可以通过 `VNC Viewer` 连接它，进行控制，发送消息以及文件。

树莓派 VNC 端口默认为 `5900`，连接的时候不用输入 `5900`，输入 `内网ip` 即可访问。

例如我的树莓派的内网 ip 为 `192.168.1.107`：

![FaIpVO.png](/img/csdn/85023305-18.png)

回车，输入用户名密码，即可进入树莓派图形界面，进行操作。

![FaIaoF.png](/img/csdn/85023305-19.png)

此时用电脑端的 `SSH` 以及 `VNC` 就可以完整控制树莓派了。免去了显示屏、鼠标、键盘的成本。当然有资金的话，配置树莓派就简单多了。

对于手机端，`iOS` 推荐 `树莓派助手(pi helper)`，可以连接树莓派，对树莓派进行监控，也可以进行终端的访问以及 `SFTP` 文件访问、自定义命令，免费。

安卓端下载任意可以 ssh 的终端即可。

`VNC Viewer` 同样有 `iOS` 和 `Android` 端，用手机也可以对树莓派进行图形化控制。

#### 5. 为树莓派设定静态 ip

为什么不用终端设定静态 ip，因为图形化操作简单！

鼠标右键 WiFi 图标：

![FdmTc4.png](/img/csdn/85023305-20.png)

选择 `interface->wlan0`，如果连接网线，则选择 `interface->eth0`

![Fdm7jJ.png](/img/csdn/85023305-21.png)

根据自己树莓派的 ip 填写，如果有 ipv6 也可以填。

`Router` 是网关，也就是路由器的访问地址，我的是 `192.168.1.1`

`DNS` 地址可以在路由器管理网址里查看：

![FdnS3D.png](/img/csdn/85023305-22.png)

填写完以后点击 `应用`，此时我的树莓派的静态 ip 为 `192.168.1.107`。

只有设定了静态 ip，每当树莓派重启的时候，它才不会被动态分配 ip 地址。

#### 6. 安装 Arduino IDE

**忠告：不要通过 `sudo apt-get install arduino` 的方式进行安装，那是很老的版本。**

下载页面在 https://www.arduino.cc/en/Main/Software

由于树莓派是 Linux ARM 架构，所以选择 Linux ARM 版本，通过 wget 命令行下载：

想下载最新版，访问上面的网站，用最新版的链接，用下面类似的方法完成安装（文件夹的名字会不同，解压完后记得 `ls` 一下再 `cd` 进入目录进行安装）

```bash
sudo wget https://www.arduino.cc/download_handler.php?f=/arduino-1.8.8-linuxarm.tar.xz
sudo tar xvJf arduino-1.8.8-linuxarm.tar.xz
cd arduino-1.8.8
./install.sh
```

安装完毕后，将 `Arduino Uno R3` 插入串口线，USB 端插入树莓派的 USB 接口(推荐使用 usb hub 外接电源，usb hub 接树莓派，再将串口线 USB 端插入 usb hub 中，以避免 Uno 供电不足导致的程序错误)

```bash
ls /dev/tty*
```

如果有 `/dev/ttyACM0` 或者类似，则说明串口连接成功。

打开 `Arduino IDE`，选择开发板类型及端口：

![FaoVfJ.png](/img/csdn/85023305-23.png)

![FaoEY4.png](/img/csdn/85023305-24.png)

打开实例程序 `Blink`

![FaoPmV.png](/img/csdn/85023305-25.png)

![Faopyq.png](/img/csdn/85023305-26.png)

点击向右的箭头就是上传代码，上传成功后，Arduino 的 led 开始闪烁，则说明正常工作。

#### 7. SFTP 文件访问

Windows 中使用 `WinSCP`，MacOS 或 Linux 可用 `FileZilla`

只需要知道树莓派内网 ip，用户名和密码即可访问树莓派并进行文件控制，操作简单，在此不多叙述。

#### 8. 域名的购买与解析

本人使用腾讯云，关于域名购买，渠道很多，我只谈解析。

我们只需要了解 CNAME 解析：

例如腾讯云的：我的域名买的 code4world.cn

![FwCE0U.png](/img/csdn/85023305-27.png)

这样解析，就可以将 pi.code4world.cn 解析到 frp.kerwin.cn 从而实现 frp 内网穿透，关于 frp 内网穿透，后面会提到。

## 3. 寝室助手的模块搭建

### 1. Apache2 或者 Nginx 来搭建 Web 服务器

> Apache2 和 Nginx 都可以，两者搭建起来也比较类似。
>
> 两者二选一，不要都安装，因为功能相同，默认都开放 80 端口，都安装的意义不大并且会冲突。

#### ①Apache2 的搭建

安装 Apache2:

```bash
sudo apt-get install apache2
```

此时访问 `http://树莓派内网ip`，应该出现 Apache2 的欢迎界面，提示 `it works`。

这是因为 Apache2 默认监听 `80` 端口，`80` 端口网站位置默认为 `/var/www/html`，默认页面则是 `/var/www/html/index.html`。所以安装完访问树莓派内网 ip 就可以看到效果。

接下来讲述如何自定义添加端口监听，并设定对应网站的位置。

Apache2 的主目录在 `/etc/apache2`，`apache2.conf` 是它的配置文件，但是 `apache2.conf` 也是用过引用模块来配置的，如果要配置 Apache2，流程应该是先在 `ports.conf` 中添加端口监听：

```bash
sudo nano /etc/apache2/ports.conf
```

```apache
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 80

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

可见目前默认监听 `80` 端口，如果想监听其他端口，则在 `Listen 80` 这一行下面加一行 `Listen 端口号` 即可

其实安装完 Apache2，它默认监听 `80` 端口，而 `80` 端口映射的位置在 `/etc/apache2/sites-available/000-default.conf` 中定义了:

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

内容为：

```apache
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

可见，这是 `80` 端口的设置，大致格式应该如下:

```apache
<VirtualHost *:80> #端口号为80
        ServerName www.example.com #服务器域名为www.example.com，没有域名无需设置，用#注释
        ServerAdmin webmaster@localhost #服务器管理员邮箱为webmaster@localhost
        DocumentRoot /var/www/html #服务器位置为/var/www/html
</VirtualHost>
```

`ports.conf` 中添加了端口监听，`000-default.conf` 中添加了网站配置，接下来重启 apache2 服务即可：

```bash
sudo service apache2 restart
```

查看 apache2 的运行状态:

```bash
sudo service apache2 status
```

如果是 `running` 且 `active`，绿色，则运行正常。例如你添加了端口 81，配置好了位置，且该位置下有 `index.html` 之类的入口网页，访问 `http://树莓派内网ip:81` 即可看到结果。

如果想要 apache2 能支持 php，需要以下步骤：

```bash
sudo service apache2 stop
sudo apt-get install php7.0-fpm php7.0-cli php7.0-curl php7.0-gd php7.0-mcrypt php7.0-cgi libapache2-mod-php7.0
sudo service apache2 start
```

例如我配置好了 `70` 端口，配置好了网站根目录为 `/var/www/html/test`，入口为 `/var/www/html/test/index.php`:

```php
<!DOCTYPE html>
<html>
<body>
<?php echo phpinfo(); ?>
</body>
</html>
```

浏览器输入 `192.168.1.107:70` 并回车，将会看到 php 的相关信息界面：

![FdrEaq.png](/img/csdn/85023305-28.png)

此时 apache2+php 搭建完成。

#### ②Nginx 的搭建

安装了 Apache2 就不要再安装 Nginx 了。

安装 Nginx + php：

```bash
sudo apt-get update
sudo apt-get install nginx php7.0-fpm php7.0-cli php7.0-curl php7.0-gd php7.0-mcrypt php7.0-cgi
sudo service nginx start
sudo service php7.0-fpm restart
```

跟 Apache2 类似，Nginx 默认监听 `80` 端口，默认根目录也是 `/var/www/html`，浏览器输入 `http://树莓派内网ip` 并回车，即可看到 nginx 的欢迎界面。

Nginx 的配置目录是 `/etc/nginx`，同 Apache2，Nginx 也有文件夹名为 `sites-available`，意思都是可用网站的配置，不同于 Apache2，我们只用修改 `/etc/nginx/sites-available/default` 文件即可完成配置:

```bash
sudo nano /etc/nginx/sites-available/default
```

配置格式是这样的：

```nginx
server {
        listen 80; #监听端口号80
        listen [::]:80; #监听端口号80

        #server_name www.example.com; #服务器域名

        root /var/www/html; #网站根目录
        index index.php; #网站索引文件

        location / { #增加索引文件类型
                index  index.html index.htm index.php default.html default.htm default.php;
        }

        location ~\.php$ { #支持php
                fastcgi_pass unix:/run/php/php7.0-fpm.sock;
                #fastcgi_pass 127.0.0.1:9000;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
        }
}

```

将默认的替换为以上内容，则可以让 `80` 端口支持 php。如果需要新增端口及网站目录，按照上面的格式添加到 `default` 文件中即可。

修改完后：

```bash
sudo service nginx restart
```

这样就完成了配置。

#### ③设置网站的 logo

网站的 `logo`，即 `favicon.ico`。一般放在网站根目录即可。如何制作 `ico` 图标？

easyicon 的在线转换工具（网站已关闭，原链接已失效）

访问上面的网站，将想要的 `logo` 的 `png` 格式图片转换为 `ico` 格式，重命名为 `favicon.ico`，放在网站根目录中，例如放在 `/var/www/html` 中，怎么放呢？请看上面提到的 `7. SFTP文件访问`。

> 提示：用 sudo chmod -R 777 目录 来使目录有读写权限。下同。

放进去了以后，清空浏览器缓存，刷新网页，即可看到网站带有刚刚放的 `logo`。

#### ④更多

更多知识请去 [W3School](http://www.w3school.com.cn) 学习...

### 2. 搭建花生壳平台，进行外网 ssh 和外网 vnc

进入 [下载界面](https://hsk.oray.com/download/)，下载树莓派版本:

![Fd5Hte.png](/img/csdn/85023305-29.png)

当前的文件为 `phddns_rapi_3.0.2.armhf.deb`

将下载的 deb 包传到树莓派 `/home/pi` 中:

```bash
dpkg -i phddns_rapi_3.0.2.armhf.deb
```

即可安装花生壳。

安装成功后，会自动显示树莓派对应的 SN 码、默认密码 `admin` 和远程管理网址 http://b.oray.com

访问 http://b.oray.com 输入 SN 码和默认密码 `admin` 并回车，进入后台管理：

![Fdo7zd.png](/img/csdn/85023305-30.png)

选择 `内网穿透`，如需 `6` 元，开通即可，我已经配置好的界面是这样的：

![FdTlO1.png](/img/csdn/85023305-31.png)

点击 `添加映射`：

![Fw4PTU.png](/img/csdn/85023305-32.png)

第一个映射，应用名称 `远程ssh`，域名可以选择它免费提供的域名，选择 `非80端口`，不用固定端口号，内网主机填树莓派内网 ip，内网端口填写 `22`，因为 `ssh` 的端口为 `22`

第二个映射，应用名称 `远程vnc`，域名可以选择它免费提供的域名，选择 `非80端口`，不用固定端口号，内网主机填树莓派内网 ip，内网端口填写 `5900`，因为 `vnc` 的端口为 `5900`

映射完后，测试一下：

MacOS 或 Linux 下 `ssh -oPort=外网端口 pi@域名`

Putty 上 `Host Name(or IP Address)` 填写域名，`Port` 填写外网端口，点击 `Open` 进入

如果提示输入用户名或密码，则说明成功。

测试一下 vnc:

输入 `域名:外网端口`，如果输入用户名和密码后能看到图形界面，则配置成功。

为了方便记住外网端口，可在手机端下载花生壳 app。

### 3. 搭建 frp，进行更多的内网穿透

首先下载

```bash
wget https://github.com/fatedier/frp/releases/download/v0.16.0/frp_0.16.0_linux_arm.tar.gz
```

解压

```bash
tar -xzvf frp_0.16.0_linux_arm.tar.gz
```

进入目录

```bash
cd frp_0.16.0_linux_arm
ls
```

发现目录下有可执行程序 `frpc` 和配置文件 `frpc.ini`

接下来配置 `frpc.ini`：

```bash
sudo nano frpc.ini
```

将 `[common]` 一栏替换为以下内容：

```ini
[common]
server_addr = frp.kerwin.cn
privilege_token = kerwin.cn
server_port = 7000
log_file = frpc.log
log_level = info
log_max_days = 7
login_fail_exit = false
```

这里使用了免费的 frp 服务，网址为 `frp.kerwin.cn`（该服务已停止，链接已失效）

使用免费 frp 的原因是我们无需再花钱搭建 VPS。

接下来是配置模板，根据你的需求修改后添加在 `frpc.ini` 中：

```ini
[jack] #配置名为jack
type = http #类型为http
custom_domains = pi.code4world.cn #域名为pi.code4world.cn
local_ip = 192.168.1.107 #树莓派内网ip为192.168.1.107
local_port = 80          #需要内网穿透的端口为80，即默认/var/www/html对应的页面
privilege_mode = true
authentication_timeout = 0
use_encryption = true
use_gzip = true
```

配置完以后，保存文件，如何产生效果?

必须使用 `frpc -c frpc.ini` 才能使用，但是这样没有后台执行，需要 `Ctrl-C` 退出

在命令后使用 `$` 来使该命令后台执行:

```bash
./frpc -c frpc.ini &
```

为了使这个效果在每次树莓派重启开机后都自动后台执行，需要修改 `/etc/rc.local` 文件：

```bash
sudo nano /etc/rc.local
```

在 `return 0` 上面添加一行:

```bash
nohup /home/pi/frp_0.16.0_linux_arm/frpc -c /home/pi/frp_0.16.0_linux_arm/frpc.ini&
```

其中的路径根据你自己的文件路径而改变。

同理，其他开机启动指令一般可以用相同的方法实现。

此时我访问 `http://pi.code4world.cn`（域名现已失效）相当于访问 `http://192.168.1.107:80` 即 `http://192.168.1.107`，但是后者是内网访问，前者无论身处何地，都可以访问。

### 4. 硬盘的挂载

首先进入 VNC 图形界面。

为了保证你的硬盘能稳定读取，连上易驱线后连接外接电源的 usb hub、或者插入外接电源的硬盘盒后接入树莓派，观察能否顺利挂载。

挂载 ntfs 格式需要先

```bash
sudo apt-get install fuse-utils ntfs-3g
modprobe fuse
```

如果挂载成功，ok，可以进行后续操作。

那么，如何让硬盘自动挂载呢？

首先关闭开机后插入介质自动挂载和开机时挂载的选项，因为经过测试，必须如此。

![FwlcLD.png](/img/csdn/85023305-33.png)

点击文件夹，`偏好设置`->`卷管理`，取消勾选第一和第二个选项。

接下来

```bash
sudo nano /etc/fstab
```

加入一个

```text
/dev/sda1 /media/pi/MyDisk ntfs-3g defaults,iocharset=utf-8 0 0
```

`/media/pi/MyDisk` 是挂载的文件夹，由于我的硬盘是 `ntfs` 格式，所以填 `ntfs-3g`，后面的跟我填写一样的就行。具体参见 `fstab` 文件的参数规则。

```bash
sudo reboot
```

重启后，发现自动挂载硬盘到了 `/media/pi/MyDisk`，成功。

为了后续的下载机的下载，创建下载路径

```bash
sudo mkdir /media/pi/MyDisk/Downloads
```

更改读写权限

```bash
sudo chmod -R 777 /media/pi/MyDisk
```

### 5. Aria2 和 Transmission 的搭建，实现下载机

#### ①Aria2 和 Aria-Ng Web-UI

安装 aria2

```bash
sudo apt-get install -y aria2
```

创建文件夹

```bash
mkdir -p ~/.config/aria2/
```

添加配置文件

```bash
sudo nano ~/.config/aria2/aria2.config
```

粘贴以下内容，并修改 `dir` 以及 `rpc-secret `：

```ini
#后台运行
daemon=true
#用户名
#rpc-user=user
#密码
#rpc-passwd=passwd
#设置加密的密钥
rpc-secret=secret
#允许rpc
enable-rpc=true
#允许所有来源, web界面跨域权限需要
rpc-allow-origin-all=true
#是否启用https加密，启用之后要设置公钥,私钥的文件路径
#rpc-secure=true
#启用加密设置公钥
#rpc-certificate=/home/pi/.config/aria2/example.crt
#启用加密设置私钥
#rpc-private-key=/home/pi/.config/aria2/example.key
#允许外部访问，false的话只监听本地端口
rpc-listen-all=true
#RPC端口, 仅当默认端口被占用时修改
#rpc-listen-port=6800
#最大同时下载数(任务数), 路由建议值: 3
max-concurrent-downloads=5
#断点续传
continue=true
#同服务器连接数
max-connection-per-server=5
#最小文件分片大小, 下载线程数上限取决于能分出多少片, 对于小文件重要
min-split-size=10M
#单文件最大线程数, 路由建议值: 5
split=10
#下载速度限制
max-overall-download-limit=0
#单文件速度限制
max-download-limit=0
#上传速度限制
max-overall-upload-limit=0
#单文件速度限制
max-upload-limit=0
#断开速度过慢的连接
#lowest-speed-limit=0
#验证用，需要1.16.1之后的release版本
#referer=*
#文件保存路径, 这里设置为硬盘的下载目录
dir=/media/pi/MyDisk/Downloads
#文件缓存, 使用内置的文件缓存, 如果你不相信Linux内核文件缓存和磁盘内置缓存时使用, 需要1.16及以上版本
#disk-cache=0
#另一种Linux文件缓存方式, 使用前确保您使用的内核支持此选项, 需要1.15及以上版本(?)
#enable-mmap=true
#文件预分配, 能有效降低文件碎片, 提高磁盘性能. 缺点是预分配时间较长
#所需时间 none < falloc ? trunc << prealloc, falloc和trunc需要文件系统和内核支持
file-allocation=prealloc
#不进行证书校验
check-certificate=false
#保存下载会话
save-session=/home/pi/.config/aria2/aria2.session
input-file=/home/pi/.config/aria2/aria2.session
#断电续传
save-session-interval=60
```

保存后

```bash
touch /home/pi/.config/aria2/aria2.session
aria2c --conf-path=/home/pi/.config/aria2/aria2.config
```

这样就将 aria 的配置文件绑定为了 `/home/pi/.config/aria2/aria2.config`

接下来设置 aria2 开机启动：

```bash
sudo nano /lib/systemd/system/aria.service
```

输入以下内容:

```ini
[Unit]
Description=Aria2 Service
After=network.target

[Service]
User=pi
Type=forking
ExecStart=/usr/bin/aria2c --conf-path=/home/pi/.config/aria2/aria2.config

[Install]
WantedBy=multi-user.target
```

重新载入并设置开机启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable aria
```

下载 AriaNg

```bash
wget https://github.com/mayswind/AriaNg/releases/download/0.4.0/aria-ng-0.4.0.zip -O aria-ng.zip
```

解压

```bash
unzip aria-ng.zip -d aria-ng
```

将 aira-ng 放到 `/var/www/html/` 目录下

```bash
sudo mv aria-ng /var/www/html/
```

浏览器访问 `树莓派ip/aria-ng`

`设置`，`全局`，语言选择 `中文`，然后修改 `rpc密钥` 为刚刚你设定的密钥，默认为 `secret`

![Fw98ij.png](/img/csdn/85023305-34.png)

刷新后，即可开始下载任务，内网访问 `http://树莓派内网ip/aira-ng`，外网访问 `http://pi.code4world.cn/aira-ng`（域名现已失效），其中 pi.code4world.cn 是 192.168.1.107:80，具体根据你自己设定的内网穿透来访问。

外网需要设定 rpc 地址，需要再次用到 frp：

在 `frpc.ini` 中添加以下内容：

```ini
[aria2]
type = http
custom_domains = aria.zhangkexuan.cn
local_ip = 192.168.1.107
local_port = 6800
privilege_mode = true
authentication_timeout = 0
use_encryption = true
use_gzip = true
```

其中，aria.zhangkexuan.cn 换为你自己的某个 CNAME 解析到 frp.kerwin.cn 的域名，其他不变。

保存后，更新 frp 服务

`cd` 到 frp 的路径后：

```bash
./frpc -c frpc.ini &
```

在远程访问的 aria2 的 web 界面中，`设置`->`Aria2 RPC 地址` 两栏输入刚刚的域名和 80

再填入密钥并刷新，提示已连接，则成功。

#### ②Transmission

安装 transmission

```bash
sudo apt-get install transmission-daemon
```

修改配置文件

```bash
sudo nano /etc/transmission-daemon/settings.json
```

更改为以下内容

```json
{
    "alt-speed-down": 50,
    "alt-speed-enabled": false,
    "alt-speed-time-begin": 540,
    "alt-speed-time-day": 127,
    "alt-speed-time-enabled": false,
    "alt-speed-time-end": 1020,
    "alt-speed-up": 50,
    "bind-address-ipv4": "0.0.0.0",
    "bind-address-ipv6": "::",
    "blocklist-enabled": false,
    "blocklist-url": "http://www.example.com/blocklist",
    "cache-size-mb": 4,
    "dht-enabled": true,
    "download-dir": "/media/pi/MyDisk/Downloads",
    "download-limit": 100,
    "download-limit-enabled": 0,
    "download-queue-enabled": true,
    "download-queue-size": 5,
    "encryption": 1,
    "idle-seeding-limit": 30,
    "idle-seeding-limit-enabled": false,
    "incomplete-dir": "/media/pi/MyDisk/Downloads",
    "incomplete-dir-enabled": false,
    "lpd-enabled": false,
    "max-peers-global": 200,
    "message-level": 1,
    "peer-congestion-algorithm": "",
    "peer-id-ttl-hours": 6,
    "peer-limit-global": 200,
    "peer-limit-per-torrent": 50,
    "peer-port": 51413,
    "peer-port-random-high": 65535,
    "peer-port-random-low": 49152,
    "peer-port-random-on-start": false,
    "peer-socket-tos": "default",
    "pex-enabled": true,
    "port-forwarding-enabled": false,
    "preallocation": 1,
    "prefetch-enabled": true,
    "queue-stalled-enabled": true,
    "queue-stalled-minutes": 30,
    "ratio-limit": 2,
    "ratio-limit-enabled": false,
    "rename-partial-files": true,
    "rpc-authentication-required": true,
    "rpc-bind-address": "0.0.0.0",
    "rpc-enabled": true,
    "rpc-host-whitelist": "",
    "rpc-host-whitelist-enabled": true,
    "rpc-password": "your_password",
    "rpc-port": 9091,
    "rpc-url": "/transmission/",
    "rpc-username": "your_user_name",
    "rpc-whitelist": "*.*.*.*",
    "rpc-whitelist-enabled": false,
    "scrape-paused-torrents-enabled": true,
    "script-torrent-done-enabled": false,
    "script-torrent-done-filename": "",
    "seed-queue-enabled": false,
    "seed-queue-size": 10,
    "speed-limit-down": 100,
    "speed-limit-down-enabled": false,
    "speed-limit-up": 100,
    "speed-limit-up-enabled": false,
    "start-added-torrents": true,
    "trash-original-torrent-files": false,
    "umask": 18,
    "upload-limit": 100,
    "upload-limit-enabled": 0,
    "upload-slots-per-torrent": 14,
    "utp-enabled": true
}

```

修改 `"rpc-username"` 为你的用户名，修改 `"rpc-password"` 为你的密码

执行以下内容(一定要先 reload，否则配置文件会还原)

```bash
sudo service transmission-daemon reload
sudo service transmission-daemon restart
```

浏览器输入 `树莓派内网ip:9091` 即可访问 transmission，若要外网访问，则还需在 `frpc.ini` 添加以下内容：

```ini
[transmission]
type = http
custom_domains = download.zhangkexuan.cn
local_ip = 192.168.1.107
local_port = 9091
privilege_mode = true
authentication_timeout = 0
use_encryption = true
use_gzip = true
```

同理，download.zhangkexuan.cn 是经过 CNAME 域名解析到 frp.kerwin.cn 的域名。

`cd` 到 frp 的路径后：

```bash
./frpc -c frpc.ini &
```

访问 `http://刚刚的域名` 即可远程访问 transmission，到这里，无论是本地下载，还是远程下载，都可以实现。

### 6. 私有云的搭建

我们使用可道云，配置比较简单。

私有云的物理存储在硬盘，所以先在硬盘上新建文件夹 `kod`

```bash
cd /media/pi/MyDisk
sudo mkdir kod
sudo chmod -R 777 /media/pi/MyDisk/kod
cd kod
sudo wget http://static.kodcloud.com/update/download/kodexplorer4.37.zip
unzip kodexplorer4.37.zip
chmod -Rf 777 ./*
```

可见 `/media/pi/MyDisk/kod` 路径内有 `index.php` 入口文件

联系前面的 Apache2+php 或 Nginx+php，我们监听一个端口，例如 `1998`，配置好网站根目录为 `/media/pi/MyDisk/kod`，域名可以使用一个 CNAME 到 frp.kerwin.cn 的域名，frp 端口设置为 `1998`，刷新 frp 服务，重启 apache 或者 nginx 服务，此时可以通过 `http://树莓派内网ip:1998` 来访问，或者用 `http://刚刚设定的域名` 来访问。

管理员默认用户名 `admin`，初次使用输入密码后即可登录。

普通用户用户名 `default`，默认密码 `default`，游客用户名 `guest`，密码 `guest`。

后台可以设置更多，详情请自行尝试。

### 7. Samba 的搭建

安装 Samba

```bash
sudo apt-get install samba samba-common-bin
sudo apt-get install avahi-daemon
```

配置 Samba

```bash
sudo nano  /etc/samba/smb.conf
```

在文件尾部追加：

```ini
[public]
comment = Public Storage
path = /media/pi
read only = no
writable = yes
create mask = 0777
directory mask = 0777
guest ok = yes
browseable = yes
```

其中，`path` 是公共共享的路径，你也可以设置为 `/media/pi` 来共享硬盘等介质。

配置好后，重启 samba 服务

```bash
smbd restart
```

这时电脑里可能没有打开 samba，

`控制面板`->`程序`->`启用或关闭Windows功能`

![Fw0T4f.png](/img/csdn/85023305-35.png)

勾选 SMB 的两个选项，并启用网络共享发现，则可以在 `网络` 里找到自己的树莓派，可以访问 `public` 文件夹，

为了确保可以读写：

```bash
sudo chmod -R 777 /media/pi
```

其中 `/media/pi` 是刚刚设置的共享路径

此时 Samba 设置完毕。

### 8. miniDLNA 的搭建

更新软件源

```bash
sudo apt-get update
```

安装 minidlna

```bash
sudo apt-get install minidlna
```

设置配置文件

```bash
sudo nano /etc/minidlna.conf
```

在尾部追加内容：

```ini
media_dir=/
```

这么写的意思就是，扫描所有路径的文件

重启 minidlna

```bash
/etc/init.d/minidlna restart
```

此时 miniDLNA 搭建完毕，手机或者电脑只要支持 DLNA，都能直接播放树莓派里的视频，查看图片，收听音乐...

### 9. 寝室开门助手

> 本模块将分成两部分，一部分是单独 Arduino+ 蜂鸣器+舵机+RC522(RFID 射频) 模块的开门实现，另一部分是树莓派通过 Python 的 serial 库和 socket 库实现多端内网 Socket 开门和手机外网开门。

#### ①Arduino+ 蜂鸣器+舵机+RC522 实现校园卡开门

首先看看线路图：

![FBtanI.png](/img/csdn/85023305-36.png)

电路是这么连，具体怎么占地面积小、怎么走线，请自己规划。

##### 对于 `RFID-RC522` 模块：

![FBty9g.png](/img/csdn/85023305-37.png)

其中，`Vcc` 接 Arduino 的 `3.3v`，`RST` 接 Arduino 的引脚 `9`，`GND` 顾名思义 `Ground` 当然接地，即 Arduino 的 `GND` 端，`IRQ` 不接任何引脚，`MISO` 接 Arduino 的引脚 `12`，`MOSI` 接 Arduino 的引脚 `11`，

`SCK` 接 Arduino 的引脚 `13`，`(SDA)SS` 接 Arduino 的引脚 `10`。

![FBNe58.png](/img/csdn/85023305-38.png)

买到的模块需要进行焊接引脚，你需要会使用电烙铁、锡丝、松香等工具。

##### 对于蜂鸣器：

蜂鸣器的正极接直流信号源，`GND` 接 Arduino 的 `GND` 端。

##### 对于金属舵机：

经过测试，舵机的 `vcc` 接 `3.3V` 才能正常工作。

`vcc（红线）` 接 Arduino 的 `3.3v`，`gnd（黑线）` 接 Arduino 的 `GND`，`j2（黄线）` 接 Arduino 的引脚 `6`，因为需要交流信号。

接完了线，就可以进行程序的构思和编写了。

整个程序应该是这样的流程：

1. 获得卡的唯一标识
2. 记录卡的唯一标识并存入数据库（或数组）
3. 程序中若读取到卡的唯一标识与数据库匹配，则让蜂鸣器鸣叫，舵机旋转一定的角度，实现开门。

**补充内容：**

对于 `RFID` 与 `M1` 卡的原理和相关理论，我以后会写下详细内容，这里简单说说。

校园卡一般是 `M1` 类型的 `IC` 卡，对于 `M1` 卡的 `EEPROM` 存储器，它有 `16` 个扇区，每个扇区有 `4` 个块，每个块 `16` 个字节。`16` 个字节编号从 `0` 到 `F`。块编号从 `0` 到 `3`，块 `3` 是扇区的尾块，块 `3` 的 `16` 个字节 `0-5` 对应 `KEY A `，`6-9` 对应 `控制位`，`A-F` 对应 `KEY B`。其他块的字节 `0-F` 都存放数据，例如饭卡余额、水卡余额等...这里不教违法的事儿。多的关于存储控制、密码验证我就不提了。`UID` 就是我们需要读取和记录的数据。

一张卡，对应唯一 `UID`。所以我们刷卡进门，只需判断刷的卡的 `UID` 是否在匹配的列表中存在。

`UID` 即扇区 `0` 块 `0` 的字节 `0-3`，例如某 `M1` 卡的扇区 `0` 的块 `0` 为

> 20 1A 01 A5 9E 88 04 00 00 00 00 00 00 00 00 00

则该卡 `UID` 为 `20 1A 01 A5`。

所以在为 Arduino 写入最终程序之前，你得知道需要录入卡的 `UID` 是多少。

先写入**能够读取 `UID` 的程序**：

首先把 Arduino 的串口线 USB 端插入树莓派，电脑上用 VNC 控制编辑树莓派中安装好的 `Arduino IDE`，或者在电脑上下载 `Arduino IDE`，把 Arduino 的串口线 USB 端插入电脑，效果都一样，我拿树莓派举个栗子。

选择 `项目`->`加载库`->`管理库`：

![FBUhfU.png](/img/csdn/85023305-39.png)

输入 `mfrc`：

![FBUfYT.png](/img/csdn/85023305-40.png)

安装 `MFRC522` 库，我这里已经安装过了。

安装完成后，点击 `文件`->`示例`->`MFRC522`->`ReadNUID`：

![FBUjfO.png](/img/csdn/85023305-41.png)

打开以后，上传，即写入程序，提示上传成功后，

打开串口监视器：`工具`->`串口监视器`：

![FBaCnA.png](/img/csdn/85023305-42.png)

将你待记录的校园卡靠近 `RC522` 模块，串口监视器会显示串口打印的信息，里面包括卡的 `UID`：

![FBamcQ.jpg](/img/csdn/85023305-43.jpg)

我们不记录 `hex(16进制)` 值，我们记录 `dec(10进制)` 值。因为 10 进制是我们最熟悉，并且方便用变量存储、易于转换的值。

最后的示例程序：

```cpp
#include <Servo.h>
#include <MFRC522.h>
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

MFRC522::MIFARE_Key key;

byte nuidPICC[4];
byte keys[4][4]={{*,***,***,***},	//四个人一个寝室，用4*4二维数组存放数据
                 {***,***,***,***},	//我用*屏蔽了我们的uid
                 {**,***,***,***},	//请填入自己记录的10进制值。
                 {***,***,**,**}};

Servo myservo;				//创建舵机对象myservo
int pos = 0;				//舵机初识角度为0
bool isMatch;				//uid是否匹配
int toneVal= 2000;			//蜂鸣器音调值2000

void setup() {				//初始化
    pinMode(4,OUTPUT);		//设定引脚4为输出（蜂鸣器）
    isMatch = false;		//初始化为不匹配
    Serial.begin(9600);		//串口波特率初始化9600
    SPI.begin();			//SPI初始化
    rfid.PCD_Init();		//rfid初始化
    myservo.attach(6);		//舵机信号源绑定为引脚6
    myservo.write(0);		//舵机初始化
    for (byte i = 0; i < 6; i++) {
      key.keyByte[i] = 0xFF;	//初始化key
    }
    Serial.println(F("Serial begun."));
}

void loop() {
    // 读取串口信息，如果接收到字符'o'，则isMatch为true并跳转到标签Label
    if (Serial.available() > 0)
    {
        Serial.println(F("Got a message."));
        if('o' == Serial.read())
        {
            Serial.println(F("The door opened."));
            isMatch = true;
            goto Label;
        }
    }
    // 寻找新卡
    if ( ! rfid.PICC_IsNewCardPresent())
        return;

    // 确认NUID是否已读取
    if ( ! rfid.PICC_ReadCardSerial())
        return;

    MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
    // 检查卡是否为MIFARE类型
    if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
        piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
        piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
        return;
    }
    // 存储NUID到nuidPICC数组
    for (byte i = 0; i < 4; i++) {
        nuidPICC[i] = rfid.uid.uidByte[i];
    }
	// 遍历二维数组，如果数据匹配，则isMatch为true，否则为false
    for(byte i = 0; i < 4; i++){
        if(isMatch) break;
        for(byte j = 0; j < 4; j++){
            if(rfid.uid.uidByte[j] == keys[i][j]) isMatch = true;
            else {isMatch = false;break;}
        }
    }
    // 标签Label
    Label:
    // Halt PICC
    rfid.PICC_HaltA();
    // Stop encryption on PCD
    rfid.PCD_StopCrypto1();
    // 如果匹配
    if(isMatch){
        // 蜂鸣器鸣叫，4是引脚，toneVal上面定义为2000，可根据实际更改。
        tone(4, toneVal);
        // 舵机从初始位置旋转100度，delay的作用是延时去抖。
        for(pos = 0; pos < 100; pos ++){
            myservo.write(pos);
            delay(10);
        }
        // 此时门已开，蜂鸣器停止鸣叫
        noTone(4);
        // 保持门开2.5秒
        delay(2500);
        // 舵机回到初始位置
        for(pos = 100; pos >=0; pos--){
            myservo.write(pos);
            delay(10);
        }
        // 标识符还原
        isMatch = false;
    }
    // 标识符还原
    isMatch = false;
}
```

上传（烧写），成功后刷卡，测试能否控制蜂鸣器的鸣叫，舵机旋转。如果成功，我们进入下一个环节。

#### ②树莓派+python 的 serial 库、socket 库实现多端开门

> 本环节涉及 Python、serial 串口、socket 套接字、Windows 批处理、Java 和 Android Studio、Swift 和 XCode，HTML+JS+PHP，以及 Wox 插件等内容。

##### 如何使用树莓派中的 python 脚本控制 Arduino？

我直接挂代码

代码路径 `/home/pi` 下：

`arduino.py`：

```python
import serial    #import serial module
ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.3);   #open named port at 9600,0.3s timeot

#try and exceptstructure are exception handler

try:
    for i in range(1,4):
        ser.write("o"); #writ a string to port
        response = ser.readall(); #read a string from port
        print (response);
except:
    ser.close();
```

其中，`/dev/ttyACM0` 即 Arduino 的串口设备路径，`9600` 是波特率。

经过测试，发送串口信息有一定的延迟，所以我进行 for 循环，多次发送开门信号 `o`。

在树莓派终端中 `python /home/pi/arduino.py`，即可实现开门。

##### 如何让别的设备也能实现开门？

由于 python 有 `os` 库，其中的 `system` 函数可以执行系统指令，我们用 python 创建一个多线程的 socket 服务端，用于接受客户端的信息，只要接受到特定指令，就执行 `system("python /home/pi/arduino.py&")`，这样就能通过 socket 实现开门。一旦实现 socket，一切能发送 socket 信息的设备都能进行开门。

`Socket Sever` 的代码：

代码路径 `/home/pi` 下:

`server.py`：

```python
#coding=utf-8
import socket
import threading,getopt,sys,string
import os

opts, args = getopt.getopt(sys.argv[1:], "hp:l:",["help","port=","list="])
#设置默认的最大连接数和端口号，在没有使用命令传入参数的时候将使用默认的值
list=10
host='192.168.1.101'
port=6666
def usage():
    print """
    -h --help             print the help
    -l --list             Maximum number of connections
    -p --port             To monitor the port number
    """
for op, value in opts:
    if op in ("-l","--list"):
        list = string.atol(value)
    elif op in ("-p","--port"):
        port = string.atol(value)
    elif op in ("-h"):
        usage()
        sys.exit()

def jonnyS(client, address):
    try:
    #设置超时时间
        client.settimeout(500)
    #接收数据的大小
        buf = client.recv(2048)
    #将接收到的信息原样的返回到客户端中
        client.send(buf)
	if buf == 'open the door':
		os.system('python /home/pi/arduino.py&')
    #超时后显示退出
    except socket.timeout:
        print 'time out'
    #关闭与客户端的连接
    client.close()

def main():
    #创建socket对象。调用socket构造函数
    #AF_INET为ip地址族，SOCK_STREAM为流套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #将socket绑定到指定地址，第一个参数为ip地址，第二个参数为端口号
    sock.bind((host, port))
    #设置最多连接数量
    sock.listen(list)
    while True:
    #服务器套接字通过socket的accept方法等待客户请求一个连接
        client,address = sock.accept()
	thread = threading.Thread(target=jonnyS, args=(client, address))
        thread.start()

if __name__ == '__main__':
    main()
```

其中，`host` 改为你自己树莓派的内网 ip，`port` 改为你想要开放的端口号。这里以 `192.168.1.101` 和 `6666` 示例。终端 `python /home/pi/server.py &` 即可后台开启服务。

但是一旦重启树莓派，该服务就终止了，于是我们编辑 `/etc/rc.local` 文件，在 `return 0` 上面一行添加 `nohup python /home/pi/server.py &` 即可

接下来，只要通过其他端的 socket 客户端，连接上这个服务端，发送一串 `open the door` 的消息，就能开门。

###### Windows 端：

先用 python 写一个 socket 客户端程序：

在任意位置创建文件夹 `开门`，

然后在该文件夹下创建文件 `client.py`：

```python
import socket
import time

HOST = '192.168.1.101'
PORT = 6666
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(b'open the door')
print (sock.recv(1024).decode())
sock.close()
```

我们知道 `.bat` 格式的文件是批处理文件，可以执行系统命令，

在该文件夹下创建 `open.bat`：

```bat
python client.py
```

保存，右键 `open.bat`，发送快捷方式到桌面，然后重命名为 `开门`。以后在桌面点击 `开门` 即可实现开门。

还可以通过 `Wox`+自己写的 python 插件实现，这里原理类似。这是它的 github 的 release 网页：https://github.com/Wox-launcher/Wox/releases

###### 安卓端：

创建空工程，默认主事件 `MainActivity.java`，默认布局 `activity_main.xml`，清单文件 `AndroidManifest.xml`。

①添加权限，在 `AndroidManifest.xml` 文件中添加：

```xml
    <!--允许应用程序改变网络状态-->
    <uses-permission android:name="android.permission.CHANGE_NETWORK_STATE"/>

    <!--允许应用程序改变WIFI连接状态-->
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>

    <!--允许应用程序访问有关的网络信息-->
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <!--允许应用程序访问WIFI网卡的网络信息-->
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>

    <!--允许应用程序完全使用网络-->
    <uses-permission android:name="android.permission.INTERNET"/>
```

②修改布局文件 `activity_main.xml`：

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
xmlns:tools="http://schemas.android.com/tools"
android:layout_width="match_parent"
android:layout_height="match_parent"
android:gravity="center"
tools:context=".MainActivity"
android:weightSum="1">
<Button
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:id="@+id/open_button"
    android:text="开门"
    android:onClick="onClick"
    android:gravity="center"
    android:layout_gravity="center"
    />
</LinearLayout>
```

③在 `MainActivity.java` 中导包、添加代码：

导包：

```java
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
```

添加代码：

```java
public class MainActivity extends AppCompatActivity {
    public Button openButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        openButton = findViewById(R.id.open_button);
    }
    public void onClick(View view){
        new Thread(){
            @Override
            public void run() {
                super.run();
                try {
                    //1.创建监听指定服务器地址以及指定服务器监听的端口号
                    Socket socket = new Socket("192.168.1.101", 6666);//192.168.1.101为我这个本机的IP地址，端口号为6666.
                    //2.拿到客户端的socket对象的输出流发送给服务器数据
                    OutputStream os = socket.getOutputStream();
                    //写入要发送给服务器的数据
                    os.write("open the door".getBytes());
                    os.flush();
                    socket.shutdownOutput();
                    //拿到socket的输入流，这里存储的是服务器返回的数据
                    InputStream is = socket.getInputStream();
                    //解析服务器返回的数据
                    InputStreamReader reader = new InputStreamReader(is);
                    BufferedReader bufReader = new BufferedReader(reader);
                    String s = null;
                    final StringBuffer sb = new StringBuffer();
                    while((s = bufReader.readLine()) != null){
                        sb.append(s);
                    }
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //tv.setText(sb.toString());
                        }
                    });
                    //3、关闭IO资源（注：实际开发中需要放到finally中）
                    bufReader.close();
                    reader.close();
                    is.close();
                    os.close();
                    socket.close();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();
    }
}
```

然后 usb 连接手机，进入开发者模式，允许 usb 调试，安装 apk 到手机中即可。手机连上寝室 wifi，即可用安卓端 app 开门。

###### Mac、Linux 端：

这个就比较简单了，假设你的用户目录是 `/user/bob`，你在该目录下创建一个文件名为 `client.py`，内容依旧是：

```python
import socket
import time

HOST = '192.168.1.101'
PORT = 6666
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(b'open the door')
print (sock.recv(1024).decode())
sock.close()
```

你可以编辑 `~/.bashrc`：

```bash
sudo nano ~/.bashrc
```

添加一行 `alias km='python /user/bob/client.py&'` 后保存，激活：

```bash
source ~/.bashrc
```

以后就可以通过终端命令 `km` 实现开门，配合 `Alfred` 效率更高。

###### iOS 端：

待续。。。2018.12.23 1:12

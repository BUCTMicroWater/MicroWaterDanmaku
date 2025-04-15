# 微水弹幕姬
[[English](README.md)|简体中文]

基于PyQt5构建的实时桌面弹幕服务。 灵感来自由北京大学元火动漫社开发的[弹幕服务](https://github.com/PKUOriginalFire/DanmakuLight)。



## 用法
***请注意：为确保热键功能正常，需要Administrator权限（Windows系统）或 root权限（Linux 和 Mac OS系统）。*** 

我们正尽力通过 GitHub CI 工作流提供预构建版本（Release）。如果您没有看到预构建版本，请参阅下面的 “开发与贡献 ”部分。

**请注意： 由于某些间接依赖项不支持双架构二进制，我们不得不放弃对 Intel Mac 的支持。很抱歉给您带来不便，我们正在寻求解决方法。**

北化微水弹幕姬是北大元火弹幕姬的开箱即用替代品，而且我们设法提供了更多选项。也就是说，弹幕姬会在`3210`端口设立一个WebSocket服务器以接收弹幕信号。与WebSocket服务器建立连接后，就可以向弹幕姬发送如下的弹幕信号：

```json
{
    "text":"Danmaku Content", // 弹幕信号
    "size": 20, // 以像素为单位的弹幕尺寸，默认为20像素
    "color": "#66ccff", // 弹幕颜色，PyQt5支持的任何颜色格式皆可，默认#FFFFFF
    "speed": 300, // 以像素每秒为单位的弹幕移动速度, 默认300像素/秒
    "fontFamily": "Microsoft YaHei", // 弹幕使用的字体, 默认为微软雅黑
    "fontWeight": 400, // 字体的粗细程度，默认为400 (QFont.Normal)
    "fontStyle": 0, // 弹幕的字体样式，默认为0 (QFont.StyleNormal)
    "textDecoration": "" // 弹幕的字体装饰，默认为空
}
```
请注意，可以省略带有默认值的选项，可用选项在将来也有可能更新。

虽然未经测试，但理论上弹幕姬可以同时支持 Windows、Linux 和 MacOS。

要关闭微水弹幕姬，请按快捷键 `Ctrl+Shift+Q` . 

## 优缺点
显然，微水动漫社选择开发自己的弹幕姬是有原因的，即使北大元火动漫社的弹幕姬看起来业已够用，况且微水动漫社并不以开发见长。下表从某种程度上解释了我们为什么要开发属于自己的弹幕姬，以及您应该选择哪个弹幕服务。
| 微水                 | 元火           |
| -------------------- | -------------- |
| 隐藏标题横幅         | 显示标题横幅   |
| 弹幕选项更多         | 弹幕选项更少   |
| 跨平台支持           | 仅Windows      |
| 支持多行弹幕和Emoji  | 仅单行弹幕     |
| 没有GUI控制面板      | 有GUI控制面板  |
| 配置项硬编码于程序中 | 可使用配置文件 |
| 需要较高权限         | 用户权限足矣   |



## 开发与贡献

***请注意： 强烈建议使用虚拟环境。参见 [python venv document](https://docs.python.org/3/library/venv.html).***

和其他Python项目差不多：

```powershell
> Start-Process powershell -Verb RunAs # 启用Administrator权限

> pip install -r requiremets.txt
> python main.py # 在Windows下测试

> pyinstaller main.py # 按照你的意愿添加编译选项
```



```bash
$ pip install -r requirements.txt
$ sudo python main.py # 在Mac OS和Linux下测试

$ pyinstaller main.py # 按照你的意愿添加编译选项
```

当然，这绝对不是一个成熟的项目。我们真诚欢迎Issues和Pull Requests。



## 要实现的功能

1. 从代码中解耦出可能的配置项，并引入配置文件的概念
2. 添加更多种类的弹幕，而不局限于滚动弹幕



## 写在最后

**即使是最微小的水滴，也能折射整个太阳的光芒**。
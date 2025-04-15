# MicroWater Danmaku Sprite
[English|[简体中文](README.zh-CN.md)]

Real-time desktop danmaku service, built with PyQt5. Inspired by [the danmaku service](https://github.com/PKUOriginalFire/DanmakuLight) from the Peking University Original Fire Anime Club.



## Usage
***Attention: To ensure the hot key functions correctly, Administrator (Windows) or root (Linux & Mac OS) is required.*** 

We are trying our best to provide built releases via a GitHub CI workflow. If you didn't see a built release, see Develop & Contribute section below.

BUCT MicroWater Danmaku Sprite is an out-of-the-box alternative to the one from the PKU Original Fire, and we managed to make more options available. Which means, a WebSocket server will be set up at port `3210` to accept danmaku signals. After a WebSocket connection is established with the server, JSON messages like the one below will be accepted: 

```json
{
    "text":"Danmaku Content" // Content of the danmaku
    "size": 20 // Size of the danmaku in pixel, default 20
    "color": "#66ccff" // Color of the danmaku, any format accepted by PyQt is available, default #FFFFFF
    "speed": 300 // Speed of the danmaku in pixel per second, default 300
    "fontFamily": "Microsoft YaHei" // Font used by the danmaku, default Microsoft Yahei
    "fontWeight": 400 // Font weight of the danmaku, default 400 (QFont.Normal)
    "fontStyle": 0 // Font style of the danmaku, default 0 (QFont.StyleNormal)
    "textDecoration": "" // Text Decoration of the danmaku, default empty
}
```
Attention that options with default values can be omitted, and options available may be enriched.

Though not tested, theoretically we support Windows, Linux and MacOS.

To shut off MicroWater Danmaku Sprite, press `Ctrl+Shift+Q` . 

## Pros & Cons
Of course the are reasons why we need to develop our own danmaku service, even if the one from PKU is available and seemly quite enough, and we do not have so much technicians. From the chart below, you may find out why we are developing our own danmaku service, and which one you may use.
| MicroWater                         | Original Fire            |
| ---------------------------------- | ------------------------ |
| Title banner hidden                | Title banner shown       |
| More options available             | Less options available   |
| Multi-platform support             | Windows only             |
| Multi-line danmaku & Emoji support | Single-line text only    |
| No control panel                   | Control panel available  |
| Configs hardcoded                  | Config files available   |
| High privilege required            | User privilege is enough |



## Develop & Contribute

***Attention: A virtual environment is strongly recommended. See [python venv document](https://docs.python.org/3/library/venv.html).***

Just like most Python projects:

```powershell
> Start-Process powershell -Verb RunAs # Enable Administrator privilege

> pip install -r requiremets.txt
> python main.py # Test under Windows

> pyinstaller main.py # Add parameters as you like
```



```bash
$ pip install -r requirements.txt
$ sudo python main.py # Test under Mac OS & Linux

$ pyinstaller main.py # Add parameters as you like
```

Of course, it is definitely not a mature project. We sincerely welcome Issues and Pull Requests.



## TODO

1. Decouple possible configuration items from the code and introduce the concept of configuration files
2. Add more varieties of danmakus, than just scrolling danmakus.



## Additional Notes

**Even the tiniest drop of water can refract the light of the entire sun.**
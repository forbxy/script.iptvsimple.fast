# IPTV Simple Fast Play

一键为 IPTV Simple Client 写入快速播放设置，跳过流类型探测，切台更快。

## 原理

IPTV Simple 在播放每个频道前默认会对流地址发起探测请求（Stat/HEAD）以判断流类型，这会导致切台有延迟。

本插件向 IPTV Simple 的设置文件写入两项全局默认值：

| 设置项 | 值 |
|---|---|
| 输入流名称（defaultInputstream） | `inputstream.ffmpegdirect` |
| MIME 类型（defaultMimeType） | `application/vnd.apple.mpegurl` |

设置后，当频道 m3u8 未通过 `#KODIPROP` 指定输入流时，IPTV Simple 将跳过探测直接用 ffmpegdirect 播放。

## 使用方法

1. 在 Kodi 中运行本插件
2. 弹窗中选择 **写入设置** 写入快速播放配置，或选择 **清除设置** 恢复默认
3. 修改后重启 Kodi 生效

## 注意

- avdvplus编译的CE从R7开始inputstream.ffmpegdirect插件都处于不可用状态，如使用该固件，请在设置-高级-输入流名称中删除inputstream.ffmpegdirect后点确定，否则会导致全部电视都无法播放  
- 如遇个别频道播放异常，可运行插件选择 **清除设置** 恢复
- 若 m3u8 频道已通过 `#KODIPROP:inputstream=...`  `#KODIPROP:mimetype==...`指定输入流，频道的设置优先，本插件写入的客户端设置对其无效

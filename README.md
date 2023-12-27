# NoneBot-Plugin-AntiMonkey

基于cv2和预训练的机器学习模型（TensorFlow）实现检测🐒猴子图并撤回的nonebot插件

## 声明

本项目的开发旨在提供一个技术解决方案，以应对在线群聊中出现的特定类型的刷屏行为。重要的是要强调，此举并非反映出对任何动物，特别是猴子，的不喜欢或成见。作者深知动物在自然界和文化中的重要地位，并且尊重所有生命的多样性和独特性。此项目仅针对那些利用猴子图片进行刷屏、干扰正常交流的行为。作者的目标是促进在线交流的健康和秩序，同时保护用户免受持续的信息干扰和不适内容的影响。

## 介绍

你是否被某些人高频刷的猴子图恶心过？

🐒🐒🐒

本插件能在bot是管理员的群持续检测群聊人员所发图片，判断是否为🐒图并自动撤回，值得注意的是，**撤回功能并不受tx风控影响！**

## 安装

使用pip进行安装

``pip install nonebot-plugin-antimonkey``



## 使用

安装运行后，插件将自动加载并开始监控管理的群消息。

## 存在的问题

不是百分百能识别准确！特别是抽象🐒图！

偶尔会有cv2报错，可能存在于检测表情包这类较小的图片，调整尺寸时发生了错误从而无法读取图片

目前存在极个别群识别不到自己是管理员的情况，正在加紧修复中

管理员的🐒图撤不了

群主的🐒图更撤不了

## 贡献
欢迎提交Pull Request或报告Issues。

## 许可
[MIT License](LICENSE)

## 致谢
感谢google公司开发的MobileNetV2模型，这是一个由Google开发的高效的轻量级深度学习模型。更多关于MobileNetV2的信息可以在[官方论文](https://arxiv.org/abs/1801.04381)中找到

感谢低嫩群友刷的恶心吗喽🐒🐒🐒，让这个项目得以实现。


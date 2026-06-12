---
title: "CAMduct 2020 小孔不出 NC 码的解决方法"
date: 2026-06-12
description: "CAMduct 中小于 5mm 的孔不输出切割代码，原因是 Pierce Size 参数设置"
categories:
  - 暖通风管
tags:
  - CAMduct
  - NC码
  - 踩坑记录
---

## 问题现象

使用 CAMduct 2020 输出 NC 码时，发现**直径 ≤5mm 的小孔不生成切割代码**。大孔正常输出，只有小孔"消失"了。

## 原因分析

经过排查，问题出在 CAMduct 的**穿孔尺寸（Pierce Size）**参数上。

这个参数的含义是：**小于等于该值的孔，不生成穿孔切割代码。** 系统默认值可能为 5.00mm，所以 5mm 及以下的孔就被"吞"掉了。

## 解决方法

1. 打开 CAMduct
2. 进入 **File → Setup → Installed Machines**
3. 选择你的机床
4. 进入 **Tool Setup → Global** 面板
5. 找到 **Pierce Size（穿孔尺寸）** 参数
6. 将其改为 **0** 或 **1mm**
7. 保存

## 相关检查项

如果改了 Pierce Size 还是不行，继续检查：

- **Pierce Delay**：设为 0.1 秒（太长可能跳过小孔）
- **自动嵌套**：检查孔缝合值设置
- **切割工具**：确认机床已添加对应的切割刀具

## 经验总结

> CAMduct 的很多"诡异"行为，根源都在 Machine Setup 里。遇到输出异常，先去翻机床设置，十有八九能找到答案。

这个问题困扰了我两天，最后发现就是一个参数的事。记录下来，希望能帮到遇到同样问题的同行。

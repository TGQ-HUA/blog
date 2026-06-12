---
title: "CAMduct 自动化工具"
description: "解决 CAMduct 2020 中文路径回归 bug，VBS 启动器 + 剪贴板方案"
date: 2025-01-01
image: /img/portfolio/camduct-auto.png
categories:
  - 软件作品
tags:
  - CAMduct
  - VBS
  - AutoIt
weight: 4
---

## 项目概述

CAMduct 2020 存在一个 Autodesk 2014→2020 升级引入的**回归 bug**：无法通过命令行打开中文路径的 .MAJ 文件。本工具通过 VBS 启动器彻底解决此问题。

> 2014 版双击中文 MAJ 正常，2020 版不行——编译工具链升级导致入口点变 ANSI。

---

## 问题根因分析

| 版本 | 行为 | 原因 |
|------|------|------|
| CAMduct 2014 | 双击中文路径 MAJ 正常打开 | 入口点走 Unicode API |
| CAMduct 2020 | 双击中文路径报"错误2-无法开档" | 编译器升级导致命令行参数走 ANSI |

**软件内部 File→Open 走 Unicode API 正常**——所以方案是绕过命令行，改用内部打开。

---

## 解决方案

```
双击 .MAJ 文件
  → 注册表触发 VBS 启动器
  → VBS 复制文件路径到剪贴板
  → 同时启动 CAMduct
  → 用户 Ctrl+O → Ctrl+V → Enter 打开文件
```

配套 Inno Setup 安装包，一键注册文件关联 + 部署 VBS 启动器。

---

## 踩过的坑

- Windows 10 LTSC 的 8.3 短文件名在 D 盘被禁用，`dir /x` 短名为空
- VBS 文件必须 GBK 编码（VBScript 引擎只认 ANSI 代码页）
- .reg 文件含中文必须 UTF-16 LE 带 BOM
- git-bash 下 `reg add` 嵌套引号容易出错，改用 Python winreg

---

## 技术栈

- **启动器**：VBS (GBK 编码)
- **注册表**：HKCR\CAMduct.majfile\shell\open\command
- **安装包**：Inno Setup
- **辅助**：Python + AutoIt（早期方案）

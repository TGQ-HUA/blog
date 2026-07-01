---
title: "CAMduct 自动化配置工具"
date: 2026-07-01
slug: camduct-auto-setup
description: "一键部署 CAMduct 2020 环境：MAJ 中文路径修复、Fabrication 配置文件、7个管件数据库配置，全自动写入注册表。"
categories:
  - 编程工具
tags:
  - CAMduct
  - 自动化
  - 安装包
  - Fabrication
---

## 解决了什么问题

CAMduct 2020 在中文 Windows 上有个旧病：双击含中文路径的 .MAJ 文件会报"错误 2-无法开档"。每次重装系统或换电脑，都要手动：

- 改 MAJ 文件关联
- 覆盖 Fabrication 配置文件到 `%LOCALAPPDATA%\Autodesk`
- 在注册表里一条条加数据库配置（TK1~TK8）
- 配置 NC 码输出参数

这个安装包把这些操作全自动化了。

## 安装包内容

| 功能 | 说明 |
|------|------|
| MAJ 中文路径修复 | 双击 .MAJ → 自动复制路径到剪贴板 + 启动 CAMduct |
| Fabrication 配置 | 覆盖 MAP/INI 配置文件到正确位置 |
| 7个 TK 数据库配置 | TK1~TK8 自动写入 HKCU 注册表 |
| NC 码小孔修复 | Pierce Size 参数说明（≤5mm 孔不切割的解法） |

## 安装步骤

1. 把整个 `CAMduct自动化配置` 文件夹复制到目标电脑
2. 运行 `CAMduct自动化配置_Setup.exe`
3. 选择 CAMduct.exe 位置（自动检测 `D:\CAM 2020`）
4. 选择 TK 配置目录（默认 `D:\CAM\TK2026`）
5. 点击安装 → 完成

## 使用方式

安装后，双击任意 .MAJ 文件：
- 文件路径自动复制到剪贴板
- CAMduct 自动启动
- 在 CAMduct 中按 `Ctrl+O` → `Ctrl+V` → `Enter` 打开文件

## 常见问题

**Q: 为什么不直接自动打开文件？**
CAMduct 2020 是老式 ANSI 程序，命令行参数不支持中文路径。内部 File→Open 走 Unicode 正常，所以用剪贴板 + 手动粘贴的方式绕过。

**Q: 2014 版没问题，2020 版为什么不行？**
Autodesk 在版本迭代中升级了编译工具链，导致命令行参数从 Unicode 退化为 ANSI。这是已知回归 bug，官方未修复。

**Q: NC 码里 ≤5mm 的孔没割出来？**
文件 → 设置 → 已安装机床 → 刀具设置 → Global 面板 → 把「Pierce Size」改成 0 或 1mm。

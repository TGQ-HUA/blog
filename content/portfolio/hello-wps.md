---
title: "HelloWps 加载项"
description: "WPS 表格效率增强工具，一键提取项目/规格/编码处理，配套安装包一键部署"
date: 2025-03-01
image: /img/portfolio/hello-wps.png
categories:
  - 软件作品
tags:
  - WPS JS
  - 加载项
  - Inno Setup
weight: 3
---

## 项目概述

为联泰技术部定制开发的 **WPS 表格加载项**，把日常高频操作封装成一键按钮，让表格操作效率翻倍。

> 版本：v1.1.0 | 离线加载项，不依赖网络

---

## 功能按钮

| 按钮 | 功能 | 使用场景 |
|------|------|---------|
| 教程 | 打开操作手册 | 新员工上手 |
| 提取项目 | 从文件名/单元格自动提取项目名 | 报价单整理 |
| 提取规格 | 正则匹配提取宽×高数值 | 规格汇总 |
| 资料查询 | 快速检索历史数据 | 数据对比 |
| 编码处理 | 编码转换/格式规范化 | 数据清洗 |

---

## 部署方式

```
Inno Setup 安装包 → 双击安装 → WPS 工具栏自动出现按钮
```

- 安装包自带修复脚本（fix_helloWps.py）
- 解决 WPS "已被修改" 弹窗导致加载项失效的问题
- 一键部署到同事电脑，无需技术背景

---

## 技术栈

- **开发语言**：WPS JS 宏（JavaScript）
- **安装打包**：Inno Setup
- **修复工具**：Python（fix_helloWps.py → 编译为 .exe）
- **部署方式**：离线 jsaddons，%APPDATA%\Kingsoft\wps\jsaddons\

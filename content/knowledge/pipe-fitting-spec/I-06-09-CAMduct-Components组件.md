---
title: "I.06.09 CAMduct Components 组件"
date: 2026-06-17
categories:
  - 管件排版规范
tags:
  - 排版软件与流程
weight: 85
---

# I.06.09 CAMduct Components 组件

> CAMduct Components 是与 CAMduct 一起自动安装的**附加软件**。

---

## 定位

它相当于 CAMduct 的**"轻量版"**——拥有管件选型和工单管理能力，但**不负责套料和 NC 码输出**。

---

## 用途

让额外操作员**管理生产线**，提高生产效率和车间灵活性。

### 功能边界

| 有 | 没有 |
|-----|------|
| ✅ 共享 CAMduct 图库和配置库 | ❌ 套料（Nesting） |
| ✅ 管件选型与参数设置 | ❌ 机床接口与 NC 码输出 |
| ✅ 工单创建与管理 | ❌ 轮廓处理器 Profiler |
| ✅ DXF 导出 | |
| ✅ MAJ 工单保存 | |

---

## 典型工作流

### 场景一：对接第三方套料软件

1. 在 Components 中创建工单
2. 导出展开件 DXF
3. 第三方套料软件接收 DXF 进行套料和切割

### 场景二：对接 CAMduct 主站

1. 在 Components 中创建工单
2. 保存为 MAJ 文件
3. 在 CAMduct 中打开 → 套料 → NC 码输出

---

## 相关笔记

- I.06.01 CAMduct简介 → CAMduct 全功能概览
- I.06.04 DXF导出 → DXF 导出详细说明

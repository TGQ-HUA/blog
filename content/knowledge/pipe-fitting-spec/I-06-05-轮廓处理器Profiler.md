---
title: "I.06.05 轮廓处理器 Profiler"
date: 2026-06-17
categories:
  - 管件排版规范
tags:
  - 排版软件与流程
weight: 81
---

# I.06.05 轮廓处理器 Profiler

> Profile 功能（也称 Profiler）是 CAMduct 的**前处理工具**，用于处理导入的 CAD 图形零件和 Opus 绘制的零件。

---

## 概述

### 可处理的文件类型

- DXF 文件或套料排版图的一部分
- 其他软件生成的 NC 码文件
- 旧版 "Profile Master" 工具绘制的零件
- Opus 内绘制的零件

> 💡 Profiler 不仅处理 CAD 图形——当管件录入工单时也会用到它来确定刀具使用。

### Profiler 执行的 9 项任务

1. 分析几何形状
2. 删除重复元素
3. 报告或消除可修复的缺口
4. 报告多重路径
5. 将零件排序为零件岛：内岛（Inner）、中心线（Center Line）、外岛（Outer）
6. 分配默认引入线/引出线（Lead-in / Lead-out）
7. 分配默认刀具
8. 为零件岛和刀具分配颜色
9. 以状态标记保存零件

### 访问方式

- 导入管件时**自动触发**
- Opus 中：`View → Profile`，或工具栏 Profile 图标
- 命令行输入 `PROFILER` 或 `PR`

---

## 启用 Profiler

Profiler 在导入 CAD 管件时自动打开。零件录入工单后可通过菜单或工具栏访问。

> ⚠️ 在 Profiler 中**无法修改图形**——要修改图形需返回 Opus（点击 View → Opus 或工具栏 Opus 图标，或输入 `OPUS`）。

Profiler 菜单栏提供以下命令入口：Auto Repair、Cut Order、Common Line Array、Define Islands、Explode、Simplify、Slice、Stitch Gap、Trim、Tool Use、Write NC。

---

## 自动修复（Auto Repair）

路径：`File → Setup → Profile Database → Profiler Options`

自动修复尝试按指定参数修复零件上的问题。

| 选项 | 说明 |
|------|------|
| **Allow Repair** | 勾选后启用以下修复选项 |
| **Error Tolerance** | 低于此值的错误被忽略 |
| **Deliberate Gap Size** | 低于此值的缺口被忽略 |
| **Maximum Lead Size** | 引入线/引出线的最大尺寸 |

---

## 切割顺序（Cut Order）

路径：`Profiler → Cut Order`

显示切割顺序供确认或编辑。每个切割编号显示为绿色方块。

**重新排序步骤**：

1. 点击所需引入线位置 → 编号 1 被白框包围
2. 依次点击各零件岛（**内岛和中心线岛应在外岛之前处理**）
3. 如出错或只需从某岛重排：右键点击该岛的切割编号 → 白框高亮已排序岛 → 继续点击后续岛
4. 使用多刀具时，建议将同一刀具处理的所有岛放在连续位置

---

## 共线阵列（Common Line Array）

路径：`Profiler → Common Line Array`

从单个零件创建阵列，阵列中各零件**尽可能共享切割边**。

| 参数 | 说明 |
|------|------|
| **Kerf** | 切缝宽度（默认取自机床刀具设置） |
| **Number of Rows** | 水平方向重复数 |
| **Number of Columns** | 垂直方向重复数 |
| **Mirror(m) / Rotate(r) / Copy(c)** | 交替行的处理方式：镜像 = 左右翻转；旋转 = 180° 旋转；如选镜像或旋转，交替行同时上下翻转 |

> 阵列完成后可直接 `Profiler → Write NC` 输出 NC 码，也可保存后正常套料。

---

## 定义零件岛（Defining Islands）

路径：`Profiler → Define Islands`

自定义零件岛——将指定元素组合为一个岛，共享一个引入/引出线。

**操作**：
1. 依次点击要归属同一岛的每个元素
2. 右键完成选择

**适用场景**：切割仅需处理两端的零件（如已部分切割的零件）。

---

## 分解（Explode）

路径：`Profiler → Explode`

当导入的轮廓件包含**多个零件**时，分解功能将它们分离，使各零件可独立套料。

- 点击 Next 可逐一查看分解后的零件。

---

## 简化零件（Simplify Parts）

路径：`Profiler → Simplify`

降低图形复杂度，减少输出 NC 码的指令量。对含 TrueType 文字、椭圆及扫描图形特别有效。

### 基本参数

| 选项 | 说明 |
|------|------|
| **Tolerance（容差）** | High = 更精确；Low = 更多简化 |
| **Shape Retention（形状保留）** | Fine = 更精确；Curvey = 更多简化 |
| **Apply Whole Part / Selected Islands** | 应用到整个零件 / 仅选中岛 |

### 高级参数

| 选项 | 说明 |
|------|------|
| **Inside / Central / Outside Tolerance** | 指定线段合并为单线的阈值 |
| **Restrict Angles** | 只有夹角在此范围内的两条连续线才考虑合并 |

---

## 切片工具（Slice Tool）⭐

> CAMduct 中**超尺寸零件拼板**的核心工具。

路径：`Profiler → Slice`（工具栏 Slice 图标）

### 工具栏/命令

| 模式 | 说明 |
|------|------|
| **Select** | 选择并调整已有切片线，确认后点 Go/Slice 执行 |
| **Polyline** | 类似 Opus 的 Line 命令绘制切片线，可用捕捉模式 |
| **New Vertical Slicer** | 附加**垂直线**到光标，点击固定位置 |
| **New Horizontal Slicer** | 附加**水平线**到光标，点击固定位置 |
| **Auto** | 下拉比例（1:2 ~ 1:12）定义等份切片数 |
| └ Horizontal | 水平方向切分为指定份数 |
| └ Vertical | 垂直方向切分为指定份数 |
| └ Angular | 按角度切分（适合圆形零件） |
| **Cancel** | 清除所有切片线 |
| **Go / Slice** | 执行切片 |
| **Layers** | 导入 Opus 绘制图层中的切片线（需在 Profile Database 中预设图层） |

### 切片对话框

| 选项 | 说明 |
|------|------|
| **Start / End Point / Angle** | 指定起始/结束点绝对坐标 (X,Y)，或起始点+角度（0°=向右） |
| **Split Horizontal / Vertical** | 在绝对位置或百分比处单次分割 |

### 设置选项

| 选项 | 说明 |
|------|------|
| **Use Oversize Seam** | 从超尺寸接缝库中选择拼接接缝 |
| **Export Layer** | 切片线放置的图层 |
| **Default Import Layer** | 图层切片操作的默认图层 |
| **Auto Import Slice Lines** | 启用后自动将默认导入图层上的线显示为切片线 |
| **Slice Line Offset Snap** | 自动偏移切片线指定距离或角度 |

### 典型工作流

1. 选择模式（Polyline / Vertical / Horizontal / Auto）
2. 绘制或放置切片线
3. （可选）用对话框精确设置坐标或分割
4. 点击 **Go/Slice** 执行

---

## 微连接间隙（Stitch Gap）

路径：`Profiler → Stitch`

在切割路径上留下小段未切割金属，使零件保持与板材的连接。

### 三种模式

#### Stitch Island（零件岛微连接）
1. 选择要加微连接的零件岛
2. 命令行输入微连接间隙（Stitch Gap）长度
3. 输入微连接数量
4. **Open Ends 选项**：
   - **Y（是）**：切割从微连接处开始
   - **N（否）**：切割以引入线开始

#### Manual Stitch（手动微连接）
- 输入微连接长度
- 在命令行输入坐标指定位置，或**直接在岛上点击**放置

#### Remove Stitch（删除微连接）
- 输入坐标或点击已有微连接将其删除

---

## 修剪（Trim）

路径：`Profiler → Trim`

修剪**超出切割轮廓的标记线**。常见于导入含多个零件的 DXF 文件后。如果零件没有被外岛完全包围，会提示：`"This part is not enclosed by outer islands."`

---

## 刀具使用（Tool Use）

> Profiler 最重要的配置界面之一——定义每个零件岛的切割方式。

### 零件岛分类

| 类型 | 默认颜色 | 说明 |
|------|----------|------|
| **Outer（外岛）** | 🔵 蓝色 | 最外侧连续岛 |
| **Inner（内岛）** | 🔴 红色 | 外岛内部的连续岛 |
| **Center Cut（中心切割）** | 🟣 紫色 | 未检测为连续的岛（有意或无意） |

可通过 **Cut Side** 下拉菜单手动更改岛类型。更改时引入线位置也会相应调整。

### Tool Use 对话框

| 项目 | 说明 |
|------|------|
| **Tool** | 默认刀具（取自 `Profile Database → Tool Defaults`）。如有其他刀具可在岛级别分配 |
| **Cut Side** | 决定切缝（kerf）施加在切割线的哪一侧 |
| **Kerf** | 割炬厚度补偿：Kerf Left / Kerf Right / Kerf Off |
| **Leads** | 默认引入/引出线值 |
| **Lead Style** | 引入线类型（`Profile Database → Leads` 中用户自定义） |
| **Corner Styles** | 角部样式：Stop-start、Clover Leaf、Triangular |

> 💡 若 Profiler 检测到几何限制，半圆引入线可能自动替换为斜角引入线。如 CAD 程序已施加引入线，检测到的值将自动填入引入线尺寸。

### 操作流程

1. 导入零件后自动进入 Tool Use 模式（前提是零件无需修复）
2. 各岛已自动分类和着色
3. **小黄圈** = 默认引入/引出线位置
4. **左键点击**任意岛元素 → 弹出 Tool Use 对话框确认刀具/切割类型/引入线
5. 可多岛同时选择和修改

---

## 输出 NC 码（Write NC）

路径：`Profiler → Write NC`

可直接从 Profiler 中输出 NC 码，无需经过工单套料流程。

弹出对话框提示输入 NC 码编号或文件名，并选择保存路径。

---


## 📷 配图（截自 Autodesk 官方帮助）

> ![](/img/knowledge/pipe-fitting-spec/GUID-E846D4A3-4B74-49DB-BA9B-28A15F552FF8.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-1E957D48-549D-4410-BAEA-4BD86C34CED5.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-68DE5B11-E693-43FD-8752-C6E1B298AAC1.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-35D435FB-2413-4EDF-AFED-3A89BC6E51FC.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-37CED66A-937A-44E3-888F-C37843AA0AD9.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-39F1163A-3D18-4C79-9758-E9584DB7DD0E.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-25841286-2898-454F-A11B-9D6D96A5A32B.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-BB3DEA9A-649F-4A26-BD97-476673BBEE65.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-74E5FFBB-FC01-4475-AFB9-BC836FE3A061.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-87CC028E-FC3B-495B-BA30-5F1E754C34DD.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-AAC787B9-B600-4677-82E9-A3EC01F936E6.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-AD39A7D5-8F3F-40D1-986C-A9E7F219599E.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-8BC4FCEB-C68E-411B-A553-2813CC421001.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-943DCEC5-C9C8-4B33-87AD-C89E38BF9E28.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-D98FB471-8552-42A8-BD5D-68E26584EBEC.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-E1A67F5A-F17B-48E6-83F7-52E5156A2D4C.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-95FAA385-067A-41FB-9F35-FD9E1BB19EE1.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-B0FBD2E7-C267-4E69-AA5E-B0507BCE9184.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-67343F5B-08AF-42F7-B28F-A2D9D3D7E6F9.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-59B3C8A1-7EF3-4B9D-BA49-12151523177D.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-CAAE9EF4-FCDA-4D4F-B871-17D47949B6AD.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-460128BD-3797-4BD7-9C1A-0A83CDB5A336.webp)

---

## 相关笔记

- I.06.02 Opus绘图系统 → Opus 绘图环境
- I.06.07 套料Nesting → 套料全流程
- I.02 CAMduct基本操作手册 → 实操速查（拼板/接缝）

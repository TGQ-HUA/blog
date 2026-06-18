---
title: "I.06.02 Opus 绘图系统"
date: 2026-06-17
categories:
  - 管件排版规范
tags:
  - 排版软件与流程
weight: 78
---

# I.06.02 Opus 绘图系统

> Opus 是 CAMduct 内置的 CAD 工具，用于创建和编辑管件展开图（平板展开件）。

---

## 2.1 绘图原理

### 基本概念

- **起始角度**：0° 始终在 **3 点钟方向（正东）**（罗盘方位）。
- **坐标系**：首点为绝对坐标 (0,0)；后续点相对于上一个活动点（**相对坐标**）。
- **负号 `-`** 表示从当前工作点**反向**绘制线段。
- **`C` 键**：闭合形状（将当前位置连回起点）。

### 四种绘图方法

| 方法 | 语法 | 关键操作 | 适用场景 |
|------|------|----------|----------|
| **相对坐标**（默认） | `x,y` | 无需额外操作 | 最常用 |
| **绝对坐标** | `@x,y` | `@` 前缀 | 需锁定原点的场景 |
| **正交直接输入**（推荐新手） | `长度` 即可 | `F8` 开启正交模式 | 简单直线绘图 |
| **角度线** | `长度<角度` | `<` 分隔符 | 任意角度线段 |

---

#### 方法一：相对坐标（默认）

> 首点绝对，后续相对上一点。

绘制 500×500 矩形示例：

1. 启动 Line 命令
2. 任意位置点击起点
3. 输入 `500,0` → 水平线（东）
4. 输入 `0,500` → 竖直线（北）
5. 输入 `-500,0` → 水平线（西，反向）
6. 输入 `C` → 闭合

#### 方法二：绝对坐标

> `@` 前缀强制绝对坐标。

绘制 500×500 矩形示例：

1. 启动 Line 命令
2. 输入 `@0,0` → 锚定原点
3. 输入 `@500,0` → 水平线
4. 输入 `@500,500` → 竖直线
5. 输入 `@0,500` → 水平线
6. 输入 `C` → 闭合

#### 方法三：正交直接输入（推荐新手）

> `F8` 开启正交，只输入长度，光标控制方向。

绘制 500×500 矩形示例：

1. 启动 Line，点击起点
2. 按 **F8**（正交 ON），光标向右
3. 输入 `500` → 水平线
4. 光标向上，输入 `500` → 竖直线
5. 光标向左，输入 `500` → 水平线
6. 输入 `C` → 闭合

> 💡 大多数新用户觉得这是最易上手的方法，不熟悉 CAD 环境时无需记忆坐标。

#### 方法四：角度线

> `长度<角度` 语法：`500<45` = 长度 500mm，角度 45°

绘制 500×500 旋转 45° 的正方形示例：

1. 启动 Line，点击起点
2. 输入 `500<45` → 45° 线段
3. 输入 `500<135` → 下一段
4. 输入 `500<225` → 下一段
5. 输入 `C` → 闭合

---

## 2.2 捕捉模式（Snap Modes）

通过捕捉工具栏设置 Opus 中的捕捉点类型。

### 敏感度

- **Sensitivity** 滑块控制光标距离捕捉点多远时自动吸附。右移 → 更易吸附。

### 捕捉模式列表

| 捕捉模式 | 功能说明 |
|----------|----------|
| **正交模式：完全** | 只绘制 0°/90°/180°/270° 线段。`F8` 切换 |
| **部分正交** | 光标吸附到捕捉点后自动应用正交约束 |
| **线段起点/终点** | 吸附到线段或元素的起点与终点 |
| **线段中点** | 吸附到线段或元素的中心点 |
| **圆弧圆心** | 吸附到圆弧或圆的中心点 |
| **捕捉到原始范围** | 吸附到倒角/圆角前的原始角点，或编辑前的原始中心点 |
| **圆弧象限点** | 吸附到圆弧的四个罗盘方向点（0°/90°/180°/270°） |
| **交点** | 吸附到两个元素交叉点 |
| **参考点** | 吸附到用户自定义的参考点 |
| **吸附到最近点** | 吸附到元素上距离光标最近的点（不常用） |
| **网格点** | 点击图标开关网格点显示 |
| **切点** | 吸附到圆/圆弧的切点 |
| **对象捕捉追踪** | 沿捕捉点对齐路径追踪，最多同时追踪 7 个点。已获取点显示为黄色方块 |

---

## 2.3 常用绘图命令

### 键盘快捷方式

| 按键 | 功能 |
|------|------|
| **F2** | 以光标为中心 |
| **F3** | 放大 |
| **F4** | 缩小 |
| **F5** | 缩放至全部范围 |
| **F6** | 缩放至选中对象 |
| **F8** | 切换正交模式（或命令行输入 `Ortho`） |
| **Length** | 给出所有选中元素的真实组合长度 |
| **C** | 闭合多段线 |
| **Ctrl+A** | 全选 |
| **Esc** | 取消全部选择 |

### 鼠标操作

- 滚轮缩放 + 组合键可实现更多功能。

### 菜单栏

绘图模式下菜单栏提供：**Edit / New / Insert / Modify / Tools / View**。

---

## 2.4 命令快捷方式

> 输入命令时注意 CAMduct 窗口左下角状态消息区——它会提示下一步操作要求。

| 命令 | 缩略 | 中文说明 |
|------|------|----------|
| `LINE` | `L` | 线段 |
| `ARC` | `A` | 圆弧 |
| `ARCCSE` | `ACSE` | 圆弧-圆心/起点/终点 |
| `ARCSCE` | `ASCE` | 圆弧-起点/圆心/终点 |
| `ARCSEC` | `ASEC` | 圆弧-起点/终点/圆心 |
| `ARCSEM` | `ASEM` | 圆弧-起点/终点/中间点 |
| `CIRCLE` | `C` | 圆 |
| `ELLIPSE` | `EL` | 椭圆 |
| `RECTANG` | `REC` | 矩形 |
| `POLYLINE` | `PL` | 多段线 |
| `MOVE` | `M` | 移动 |
| `COPY` | `CO` | 复制 |
| `ROTATE` | `RO` | 旋转 |
| `MIRROR` | `MI` | 镜像 |
| `SCALE` | `SC` | 缩放 |
| `STRETCH` | `S` | 拉伸 |
| `OFFSET` | `O` | 偏移 |
| `TRIM` | `TR` | 修剪 |
| `EXTEND` | `EX` | 延伸 |
| `BREAK` | `BR` | 打断 |
| `CHAMFER` | `CHA` | 倒角 |
| `FILLET` | `F` | 圆角 |
| `ERASE` / `DELETE` | `E` / `DEL` | 删除 |
| `ARRAY` | `AR` | 矩形阵列 |
| `ARRAYPOLAR` | `ARP` | 极轴阵列 |
| `UNDO` | `U` | 撤销 |
| `REGEN` | `RG` | 重新生成图形 |
| `REPAIR` | `REP` | 修复 |
| `GROW` | `GW` | 增长 |
| `SLICE` | `SL` | 轮廓切片 |
| `SLIT` | — | 开缝 |
| `SLOTHOLE` | `SH` | 长圆孔 |
| `PIERCE` | `PI` | 穿孔点 |
| `CIRCCUT` | `CC` | 圆形切除 |
| `RECTCUT` | `RC` | 矩形切除 |
| `RECTNOTCH` | `RN` | 矩形切口 |
| `VEENOTCH` | `VN` | V 形切口 |
| `SVEENOTCH` | `SVN` | 斜 V 形切口 |
| `TAGNOTCH` | `TN` | 标记切口 |
| `JUNCNOTCH` | `JN` | 连接切口 |
| `MARKINGTEXT` | `MT` | 标记/打印文字 |
| `TRUETYPE` | `TT` | TrueType 文字 |
| `MODIFYTEXT` | `MT` | 修改文字 |
| `PARTNOTES` | `PN` | 零件注释 |
| `MARKER` | `MK` | 参考点标记 |
| `REFPOINT` | `RP` | 创建参考点 |
| `DELREFPTS` | `DRP` | 删除全部参考点 |
| `DISTANCE` | `D` | 距离测量 |
| `LENGTH` | `LN` | 长度 |
| `DIMALIGNED` | `DAL` | 对齐标注 |
| `DIMANGULAR` | `DAN` | 角度标注 |
| `DIMDIAMETER` | `DIA` | 直径标注 |
| `DIMLINEAR` | `DLN` | 线性标注 |
| `DIMORDINATE` | `DOR` | 坐标标注 |
| `DIMRADIAL` | `DRD` | 半径标注 |
| `DIMLABEL` | `DLB` | 标签标注 |
| `IMPORTITEM` | `II` | 导入管件 |
| `IMPORTVECTOR` | `IV` | 导入图像转矢量 |
| `ITEMPASTE` | `IPST` | 粘贴为新管件 |
| `PARTPASTE` | `PP` | 粘贴为新零件 |
| `PASTECLIP` | `PC` | 从剪贴板粘贴 |
| `COPYCLIP` | `COC` | 复制到剪贴板 |
| `CUTCLIP` | `CU` | 剪切到剪贴板 |
| `SELECTALL` | `SELA` | 全选 |
| `SELECTINV` | `SELI` | 反选 |
| `SELECTNONE` | `SELN` | 取消选择 |
| `ZOOMTOFIT` | `ZF` | 缩放至适合窗口 |
| `ZOOMTOSELECT` | `ZS` | 缩放至选中项 |
| `ZOOMTOWINDOW` | `ZW` | 窗口缩放 |
| `PAN` | `P` | 平移视图 |
| `GRID` | `G` | 网格间距 |
| `GRIDDISPLAY` | `GD` | 网格显示组件 |
| `GRIPS` | `GR` | 切换拖拽夹点 |
| `DXFEXPORT` | — | DXF 导出 |
| `PROFILER` | `PR` | 轮廓处理器 |
| `SETTINGS` | — | 3D 查看器设置 |
| `HELP` | `?` | 显示命令列表 |

---

## 2.5 Opus 打印

在 Opus 中打印当前视图窗口中的零件图形（不同于 CAD 绘图输出）。

### 访问方式

- 工具栏 Opus 图标
- 菜单 `View → General Settings`（视图 → 常规设置）

### 打印选项

- **Show Cut Layers Only**：仅显示切割层
- **Dimensions and Annotation**：显示尺寸标注

打印前有打印预览可确认。

---


## 📷 配图（截自 Autodesk 官方帮助）

> ![](/img/knowledge/pipe-fitting-spec/GUID-C1869ECA-6D30-4F84-8908-DD742208FE70.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-E02CE682-A822-4E64-A281-5B5C7149FEE2.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-6F9075E1-BF09-4F3D-B24A-FD5EBE8FE0E9.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-22E4B4F8-4D1E-450B-9C25-6D4C112E3BEA.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-F5D45F28-CBF3-4B3A-AFC4-93518DF454F2.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-ACB2C043-E35A-4FE7-A711-24AF7B4BA1B7.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-616B3B74-331E-4D0D-9293-7F9C7C7DF9A9.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-1E192169-CB1D-420A-BB01-9DF81314F652.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-72CF346C-0634-40A4-879E-5FBC33F54ECC.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-F403CBC1-171E-4BB3-814C-A62FE610A6FD.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-ACCBCEEA-FB89-47EB-8F11-57A7EE2041B9.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-445DEF15-F83A-4DCA-BEAC-2DBFB923D407.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-F7EC0559-F195-4F2E-90CC-6CA52D2AEC9F.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-B502559D-3786-462B-8829-A649AA712E4D.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-B474BFF2-65C9-4BB8-9E3D-FF3B55E1AB93.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-54F48E1B-A1BB-450C-9442-ED2F8AF0EDF7.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-9CC7E263-5443-445B-ABAD-485293623AD6.webp)

---

## 相关笔记

- I.06.03 系统设置 → 常规选项与网格选项
- I.06.05 轮廓处理器Profiler → Profiler 更多操作
- I.02 CAMduct基本操作手册 → 实操速查

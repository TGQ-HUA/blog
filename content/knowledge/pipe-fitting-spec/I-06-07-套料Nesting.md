---
title: "I.06.07 套料 Nesting"
date: 2026-06-17
categories:
  - 管件排版规范
tags:
  - 排版软件与流程
weight: 83
---

# I.06.07 套料 Nesting

> 在 CAMduct 中，"套料"指将管件展开图在板材上高效排列，以达到最大利用率和最小废料。
> 支持两种方式：**自动套料**（桌面或云端）和**手动套料**。

---

## 7.1 套料基本配置

路径：`Database → Manufacturing → Nesting`

### 间距参数

| 参数 | 说明 |
|------|------|
| **Default margin between nested parts**（零件间默认间距） | 所有零件间的最小距离。设 10mm → 至少 10mm。此值也适用于零件到板边的距离。**间距不累加** |
| **Additional Sheet Edge Margin**（板边额外边距） | 板材四周附加边距，**与最小间距累加**。例：最小 10 + 额外 5 = 板边 15，零件间 10 |
| **Ignore Lead-ins less than**（忽略小于某值引入线） | 允许引入线侵入最小间距。应设得比最小间距小。引入线大于此值则整零件移开 |

### 新增板材策略（New Sheet）

| 策略 | 说明 |
|------|------|
| **Use default sheet size** | 使用材质库中打绿勾的默认尺寸 |
| **Allow Alternate Sizes to Avoid Oversizing** | 允许替代尺寸以避免零件超板 |
| **Use Stock Sheets from Sheet Management** | 使用板材管理的库存板材。`Use Remnants with <= %` 控制（设 100% 则全部可用） |
| **Prompt for new sheet sizes** | 每次需新板弹窗选择 |
| **Load Remnant** | 选择已保存的余料（仅配合板材管理） |

### 自动重排套料

**Re-order Nest Automatically**：仅一台机床（或同类机床）时，每次写 NC 码自动重排。省去手动点"选择机床"。

---

## 7.2 自动套料（Automatic Nesting）

对话框含多个选项卡：

### General（常规）

同 #7.1 套料基本配置。

### Preferences（偏好）

适用于多机床用户。

| 选项 | 说明 |
|------|------|
| **Nest for Machine** | 指定目标机床。`None` = 默认机床 |
| **Across Width of Sheet** | 先填满板宽（推荐——零件更快取走） |
| **Across Length of Sheet** | 先填满板长 |
| **Smallest Bounding Rectangle** | 最小外接矩形，与板上位置无关 |
| **User Item Nest Priorities** | 按工单组织菜单中设置优先级 |
| **Multi-Torch** | 割炬头数量（用于同时切多个相同零件） |

### Method（方法）

| 套料方法 | 说明 | 余料支持 | 间隙填充 |
|----------|------|----------|----------|
| **Batching** | 按分段名/页码分批。选项：None / Item Section Name / Item Page Number | — | — |
| **True-Shape Nesting**（默认）⭐ | 最常用。条带算法，非常精确。唯一使用 Preferences 设置的方法。需间距>0 | ✅ | ✅ |
| **Row Nesting** | 单一对称零件好，非对称无效 | ❌ | ❌ |
| **Rectangular Nesting** | 每零件外接矩形。**最适合矩形展开件**（多段组合弯头）。允许零间距和负切缝 | ❌ | ❌ |
| **Edge Nesting** | 从四角向中心排。**适合保留最大余料** | ❌ | ❌ |

| 附加选项 | 说明 |
|----------|------|
| **Try to fill gaps after main nesting** | 主套料后填充间隙 |
| **Create Sheared Nests for Sheared Parts** | 为标记为剪切的零件激活剪切套料 |
| **Nest Insulation Developments** | 套料保温展开件 |
| **Flanged Parts** | 专门针对翻边零件 |

### Auto Stitching（自动微连接）

| 选项 | 说明 |
|------|------|
| **Automatically Stitch Nested Islands** | 启用后显示以下设置 |
| └ Outer Islands – If Long Side < | 外岛长边小于此值 → 加微连接。`Any` = 不论尺寸 |
| └ Outer Islands – If Short Side < | 外岛短边 < 值 → 加微连接 |
| └ Inner Islands – If Long Side < | 内岛同上 |
| └ Inner Islands – If Short Side < | 内岛同上 |
| **Default Auto Stitching Values** | 指定微连接长度和数量 |

### Sheet Order（板材排序）

决定工单内容中板材显示顺序，影响 NC 码编号。可按以下字段排序：**材质 → 板厚 → 真实利用率 → 保温标记**。

---

## 7.3 手动套料（Manual Nesting）

遇到新材质/板厚组合时弹出手动套料对话框。四区域：

### 零件区（Parts）

- 每个零件显示：**零件编号**（左上）、**毛坯尺寸**（外接矩形，下方）、**待套料数量**（蓝色数字，右下）
- 套料后：数量减少，**蓝色叉号** = 该零件已无待排件
- `View → Only Show Remaining Parts`：直接移出已排完零件
- 右键 → 剪切/复制/粘贴

### 板材控制中心（Sheet Control Centre）

| 控件 | 说明 |
|------|------|
| Material & Gauge 下拉 | 选择材质/板厚 |
| Sheets 下拉 | 列出全部板材，显示尺寸和利用率 |
| New | 新建默认尺寸板材 |
| Properties | 修改尺寸和多头割炬配置（仅空板） |
| Delete | 清除板上零件（板保留） |
| Trash | 彻底删除板材 |

### 菜单操作

#### 切割顺序

| 模式 | 操作 |
|------|------|
| **Simple Cut Order** | 按零件级别改顺序。点绿色方块依次单击。重新分配：右键当前号（变黄）→ 左键新位 |
| **Advanced Cut Order** | 按单次切割级别。每刀独立编号 |

#### 链式切割（Chain Cut）

多个零件在一次割炬点火中连续切割，**减少穿孔点**。

- 从一个岛拖到另一个建立链
- 先切约一半 → 跳下一个 → 路径完成后返回完成
- 右键链起始/结束小方块可修改

#### 桥接切割（Bridge Cut）

也是连续切割，但**完整切完一个零件**再切下一个。

- 仅两个零件可桥接，超过两个用链式切割
- 主要用于终止链的末端让切割掉头

#### 引入线调整（Leadins）

- 悬停 → 灰圈显示当前位置
- 蓝箭头 = 切割方向，黑箭头 = 备选路径。单击切换
- 右键 → 查看/更改引入线类型（弧形/直线等）

#### 微连接（Stitching）

- **自动**：拖框选零件 → 右键设置
- **手动**：在零件上点击拖拽
- 黑色虚线 = 已加微连接
- 设置长度：`Operation → Tool Options`

---

## 7.4 套料分析（Analyzing Nests）

`View` 菜单下的分析选项：

| 视图 | 说明 |
|------|------|
| **Large Icons** | 大图标，同时查看多个套料图 |
| **Small Icons** | 小图标，同上 |
| **List Icons** | 极简列表 |
| **Details** | 详细：小图标+名称+材质+利用率%。可按列排序 |
| **Arrange Icons** | 按 NC 程序/材质/利用率排序 |
| **Line Up Icons** | 对齐图标 |
| **Auto Arrange** | 自动排列 |

---

## 7.5 云端套料（Cloud Nesting）

### 前提

- Autodesk 订阅用户
- 在 CAMduct 内直接访问

### 流程

1. 上传工单 → 云端用 **10 种算法并行套料**
2. 完成 → 邮件通知
3. 下载套料结果到 CAMduct
4. 已套料工单云端保存 **96 小时**

### 评估指标

| 列 | 说明 |
|----|------|
| **Sheet Qty** | 该方案使用板材数 |
| **Average Usage** | 材料利用率。**越高越高效** |

选择最优方案 → `Merge Nest into CAMduct` 下载。

---

## 7.6 自动填充零件（Auto Fill Parts）

将指定管件**无限量**填充到套料板材剩余空间，替代撕切线。

### 设置

1. 管件属性中勾选 Auto Fill
2. 以数量 1 放入工单 → Nested 列显示 "Auto"
3. 套料时自动计算最大可放数量
4. 套料后显示实际放置数量

> 💡 适合填充小零件（法兰垫片、小连接件等）。

---

## 7.7 共线切割（Common Line Cutting）

减少切割时间和热变形。**沿直线边效果最佳**。

### 条件

- 最小零件间距 ≥ 切缝值（Kerf）。如切缝 1mm → 间距 ≥ 1mm
- 切缝值查看：`Installed Machines → Tools`

### 流程

1. 套料完成 → Sheet Machining Options
2. 启用共线切割
3. NC 编号分配
4. NC Reader 预览 → 零件间无间距，共用切割线

---

## 7.8 自动套料选项（Autonest Options）

### 精度/速度滑块

| 位置 | 效果 |
|------|------|
| **偏左（Accurate）** | 紧密套料，最小废料，耗时更长 |
| **偏右（Faster）** | 快速完成但废料较多 |
| **中间（Optimal）** | 平衡 |

### 选项

| 选项 | 说明 |
|------|------|
| **Use Existing Sheets In Job** | 使用工单中已有空板 |
| **Try Alternative Solutions if Target not Reached** | 尝试多方案达到最优 |

### 优化项

| 选项 | 说明 |
|------|------|
| **Rotate Parts to Minimum Rectangles** | 旋转至最小外接矩形方向贴齐板边 |
| **Pre-Nest Parts with Each Other** | 先将零件拼成矩形再套料 |
| **Pre-Nest One-off Part Qties** | 尝试单件零件互拼 |
| **Pre-Nest Parts in Holes** | 将零件放入其他零件内部（孔中套料） |
| **Allow Nest In Stitched Holes** | 允许在微连接孔内套料 |
| **Allow edge nest parts equal to sheet width** | 零件宽度等于板宽时贴边切割（特别适用于与板宽相同直管） |

---

## 7.9 多头割炬属性（MultiTorch Properties）

配置**同一横梁上多个割炬**同时切割。多头割炬共享同一 NC 码（不同于多刀头）。

### 模式

| 模式 | 说明 |
|------|------|
| **Do not Use** | 取消 |
| **Basic Multiple Torch** | 基础设置 |
| **Advanced Multiple Torch** | 高级设置 |

### 间距

| 方式 | 说明 |
|------|------|
| **Space Nest for - Torches** | 指定割炬数，以最大零件尺寸为间距 |
| **Use Spacing of - Units** | 指定固定间距值 |

### 相似展开件链接

`Allow Multi-Torch of Similar Developments`：不同管件中相同形状的展开件可链接为一组同时切割。

---

## 7.10 翻边（Flanging）

配置库中翻边相关选项：

| 选项 | 说明 |
|------|------|
| **Use Flanged Sheets** | 使用翻边板材 |
| **Flanged Edges** | 指定哪些边翻边 |
| **Allow Margin at Edge** | 每边边距 |
| **Calculate Flanges for Nested Parts** | 计算已套料零件翻边 |
| **Break on Angle Change more than** | 角度变化超值断开 |
| **Break on Radius Change more than** | 半径变化超值断开 |
| **Minimum Reported Length** | 仅报告大于此最小长度的翻边 |
| **Stress Tables** | 应力表编辑 |
| **Outside Tolerance** | 外侧公差 |

---

## 7.11 微连接（Stitching）

自动将套料零件通过小连接点固定到板材上，防止切割中移位。

### 基本参数

| 选项 | 说明 |
|------|------|
| **Default Auto Stitching Values** | 定义微连接长度和数量 |
| **Use Spacing** | 按指定间距在岛周围分布微连接 |
| **Stitch at Start/End of Island(s)** | 在岛起点/终点加微连接 |

### 自动微连接条件

| 条件 | 说明 |
|------|------|
| Outer Islands – If Long Side < | 外岛长边 < 值 → 微连接。`Any` = 不论尺寸 |
| Outer Islands – If Short Side < | 外岛短边 < 值 |
| Inner Islands – If Long Side < | 内岛同上 |
| Inner Islands – If Short Side < | 内岛同上 |

> 💡 外岛（Outer）= 板材上外部零件；内岛（Inner）= 零件内部的孔洞部分。

---

## 7.12 余料管理（Remnants）

配置自动保存余料的条件。需先在 `Database → Nesting` 下勾选 Remnants 启用。

| 选项 | 说明 |
|------|------|
| **Only Save Sheet if Rip-Cut** | 仅当板材被撕切时才保存为余料 |
| **Minimum Length** | 仅保存余料的最小长度 |
| **Discard Used Portion** | 丢弃已切割部分（撕切线后方），避免存不可用小段余料 |

---


## 📷 配图（截自 Autodesk 官方帮助）

> ![](/img/knowledge/pipe-fitting-spec/GUID-38713C0E-67C2-41CA-8BD5-4AEA3B19A8D2.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-BE65B5F8-9927-466D-8BCF-A6F6F2F32EE6.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-50D72A9E-AB7D-41E8-975D-D08FFE766170.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-EEA97B2A-A697-473D-A082-111076BBBF30.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-73C821E1-9A22-4663-B5AA-BD75BF4A71DF.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-2E8538FC-A33B-453F-92B3-C3656384DD6B.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-F5C9EC37-46E4-479E-A07A-34A2B03FAAFA.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-8C20F322-E001-40FE-984C-A3600481073B.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-A7AF6BBA-A688-4791-8457-1DD0342FE583.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-B3E0BDAA-E6FF-4767-B428-016CCCEDCB40.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-C60BFF6C-DA9B-4630-9214-410EDF1A2FCA.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-D24493D1-65E3-47D7-A90C-7A3592B393C1.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-FE0C4EE0-F050-46AB-85DA-211702FD4A4F.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-58F19949-B9B4-4A19-B497-0D89BD3BA320.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-4E894EA2-1928-4E41-A561-F1835EC53ACC.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-2D82EA80-3F5F-4315-B129-0AFC360E53FA.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-AEFDC2C9-43F5-4394-A0B6-74F03FFACB16.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-1AF17F27-68EE-4984-B47B-2A6151CE7BDE.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-5E67B5D4-0C3E-4DC1-957A-E6E30FAD3CE8.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-A9571608-F874-4D02-B8E1-39837FE538EA.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-AA2BC669-252A-40F9-A08E-69FA87C4B38B.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-E2E3181B-037E-4D07-9A17-F3B7872F8865.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-A251CC45-1B3C-44F3-BA5A-D40B2C3EA0CC.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-AA2AFDEB-0C9F-42EB-B874-B5DC6CB5185B.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-935B98C3-7C99-42F1-89BA-FFC558065007.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-7FC3BE3F-4D4E-487B-8678-B5830A43A3B0.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-EFFE9279-CB1A-4743-9690-C0EFE9367A8F.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-44724D3D-FDA8-4F41-9E1A-36E2DEE4C842.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-EBA16746-2FFF-4D66-B501-E4AA65D09A6E.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-608933DC-39A9-4E6D-90DA-ED56EAB8C27C.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-A7CDCC1C-6D65-4558-BA5E-F31A9DD4B2C6.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-F3EEE60D-DD27-477A-AB66-966F7520B795.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-61DD5A19-32F5-4856-A0E2-EAEFEBFF7EE1.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-9917F392-E6B3-4F2B-B84F-28EFED23D406.webp)

> ![](/img/knowledge/pipe-fitting-spec/GUID-A03E249B-E4BB-4A13-8DAA-AEDF51834F8F.webp)

---

## 相关笔记

- I.06.05 轮廓处理器Profiler → 套料前零件前处理
- I.06.06 板材管理 → 库存板材与余料
- [I.02 CAMduct基本操作手册](/knowledge/pipe-fitting-spec/I-02-CAMduct基本操作手册/)#I.02.2 手工排料与自动排料后的手工调整 → 实操速查

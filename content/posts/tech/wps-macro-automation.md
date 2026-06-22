---
title: "⚡ WPS JS宏实战：风管厂加工单自动化从0到1"
date: 2026-06-22
description: "分享用WPS JS宏实现风管加工单自动格式化的实战经验，从录制宏到代码优化，适合零基础入门。"
categories: ["编程工具"]
tags: ["WPS", "JS宏", "自动化", "加工单", "风管"]
image: /img/posts/wps-macro-automation.png
---

风管厂的加工单每天几十上百行，手动调格式、加边框、改字体……一天下来手指都酸了。去年花了一个周末，用 WPS JS 宏把加工单格式化全自动化了，从此点一下按钮，3 秒搞定。

这篇文章分享一下从零开始的实战过程，没有编程基础也能看懂。

---

## 为什么要用 WPS JS 宏？

风管厂的加工单通常是 Excel 表格，包含以下信息：

| 列 | 内容 |
|---|------|
| 编号 | 风管段编号 |
| 尺寸 | 宽×高×长 |
| 数量 | 该段数量 |
| 材质 | 镀锌板/不锈钢/防火板 |
| 接口 | 共板/角铁/插条 |
| 备注 | 特殊工艺要求 |

手工操作的问题：
- 每次调格式重复劳动
- 多人经手格式不统一
- 容易漏改某些行/列

---

## 第一步：录制宏，理解基本语法

WPS 自带"录制宏"功能，这是零基础入门的最佳方式：

1. 打开 WPS 表格 → 「工具」→「宏」→「录制宏」
2. 做一遍你平时手动操作的步骤（加边框、改字体、设行高等）
3. 停止录制 → 「查看宏」→ 「编辑」

录出来的代码大概长这样：

```javascript
function 格式化加工单() {
    Range("A1:G100").Select();
    Selection.Font.Name = "微软雅黑";
    Selection.Font.Size = 10;
    Selection.Borders.LineStyle = 1;
    Rows("1:1").Select();
    Selection.Font.Bold = true;
    Selection.Interior.Color = 15773696; // 浅蓝色
}
```

这已经能用了，但**录制的宏有冗余代码**，需要手动精简。

---

## 第二步：优化代码，从"能跑"到"好用"

录制宏最大的问题是：把所有操作都录下来，包括你点错的、多选的、不必要的。优化后的版本：

```javascript
function 格式化加工单() {
    let ws = ActiveSheet;
    let lastRow = ws.UsedRange.Rows.Count;
    let lastCol = ws.UsedRange.Columns.Count;

    // 设置全局字体
    ws.UsedRange.Font.Name = "微软雅黑";
    ws.UsedRange.Font.Size = 10;

    // 加全边框
    ws.UsedRange.Borders.LineStyle = 1;

    // 表头蓝底白字加粗
    let header = ws.Rows(1);
    header.Font.Bold = true;
    header.Font.Color = 16777215; // 白色
    header.Interior.Color = 15773696; // 浅蓝

    // 自动列宽
    ws.UsedRange.Columns.AutoFit();

    // 数量列居中
    ws.Columns("D").HorizontalAlignment = -4108; // xlCenter

    MsgBox("格式化完成！共处理 " + lastRow + " 行");
}
```

---

## 第三步：添加风管厂专属逻辑

加工单常见的行业需求，可以用宏一步到位：

### 1. 自动标红特殊材质

```javascript
// 不锈钢行自动标红
for (let i = 2; i <= lastRow; i++) {
    let 材质 = ws.Cells(i, 4).Value2; // 假设第4列是材质
    if (材质 && 材质.includes("不锈钢")) {
        ws.Rows(i).Font.Color = 255; // 红色
    }
}
```

### 2. 两端接口不同自动提醒

```javascript
// 两端接口不一样的行加黄色底
for (let i = 2; i <= lastRow; i++) {
    let 接口1 = ws.Cells(i, 5).Value2; // 左端接口
    let 接口2 = ws.Cells(i, 6).Value2; // 右端接口
    if (接口1 && 接口2 && 接口1 !== 接口2) {
        ws.Rows(i).Interior.Color = 65535; // 黄色提醒
    }
}
```

---

## WPS JS宏 vs VBA：为什么选 JS？

| 对比维度 | WPS JS宏 | VBA |
|---------|---------|-----|
| 学习门槛 | 低（JavaScript 语法简单） | 中（VBA 语法特殊） |
| 调试体验 | WPS 内置编辑器，可断点 | Excel VBA 编辑器 |
| 跨平台 | 支持 Windows/Linux/Web | 仅 Windows |
| 社区资源 | 较少但增长快 | 极丰富 |

---

## 总结

WPS JS 宏没有想象中那么难。**录制 → 精简 → 加逻辑**，三步就能把重复性工作自动化。风管厂技术部用这套方法，已经把加工单格式化、保温棉清单生成、法兰数量统计等 5 个环节全部做成了一键宏。

如果你每天在 WPS 表格上有超过 10 分钟的重复操作，值得花一个周末学一下 JS 宏——一次性投入，永久省时间。

---

#暖通风管 #风管制作 #技术笔记

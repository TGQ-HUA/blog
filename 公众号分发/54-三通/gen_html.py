# -*- coding: utf-8 -*-
"""生成 54-三通 视频 HTML：62 beats，横屏1920x1080，多巴胺风格"""
import json, os

# beat 数据: (start, end, 容器, 主标题, 副标题/说明, 数字层)
# 容器: A居中大字 B左文右数 C上下分栏 D并列卡片 E双栏对比 F数字时间轴 G全屏警示
beats = [
    (0.100, 3.996, "A", "老赵拿着三通的图来找我", "上周，车间", ""),
    (3.946, 7.106, "C", "排版把支口位置画偏了", "支管接上去歪着一截", ""),
    (7.106, 11.469, "G", "现场焊工骂骂咧咧，要返工", "", ""),
    (11.469, 14.513, "A", "问题不在排版", "在做单", ""),
    (14.513, 17.083, "C", "单子上压根没写", "支口怎么对", ""),
    (17.083, 21.655, "B", "排版师傅按自己习惯填位置", "跟现场走向对不上", "习惯"),
    (21.655, 27.094, "D", "客户单子：侧三通", "500×200 / 长720 / 2节", ""),
    (27.094, 31.064, "A", "支口对中还是偏边？", "图纸没画，电话没说", ""),
    (31.064, 34.224, "G", "自由发挥，一发挥就出错", "", ""),
    (34.224, 38.171, "A", "三通不是三根管拼一起", "是三个口的位置规矩", ""),
    (38.171, 41.793, "C", "先分清三通有几种", "矩形三通就三类", ""),
    (41.793, 45.659, "E", "正三通 · 蝴蝶型", "两侧对称分支", "蝴蝶"),
    (45.659, 49.155, "A", "正三通 · T型", "单侧直分支", ""),
    (49.155, 51.527, "C", "侧三通", "支管斜着出去", ""),
    (51.527, 54.618, "D", "客户说三通", "多数人想的是T型", ""),
    (54.618, 58.541, "B", "现场最常见的", "其实是侧三通和蝴蝶型", "2类"),
    (58.541, 62.314, "C", "做单第一件事", "分清楚客户说的是哪个", ""),
    (62.314, 66.377, "G", "三个口尺寸不问清，后面全错", "", ""),
    (66.377, 68.912, "A", "三通最要命：支口位置", "", ""),
    (68.912, 71.944, "C", "手册写得明白", "对口默认对中", ""),
    (71.944, 75.185, "D", "三个口中心线对齐", "这是默认值", ""),
    (75.185, 77.337, "G", "默认两个字，最坑人", "", ""),
    (77.337, 80.382, "C", "不是每个客户", "都懂对中是什么意思", ""),
    (80.382, 84.108, "B", "图纸不画，做单不问", "排版师傅一猜就歪", "歪"),
    (84.108, 88.206, "A", "我们厂的规矩", "必须显式写“对中”", ""),
    (88.206, 92.141, "D", "贴梁贴墙的活", "先打电话问一句", ""),
    (92.141, 94.918, "A", "多问一句话", "省车间半天返工", ""),
    (94.918, 97.430, "C", "第二个高频坑", "支口不等高", ""),
    (97.430, 102.141, "B", "底口500×200", "侧口320×150 高差50", "50"),
    (102.141, 107.835, "G", "硬做不行！先加大小头，改成等高", "", ""),
    (107.835, 112.951, "C", "先加一节变径", "把支口高度拉平了再做", ""),
    (112.951, 115.590, "A", "我们以前图省事", "不等高硬做", ""),
    (115.590, 119.594, "G", "支管扭曲、法兰对不上、漏风返工", "", ""),
    (119.594, 122.141, "B", "算下来", "比加个大小头贵多了", "贵"),
    (122.141, 125.868, "A", "三通带变径是常态", "变径时默认底平", ""),
    (125.868, 128.599, "D", "偏差 ≤ 100", "用内弧", "100"),
    (128.599, 131.168, "A", "偏差 > 100", "用内菱角", ""),
    (131.168, 133.599, "E", "内弧费料", "内菱角省料", "对比"),
    (133.599, 137.939, "G", "偏差大还硬做内弧，咬口都咬不住", "", ""),
    (137.939, 139.849, "A", "做单还有两个细节", "", ""),
    (139.849, 142.291, "C", "偏移必须写“对中”", "不能空着", ""),
    (142.291, 147.303, "D", "成型方式：5片式", "异形件标准做法", "5"),
    (147.303, 149.942, "B", "别让师傅", "自己琢磨怎么下料", "别"),
    (149.942, 154.224, "C", "配套一条", "支口够大，要加导流片", ""),
    (154.224, 159.108, "F", "导流片数量", "平面边长÷500，最多4片，间距≥200mm", "≤4"),
    (159.108, 163.506, "A", "做单顺带查一眼", "别等装完风量不够再补", ""),
    (163.506, 166.168, "C", "三通在图纸上", "就一个符号", ""),
    (166.168, 170.520, "B", "支口位置、偏法、变径", "设计院基本不画全", "不画"),
    (170.520, 173.159, "A", "全压在", "排版和做单的人身上", ""),
    (173.159, 176.980, "C", "老师傅看一眼现场", "就知道支口往哪偏", ""),
    (176.980, 180.983, "B", "新人照单子填", "错了才知道问", "错"),
    (180.983, 183.449, "A", "这不是谁笨", "是没地方查", ""),
    (183.449, 188.009, "G", "国标管材料管精度，唯独支口往哪偏管不着", "", ""),
    (188.009, 190.081, "A", "全靠厂里自己的规矩", "", ""),
    (190.081, 194.328, "D", "写进手册，贴在工位", "谁来了都能翻", ""),
    (194.328, 196.956, "C", "老赵那张三通", "后来重做了", ""),
    (196.956, 200.949, "B", "单子补了一行", "顶偏移对中，侧偏移对中", "1行"),
    (200.949, 203.923, "A", "车间半小时出活", "现场一次装上", ""),
    (203.923, 208.067, "C", "小刘接三通的活", "第一句先问客户", ""),
    (208.067, 211.655, "G", "三个口尺寸多少？支口对中还是偏边？", "", ""),
    (211.655, 214.155, "C", "客户说", "以前没人问这么细", ""),
    (214.155, 217.094, "A", "问细了", "车间才不用返工", ""),
]

# 视觉多样性检查：≥3连续不重复
seq = [b[2] for b in beats]
for i in range(len(seq) - 2):
    if seq[i] == seq[i+1] == seq[i+2]:
        raise SystemExit(f"3连重复容器 at beat {i}: {seq[i]}")
print(f"beats={len(beats)} 容器序列: {' '.join(seq)}")
print("多样性检查通过")

AUDIO_DUR = 217.128

css = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>三通的规矩</title>
<style>
  @font-face{font-family:'Microsoft YaHei';src:local('Microsoft YaHei')}
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1920px;height:1080px;overflow:hidden;margin:0;font-family:'Microsoft YaHei',sans-serif}
  .center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:120px}
  .clip{position:absolute;inset:0}
  /* 版式容器 */
  .lay{position:relative;width:1680px;height:840px;display:flex}
  .la{flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:28px}
  .lb{flex-direction:row;align-items:center;justify-content:space-between;padding:0 60px;gap:48px}
  .lc{flex-direction:column;justify-content:center;align-items:flex-start;gap:36px;padding:0 80px}
  .ld{flex-direction:row;justify-content:center;align-items:center;gap:40px;flex-wrap:wrap}
  .le{flex-direction:row;justify-content:center;align-items:center;gap:48px}
  .lf{flex-direction:column;justify-content:center;align-items:center;gap:36px;text-align:center}
  .lg{flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:24px;background:rgba(220,38,38,0.08);border:2px solid rgba(220,38,38,0.35);border-radius:32px;padding:60px}
  /* 元素 */
  .big{font-size:88px;font-weight:900;color:#1e3a5f;line-height:1.25}
  .mid{font-size:56px;font-weight:700;color:#7c3aed;line-height:1.3}
  .num{font-size:120px;font-weight:900;color:#f97316;text-shadow:0 0 30px rgba(249,115,22,0.25)}
  .sub{font-size:44px;color:#475569;line-height:1.5}
  .card{background:rgba(255,255,255,0.22);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(255,255,255,0.35);box-shadow:0 8px 32px rgba(0,0,0,0.06),inset 0 1px 0 rgba(255,255,255,0.4);border-radius:22px;padding:36px 48px;text-align:center}
  .card.on{border-color:rgba(37,99,235,0.4);background:rgba(37,99,235,0.10)}
  .card.off{opacity:0.45;filter:grayscale(0.6)}
  .fnode{display:flex;flex-direction:column;align-items:center;gap:20px;width:340px}
  .fnum{font-size:110px;font-weight:900;color:#2563eb}
  .fsub{font-size:44px;color:#475569;text-align:center;line-height:1.4}
  .ftail{margin-top:36px;font-size:40px;color:#dc2626;font-weight:600;text-align:center}
  .orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:0.45}
  .orb-1{width:520px;height:520px;background:radial-gradient(circle,#60a5fa,transparent);top:-180px;left:-140px}
  .orb-2{width:450px;height:450px;background:radial-gradient(circle,#c084fc,transparent);top:-160px;right:220px}
  .orb-3{width:380px;height:380px;background:radial-gradient(circle,#f97316,transparent);bottom:-140px;left:260px}
  .orb-4{width:360px;height:360px;background:radial-gradient(circle,#34d399,transparent);bottom:-120px;right:-100px}
  .orb-5{width:420px;height:420px;background:radial-gradient(circle,#f472b6,transparent);top:300px;left:58%;transform:translateX(-50%)}
</style>
</head>
<body>

<div id="root" class="clip" data-composition-id="main" data-start="0" data-duration="__AUDIO__" data-width="1920" data-height="1080" style="position:relative;width:1920px;height:1080px;overflow:hidden;background:linear-gradient(150deg,#d4e8ff 0%,#ddd4ff 18%,#e8d4f8 35%,#d4f0ff 52%,#d8e4ff 70%,#e4d8f8 85%,#d4e8ff 100%);">

<div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div><div class="orb orb-4"></div><div class="orb orb-5"></div>

<audio id="narration" class="clip" data-start="0" data-duration="__AUDIO__" data-track-index="20" src="narration.mp3" data-volume="1.0"></audio>
"""

def beat_html(i, b):
    s, e, lay, big, sub, num = b
    cid = f"b{i}"
    inner = ""
    if lay == "A":
        inner = f'<div class="lay la">'
        if big: inner += f'<div class="big">{big}</div>'
        if sub: inner += f'<div class="sub">{sub}</div>'
        inner += '</div>'
    elif lay == "B":
        inner = f'<div class="lay lb">'
        if sub: inner += f'<div class="sub" style="max-width:1000px">{sub}</div>'
        if num: inner += f'<div class="num">{num}</div>'
        inner += '</div>'
    elif lay == "C":
        inner = f'<div class="lay lc">'
        if big: inner += f'<div class="big">{big}</div>'
        if sub: inner += f'<div class="mid">{sub}</div>'
        inner += '</div>'
    elif lay == "D":
        inner = f'<div class="lay ld">'
        if big: inner += f'<div class="card mid on">{big}</div>'
        if sub: inner += f'<div class="card mid off">{sub}</div>'
        inner += '</div>'
    elif lay == "E":
        inner = f'<div class="lay le">'
        if big: inner += f'<div class="card mid on">{big}</div>'
        if sub: inner += f'<div class="card mid off">{sub}</div>'
        inner += '</div>'
    elif lay == "F":
        inner = f'<div class="lay lf">'
        if big: inner += f'<div class="big">{big}</div>'
        if num: inner += f'<div class="num">{num}</div>'
        if sub: inner += f'<div class="sub">{sub}</div>'
        inner += '</div>'
    elif lay == "G":
        inner = f'<div class="lay lg">'
        if big: inner += f'<div class="big" style="color:#dc2626">{big}</div>'
        if sub: inner += f'<div class="sub">{sub}</div>'
        inner += '</div>'
    return f'<!-- B{i} {s:.3f}-{e:.3f} {lay} -->\n<div id="{cid}" class="clip" data-start="{s:.3f}" data-duration="{e-s:.3f}">\n  <div class="center">\n    {inner}\n  </div>\n</div>'

body = '\n'.join(beat_html(i, b) for i, b in enumerate(beats))

# GSAP 脚本
s_vars = ", ".join(f"s{i}={b[0]:.3f}" for i, b in enumerate(beats))
dur = [b[1]-b[0] for b in beats]
anim = []
for i, b in enumerate(beats):
    s, e, lay, big, sub, num = b
    cid = f"#b{i}"
    d = e - s
    out_t = d - 0.3  # 提前0.3s退场
    L = []
    if lay == "A":
        L.append(f'tl.fromTo("{cid} .lay .big", {{opacity:0, scale:.8, y:30, filter:"blur(6px)"}}, {{opacity:1, scale:1, y:0, filter:"blur(0px)", duration:.6, ease:"back.out(1.6)"}}, s{i}+0.1);')
        if sub: L.append(f'tl.fromTo("{cid} .lay .sub", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:.45, ease:"power2.out"}}, s{i}+0.4);')
        L.append(f'tl.to("{cid} .lay .big", {{opacity:0, scale:.92, y:-20, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        if sub: L.append(f'tl.to("{cid} .lay .sub", {{opacity:0, y:-15, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .big", {{opacity:0}}, s{i}+{d:.3f});')
        if sub: L.append(f'tl.set("{cid} .lay .sub", {{opacity:0}}, s{i}+{d:.3f});')
    elif lay == "B":
        L.append(f'tl.fromTo("{cid} .lay .num", {{opacity:0, x:60, scale:.8}}, {{opacity:1, x:0, scale:1, duration:.6, ease:"back.out(1.6)"}}, s{i}+0.1);')
        if sub: L.append(f'tl.fromTo("{cid} .lay .sub", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:.5, ease:"power2.out"}}, s{i}+0.3);')
        L.append(f'tl.to("{cid} .lay .num", {{opacity:0, scale:.9, y:-15, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        if sub: L.append(f'tl.to("{cid} .lay .sub", {{opacity:0, y:-15, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .num", {{opacity:0}}, s{i}+{d:.3f});')
        if sub: L.append(f'tl.set("{cid} .lay .sub", {{opacity:0}}, s{i}+{d:.3f});')
    elif lay == "C":
        L.append(f'tl.fromTo("{cid} .lay .big", {{opacity:0, y:-24}}, {{opacity:1, y:0, duration:.5, ease:"power2.out"}}, s{i}+0.1);')
        if sub: L.append(f'tl.fromTo("{cid} .lay .mid", {{opacity:0, y:-24}}, {{opacity:1, y:0, duration:.5, ease:"power2.out"}}, s{i}+0.1);')
        L.append(f'tl.to("{cid} .lay .big", {{opacity:0, y:-18, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        if sub: L.append(f'tl.to("{cid} .lay .mid", {{opacity:0, y:-18, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .big", {{opacity:0}}, s{i}+{d:.3f});')
        if sub: L.append(f'tl.set("{cid} .lay .mid", {{opacity:0}}, s{i}+{d:.3f});')
    elif lay in ("D", "E"):
        L.append(f'tl.fromTo("{cid} .lay .card", {{opacity:0, y:30, scale:.9}}, {{opacity:1, y:0, scale:1, duration:.5, stagger:.15, ease:"back.out(1.4)"}}, s{i}+0.1);')
        L.append(f'tl.to("{cid} .lay .card", {{opacity:0, y:-18, scale:.95, duration:.3, stagger:.08, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .card", {{opacity:0}}, s{i}+{d:.3f});')
    elif lay == "F":
        L.append(f'tl.fromTo("{cid} .lay .big", {{opacity:0, scale:.8, y:30, filter:"blur(6px)"}}, {{opacity:1, scale:1, y:0, filter:"blur(0px)", duration:.6, ease:"back.out(1.6)"}}, s{i}+0.1);')
        L.append(f'tl.fromTo("{cid} .lay .num", {{opacity:0, scale:2, y:40}}, {{opacity:1, scale:1, y:0, duration:.7, ease:"back.out(1.8)"}}, s{i}+0.5);')
        if sub: L.append(f'tl.fromTo("{cid} .lay .sub", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:.45, ease:"power2.out"}}, s{i}+0.8);')
        L.append(f'tl.to("{cid} .lay .big", {{opacity:0, y:-18, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.to("{cid} .lay .num", {{opacity:0, y:-15, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        if sub: L.append(f'tl.to("{cid} .lay .sub", {{opacity:0, y:-15, duration:.3, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .big", {{opacity:0}}, s{i}+{d:.3f});')
        L.append(f'tl.set("{cid} .lay .num", {{opacity:0}}, s{i}+{d:.3f});')
        if sub: L.append(f'tl.set("{cid} .lay .sub", {{opacity:0}}, s{i}+{d:.3f});')
    elif lay == "G":
        L.append(f'tl.fromTo("{cid} .lay .big", {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.55, ease:"back.out(2)"}}, s{i}+0.1);')
        if sub: L.append(f'tl.fromTo("{cid} .lay .sub", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.4, ease:"power2.out"}}, s{i}+0.35);')
        L.append(f'tl.to("{cid} .lay .big", {{opacity:0, scale:.85, duration:.25, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        if sub: L.append(f'tl.to("{cid} .lay .sub", {{opacity:0, y:-12, duration:.25, ease:"power2.in"}}, s{i}+{out_t:.3f});')
        L.append(f'tl.set("{cid} .lay .big", {{opacity:0}}, s{i}+{d:.3f});')
        if sub: L.append(f'tl.set("{cid} .lay .sub", {{opacity:0}}, s{i}+{d:.3f});')
    anim.append(f'// B{i} {lay}')
    anim.extend(L)

script = f"""
<script src="gsap.min.js"></script>
<script>
var tl = gsap.timeline({{paused:true}});

var {s_vars};

{chr(10).join(anim)}
</script>
</body>
</html>
"""

html = css.replace("__AUDIO__", f"{AUDIO_DUR:.3f}") + body + "\n\n</div>\n\n" + script
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"已生成 {out} ({len(html)} bytes)")

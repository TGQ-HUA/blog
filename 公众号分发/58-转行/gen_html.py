# -*- coding: utf-8 -*-
"""58-转行 视频 HTML 生成器：VTT beat 时间轴 + 场景 Storyboard → index.html"""
import json, re

# VTT 时间解析（已从 narration.vtt 提取）
def ts(s):
    h, m, rest = s.split(":")
    sec = int(h)*3600 + int(m)*60 + float(rest.replace(",", "."))
    return round(sec, 3)

# beats: (start, end, text)
raw_vtt = open(r"G:\blog\公众号分发\58-转行\narration.vtt", encoding="utf-8").read()
beats = []
for block in re.findall(r"\d+\n([\d:,\.]+) --> ([\d:,\.]+)\n(.+)", raw_vtt):
    s, e, t = block
    beats.append((ts(s), ts(e), t.strip()))

print("beats:", len(beats), "总时长:", round(beats[-1][1], 1))

# 场景定义: (id, 类型, beat区间[起,止], 关键HTML)
# 容器类型用于视觉多样性检查
scenes = [
    ("s00", "bare",  (None, None), """<div class="bare"><div class="bn" style="font-size:96px;color:#0f172a">卖过家具的人</div><div class="bn" style="font-size:116px;color:#2563eb">管技术部</div><div class="bl" style="font-size:44px;color:#f97316;font-weight:700">这12年，我怎么过来的</div></div>"""),
    ("s01", "tale",  (0, 1), """<div class="tale" id="s01t"><div class="glass"><div class="tt">前天，小伙子问我</div><div class="ts m">前天，新来的小伙子问我。</div><div class="ts m" style="color:#2563eb;font-weight:700;font-size:46px">师傅，你大学学的啥专业？</div></div></div>"""),
    ("s02", "ccard", (2, 4), """<div class="ccard" id="s02c"><div class="ch">我说，我没上过大学</div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">卖过三年家具，后来在五金厂画过图。</div><div class="m">再后来，才进的这行。</div></div></div>"""),
    ("s03", "ask",   (5, 7), """<div class="ask" id="s03a"><div class="aq">一个卖家具的，<br>怎么坐到了<span class="hl">技术部？</span></div><div class="aa m" style="color:#475569">他愣了半天。</div><div class="aa m" style="color:#2563eb;font-weight:700;font-size:48px">这话搁十二年前，我自己也不信。</div></div>"""),
    ("s04", "bare",  (8, 9), """<div class="bare"><div class="bn" style="font-size:60px;color:#0f172a">卖家具那三年</div><div class="bn" style="font-size:88px;color:#0f172a">教会我一件事</div><div class="bn" style="font-size:132px;color:#2563eb">听懂人话</div></div>"""),
    ("s05", "dual",  (10, 11), """<div class="dual" id="s05d"><div class="dcard"><div class="dh" style="color:#dc2626">客户说</div><div class="dd m">这柜子颜色不太正。</div></div><div class="dcard"><div class="dh" style="color:#2563eb">翻译过来</div><div class="dd m">价格能不能少点。</div><div class="dd" style="font-size:44px;color:#2563eb;font-weight:900">得听懂弦外之音</div></div></div>"""),
    ("s06", "ccard", (12, 13), """<div class="ccard" id="s06c"><div class="ch">这本事，<span class="accent">特别值钱</span></div><div class="glass"><div class="m">后来做风管清量、跟客户对图纸。</div><div class="m" style="font-size:46px;font-weight:700;color:#2563eb">图纸上写"尽量少接缝"，</div><div class="m" style="font-size:46px;font-weight:700;color:#f97316">一句话三种理解。</div></div></div>"""),
    ("s07", "grid3", (15, 18), """<div style="text-align:center;width:88%"><div class="btitle" id="s07t">图纸上写：<span class="accent">尽量少接缝</span></div><div class="grid3" id="s07g"><div class="gitem"><div class="gh">师傅理解成</div><div class="gd" style="font-size:46px;color:#2563eb;font-weight:900">能拼就拼</div></div><div class="gitem"><div class="gh">业主理解成</div><div class="gd" style="font-size:46px;color:#f97316;font-weight:900">别让我看见缝</div></div><div class="gitem"><div class="gh">一句话</div><div class="gd" style="font-size:46px;color:#dc2626;font-weight:900">三种理解</div></div></div><div class="m" style="font-size:44px;color:#dc2626;font-weight:700;margin-top:28px">不把话问透，后面全是返工</div></div>"""),
    ("s08", "ccard", (19, 21), """<div class="ccard" id="s08c"><div class="ch">转五金设计，<span style="color:#dc2626">我飘过一阵</span></div><div class="glass"><div class="m">觉得自己会画图，是个人才了。</div><div class="m" style="font-size:48px;font-weight:700;color:#dc2626">结果，第一张图就出了事。</div></div></div>"""),
    ("s09", "warn",  (22, 25), """<div class="warn" id="s09w"><div class="wl">第一张图</div><div class="wm">支架孔位，差了<span class="hl">5毫米</span></div><div class="ws m">给支架画的孔位，跟实际螺栓差了五毫米。</div><div class="ws m" style="color:#dc2626;font-weight:700;font-size:44px">现场装不上，就是装不上。</div><div class="ws m" style="color:#dc2626;font-weight:700">整批返工。</div></div>"""),
    ("s10", "bare",  (26, 27), """<div class="bare"><div class="bn" style="font-size:72px;color:#0f172a">图纸上的一毫米</div><div class="bn" style="font-size:104px;color:#dc2626">车间里就是一刀一锤的事</div></div>"""),
    ("s11", "ccard", (28, 32), """<div class="ccard" id="s11c"><div class="ch">进风管厂头两年，<span class="accent">最笨的活</span></div><div class="glass"><div class="m" style="font-size:52px;font-weight:900;color:#f97316">抄。</div><div class="m">老师傅怎么下料，我记。</div><div class="m">怎么算面积，我记。</div><div class="m">怎么给弯头分节，我还记。</div></div></div>"""),
    ("s12", "dual",  (33, 35), """<div class="dual" id="s12d"><div class="dcard"><div class="dh" style="color:#dc2626">光记没用</div><div class="dd m">老师傅的规矩在脑子里。</div></div><div class="dcard"><div class="dh" style="color:#2563eb">退休就没了</div><div class="dd m">他退休了，规矩就没了。</div><div class="dd" style="font-size:42px;color:#dc2626;font-weight:900">人一走，经验就带走</div></div></div>"""),
    ("s13", "warn",  (36, 38), """<div class="warn" id="s13w"><div class="wl">真实一幕</div><div class="wm">老师傅一走<br><span class="hl">S弯没人敢下料</span></div><div class="ws m">厂里有个老师傅一走。</div><div class="ws m" style="color:#dc2626;font-weight:700">全厂停工，等新人慢慢摸索。</div></div>"""),
    ("s14", "ask",   (39, 40), """<div class="ask" id="s14a"><div class="aq">能不能把老师傅脑子里的东西<br><span class="hl">一条条挖出来？</span></div><div class="aa m" style="color:#475569">那会儿我就在想。</div></div>"""),
    ("s15", "ccard", (41, 42), """<div class="ccard" id="s15c"><div class="ch">这一写，就是<span class="accent">三年</span></div><div class="glass"><div class="m" style="font-size:64px;font-weight:900;color:#2563eb;text-align:center">16 大类 · 200 多篇</div><div class="m" style="font-size:44px;text-align:center">排版规范手册</div></div></div>"""),
    ("s16", "grid3", (43, 46), """<div style="text-align:center;width:88%"><div class="btitle" id="s16t">手册里，<span class="accent">全有据可查</span></div><div class="grid3" id="s16g"><div class="gitem"><div class="gh">弯头</div><div class="gd" style="font-size:44px;color:#2563eb;font-weight:900">怎么选 R</div></div><div class="gitem"><div class="gh">大小头</div><div class="gd" style="font-size:44px;color:#f97316;font-weight:900">对中平边怎么定</div></div><div class="gitem"><div class="gh">三通</div><div class="gd" style="font-size:44px;color:#dc2626;font-weight:900">怎么分节</div></div></div></div>"""),
    ("s17", "ccard", (47, 49), """<div class="ccard" id="s17c"><div class="ch">光有手册，<span style="color:#dc2626">还不够</span></div><div class="glass"><div class="m">我又自学了编程。</div><div class="m" style="font-size:48px;font-weight:700;color:#2563eb">用 Delphi 和 WPS 宏，做了套管理系统。</div></div></div>"""),
    ("s18", "grid3", (50, 52), """<div style="text-align:center;width:88%"><div class="btitle" id="s18t">以前靠人盯，<span class="accent">现在靠系统盯</span></div><div class="grid3" id="s18g"><div class="gitem"><div class="gh">报价</div><div class="gd" style="font-size:42px;color:#2563eb;font-weight:900">排版 · 下单</div></div><div class="gitem"><div class="gh">出错登记</div><div class="gd m">一条线走完</div></div><div class="gitem"><div class="gh">一条线</div><div class="gd" style="font-size:44px;color:#f97316;font-weight:900">全流程闭环</div></div></div></div>"""),
    ("s19", "tale",  (53, 54), """<div class="tale" id="s19t"><div class="glass"><div class="tt">同行问我</div><div class="ts m">转行的人，怎么站住脚？</div><div class="ts m" style="color:#f97316;font-weight:700;font-size:46px">我说三条，都是自己踩出来的。</div></div></div>"""),
    ("s20", "warn",  (55, 56), """<div class="warn" id="s20w"><div class="wl">第一条</div><div class="wm">先学会<span class="hl">听懂人话</span></div><div class="ws m" style="font-size:46px;font-weight:700;color:#2563eb">技术是死的，需求是活的。</div></div>"""),
    ("s21", "dual",  (57, 58), """<div class="dual" id="s21d"><div class="dcard"><div class="dh" style="color:#2563eb">第二条</div><div class="dd m">画完图，去车间看。</div></div><div class="dcard"><div class="dh" style="color:#dc2626">差一毫米</div><div class="dd m">图纸和实物差一毫米，都是废料。</div><div class="dd" style="font-size:42px;color:#dc2626;font-weight:900">图纸是废纸，实物才是答案</div></div></div>"""),
    ("s22", "warn",  (59, 60), """<div class="warn" id="s22w"><div class="wl">第三条</div><div class="wm">把经验写成<span class="hl">文档</span></div><div class="ws m" style="font-size:46px;font-weight:700;color:#2563eb">脑子会忘，人会走，文档不会。</div></div>"""),
    ("s23", "ccard", (61, 64), """<div class="ccard" id="s23c"><div class="ch">这三条，<span class="accent">全是笨功夫</span></div><div class="glass"><div class="m">没有一条是"聪明"的事。</div><div class="m" style="font-size:48px;font-weight:700;color:#f97316">但笨功夫攒多了，</div><div class="m" style="font-size:48px;font-weight:700;color:#f97316">就是别人拿不走的底气。</div></div></div>"""),
    ("s24", "ask",   (65, 69), """<div class="ask" id="s24a"><div class="aq">转行晚不晚？<br><span class="hl">不晚。</span></div><div class="aa m" style="color:#475569">你不是来混口饭吃的。</div><div class="aa m" style="color:#2563eb;font-weight:700;font-size:48px">是来学一门本事的。</div></div>"""),
    ("s25", "grid3", (70, 75), """<div style="text-align:center;width:88%"><div class="btitle" id="s25t">12年，<span class="accent">一样没浪费</span></div><div class="grid3" id="s25g"><div class="gitem"><div class="gh" style="font-size:56px;color:#2563eb;font-weight:900">那三年</div><div class="gd m">练的听人话</div></div><div class="gitem"><div class="gh" style="font-size:56px;color:#f97316;font-weight:900">那两年</div><div class="gd m">栽的跟头</div></div><div class="gitem"><div class="gh" style="font-size:56px;color:#dc2626;font-weight:900">这七年</div><div class="gd m">攒的规矩</div></div></div><div class="m" style="font-size:44px;color:#2563eb;font-weight:700;margin-top:28px">本事不看出身，看肯不肯下笨功夫</div></div>"""),
    ("s26", "bare",  (76, 78), """<div class="bare"><div class="bn" style="font-size:72px;color:#0f172a">我是奇美星暖通</div><div class="bn" style="font-size:100px;color:#2563eb">卖过家具的风管人</div><div class="bl" style="font-size:44px;color:#f97316;font-weight:700">咱们下期见 · tangguoqi.top</div></div>"""),
]

# 视觉多样性检查：≥3 连续 beat 不重复容器
types = [s[1] for s in scenes]
for i in range(len(types)):
    if i+2 < len(types) and types[i] == types[i+1] == types[i+2]:
        print("⚠️ 3连重复容器:", scenes[i][0], types[i])
print("容器序列:", " ".join(types))

# 时间轴：每个 scene 覆盖的 beat 起止 → 显示窗口
# fadeIn = 前一个 fadeOut + 0.8；cardIn = +0.2；mods = +0.5
# fadeOut = 最后 beat end + 0.6；cardOut = fadeOut - 0.35
def scene_window(sc):
    sid, typ, br, _ = sc
    if br[0] is None:
        return (0.4, 2.9)
    return (beats[br[0]][0], beats[br[1]][1] + 0.6)

windows = [scene_window(s) for s in scenes]
# 校正：fadeIn 至少在上一个 fadeOut + 0.8
ins = []
prev_out = -10
for i, (s, w) in enumerate(zip(scenes, windows)):
    w0, w1 = w
    if i == 0:
        ins.append(0.4)
    else:
        ins.append(max(w0, prev_out + 0.8))
    prev_out = w1
print("窗口:", [(scenes[i][0], round(ins[i],1), round(windows[i][1],1)) for i in range(len(scenes))])

JS = []
for i, (sid, typ, br, _) in enumerate(scenes):
    tin = round(ins[i], 2)
    tout = round(windows[i][1], 2)
    if typ == "bare":
        JS.append(f'fadeIn("#{sid}",{tin});fadeOut("#{sid}",{tout});')
    elif typ == "tale":
        JS.append(f'fadeIn("#{sid}t",{tin});cardIn("#{sid}t .glass",{tin+0.2});mods("#{sid}t",{tin+0.5},.2);cardOut("#{sid}t .glass",{tout-0.35});fadeOut("#{sid}t",{tout});')
    elif typ == "ccard":
        JS.append(f'fadeIn("#{sid}c",{tin});cardIn("#{sid}c .glass",{tin+0.2});mods("#{sid}c",{tin+0.5},.22);cardOut("#{sid}c .glass",{tout-0.35});fadeOut("#{sid}c",{tout});')
    elif typ == "ask":
        JS.append(f'fadeIn("#{sid}a",{tin});mods("#{sid}a",{tin+0.3},.25);fadeOut("#{sid}a",{tout});')
    elif typ == "warn":
        JS.append(f'fadeIn("#{sid}w",{tin});mods("#{sid}w",{tin+0.3},.2);fadeOut("#{sid}w",{tout});')
    elif typ == "dual":
        JS.append(f'fadeIn("#{sid}d",{tin});cardIn("#{sid}d",{tin+0.2});mods("#{sid}d",{tin+0.5},.2);cardOut("#{sid}d",{tout-0.35});fadeOut("#{sid}d",{tout});')
    elif typ == "grid3":
        JS.append(f'fadeIn("#{sid}t",{tin});cardIn("#{sid}g",{tin+0.2});mods("#{sid}g .gitem:nth-child(1)",{tin+0.5},.15);mods("#{sid}g .gitem:nth-child(2)",{tin+0.75},.15);mods("#{sid}g .gitem:nth-child(3)",{tin+1.0},.15);cardOut("#{sid}g",{tout-0.35});fadeOut("#{sid}t",{tout});')

duration = int(beats[-1][1] + 6)
scene_html = "\n".join(f'  <!-- {sid} -->\n  <div class="scene" id="{sid}">{html}</div>' for sid, typ, br, html in scenes)
js_body = "\n".join(f"// {scenes[i][0]} {scenes[i][1]}\n{JS[i]}" for i in range(len(scenes)))

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="gsap.min.js"></script>
<style>

@font-face{{font-family:'Microsoft YaHei';src:local('Microsoft YaHei')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;overflow:hidden;font-family:"Microsoft YaHei",Arial,sans-serif;color:#0f172a}}
.bg{{position:absolute;inset:0;background:linear-gradient(150deg,#eff6ff,#fef7f0,#f0f9ff)}}
.orb{{position:absolute;border-radius:50%;filter:blur(70px);opacity:.4}}
.o1{{width:450px;height:450px;top:5%;left:3%;background:radial-gradient(circle,rgba(37,99,235,.5),transparent)}}
.o2{{width:380px;height:380px;top:40%;right:5%;background:radial-gradient(circle,rgba(249,115,22,.4),transparent)}}
.o3{{width:320px;height:320px;bottom:5%;left:35%;background:radial-gradient(circle,rgba(249,115,22,.3),transparent)}}
.o4{{width:280px;height:280px;top:60%;left:60%;background:radial-gradient(circle,rgba(37,99,235,.25),transparent)}}
.scene{{position:absolute;inset:0;opacity:0;display:flex;align-items:center;justify-content:center;padding:60px 100px}}
.glass{{background:rgba(255,255,255,.22);backdrop-filter:blur(20px) saturate(180%);border-radius:22px;padding:36px 44px;box-shadow:0 8px 32px rgba(0,0,0,.05)}}
.m{{font-size:42px;color:#1e293b;line-height:1.7;margin-bottom:10px;opacity:0}}
.m .accent{{color:#2563eb;font-weight:700}}
.m .hl{{color:#dc2626;font-weight:700}}
.m-sep{{height:14px}}
.btitle{{font-size:56px;font-weight:900;color:#0f172a;text-align:center;margin-bottom:28px;opacity:0}}
.btitle .accent{{color:#2563eb}}
.brand{{position:absolute;bottom:40px;right:80px;text-align:right;opacity:.7}}
.brand .bn{{font-size:28px;color:#64748b;font-weight:600}}
.brand .bu{{font-size:24px;color:#2563eb;margin-top:4px}}
.warn{{text-align:center;opacity:0}}
.warn .wl{{display:inline-block;background:#dc2626;color:#fff;font-size:32px;font-weight:700;padding:10px 28px;border-radius:10px;margin-bottom:18px}}
.warn .wm{{font-size:76px;font-weight:900;color:#0f172a;line-height:1.3}}
.warn .wm .hl{{color:#dc2626}}
.warn .ws{{font-size:42px;color:#64748b;margin-top:12px}}
.split{{display:flex;gap:50px;align-items:center;width:88%;opacity:0}}
.split .left{{flex:1;text-align:left}}
.split .right{{flex:1.2;text-align:left}}
.split .lt{{font-size:64px;font-weight:900;color:#0f172a;line-height:1.2}}
.split .lt .accent{{color:#2563eb}}
.split .rm{{font-size:42px;color:#1e293b;line-height:1.7;margin-bottom:8px}}
.grid3{{display:flex;gap:28px;width:88%;opacity:0}}
.gitem{{flex:1;background:rgba(255,255,255,.22);backdrop-filter:blur(20px) saturate(180%);border-radius:22px;padding:30px 26px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.05)}}
.gitem .gh{{font-size:40px;font-weight:700;color:#1e293b;margin-bottom:10px}}
.gitem .gd{{font-size:34px;color:#475569;line-height:1.6}}
.bare{{text-align:center;opacity:0}}
.bare .bn{{font-size:110px;font-weight:900;color:#2563eb;line-height:1.1}}
.bare .bl{{font-size:34px;color:#64748b;margin-top:6px}}
.dual{{display:flex;gap:40px;width:88%;opacity:0}}
.dcard{{flex:1;background:rgba(255,255,255,.22);backdrop-filter:blur(20px) saturate(180%);border-radius:22px;padding:32px 36px;box-shadow:0 8px 32px rgba(0,0,0,.05)}}
.dcard .dh{{font-size:44px;font-weight:700;color:#0f172a;margin-bottom:16px}}
.dcard .dd{{font-size:38px;color:#475569;line-height:1.6}}
.ask{{text-align:center;opacity:0}}
.ask .aq{{font-size:84px;font-weight:900;color:#0f172a;line-height:1.3}}
.ask .aq .hl{{color:#dc2626}}
.ask .aa{{font-size:44px;color:#64748b;margin-top:16px}}
.tale{{text-align:center;opacity:0;width:75%}}
.tale .glass{{padding:44px 60px}}
.tale .tt{{font-size:60px;font-weight:900;color:#0f172a;line-height:1.3;margin-bottom:14px}}
.tale .tt .accent{{color:#f97316}}
.tale .ts{{font-size:42px;color:#475569;line-height:1.7}}
.ccard{{text-align:center;opacity:0;width:88%}}
.ccard .ch{{font-size:60px;font-weight:900;color:#0f172a;margin-bottom:24px}}
.ccard .ch .accent{{color:#2563eb}}
.ccard .glass{{width:65%;margin:0 auto;text-align:left}}

</style>
</head>
<body>
<div id="root" class="clip" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1920" data-height="1080">
  <div class="bg"></div>
  <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div><div class="orb o4"></div>
  <audio id="n" class="clip" data-start="0" data-duration="{duration}" data-track-index="10" src="narration.mp3" data-volume="1.0"></audio>

{scene_html}

  <div class="brand"><div class="bn">奇美星暖通风管制作</div><div class="bu">tangguoqi.top</div></div>
</div>
<script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});window.__timelines.main=tl;
function cardIn(id,t){{tl.fromTo(id,{{opacity:0,rotationX:-25,y:80,scale:.75,filter:"blur(8px)"}},{{opacity:1,rotationX:0,y:0,scale:1,filter:"blur(0px)",duration:.7,ease:"elastic.out(1,0.4)"}},t);tl.to(id,{{boxShadow:"0 0 40px rgba(249,115,22,0.3)",duration:.5}},">-0.3");tl.to(id,{{boxShadow:"0 8px 32px rgba(0,0,0,0.05)",duration:.8}},">+0.2")}}
function cardOut(id,t){{tl.to(id,{{opacity:0,scale:.85,rotationX:10,y:-20,filter:"blur(4px)",duration:.18,ease:"power2.in"}},t);tl.set(id,{{opacity:0}},t+.25)}}
function mods(id,t,iv){{tl.fromTo(id+" .m",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.3,stagger:iv,ease:"power2.out"}},t)}}
function fadeIn(id,t){{tl.fromTo(id,{{opacity:0,scale:.92,filter:"blur(3px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:"power2.out"}},t)}}
function fadeOut(id,t){{tl.to(id,{{opacity:0,duration:.18,ease:"power2.in"}},t);tl.set(id,{{opacity:0}},t+.25)}}

{js_body}

</script>
</body>
</html>"""

with open(r"G:\blog\公众号分发\58-转行\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html 已生成, duration =", duration)

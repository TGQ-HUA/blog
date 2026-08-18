# -*- coding: utf-8 -*-
"""60-焊接 视频 HTML 生成器：VTT beat 时间轴 + 场景 Storyboard → index.html（横屏 1920x1080）"""
import json, re

def ts(s):
    h, m, rest = s.split(":")
    sec = int(h)*3600 + int(m)*60 + float(rest.replace(",", "."))
    return round(sec, 3)

raw_vtt = open(r"G:\blog\公众号分发\60-焊接\narration.vtt", encoding="utf-8").read()
beats = []
for block in re.findall(r"\d+\n([\d:,\\.]+) --> ([\d:,\\.]+)\n(.+)", raw_vtt):
    s, e, t = block
    beats.append((ts(s), ts(e), t.strip()))

print("beats:", len(beats), "总时长:", round(beats[-1][1], 1))

# 场景: (id, 容器类型, beat区间, HTML) —— 横屏版式：A居中大字/B左文右数/C上下分栏/D三列并列/E双栏对比/G全屏警示/H图文
scenes = [
    ("s00", "bare",  (None, None), """<div class="bare"><div class="bn" style="font-size:120px;color:#dc2626">0.75 的板</div><div class="bn" style="font-size:132px;color:#0f172a">也敢满焊？</div><div class="bl" style="font-size:48px;color:#f97316;font-weight:700">焊接风管的三道坎 · 我们厂吃了亏才定下</div></div>"""),
    ("s01", "tale",  (0, 3), """<div class="tale" id="s01t"><div class="glass"><div class="tt">周师傅<span class="accent">撂了焊枪</span></div><div class="ts m">一批不锈钢排烟管，焊到一半。</div><div class="ts m" style="color:#dc2626;font-weight:700;font-size:48px">这活没法干。</div></div></div>"""),
    ("s02", "warn",  (4, 6), """<div class="warn" id="s02w"><div class="wl">一枪下去</div><div class="wm">0.75 的板<br><span class="hl">直接烧穿</span></div><div class="ws m">补了焊疤难看，质检还嫌焊缝不饱满。</div></div>"""),
    ("s03", "ask",   (7, 9), """<div class="ask" id="s03a"><div class="aq">问题出在哪？<br><span class="hl">出在排版</span></div><div class="aa m" style="color:#475569">新人把焊接件，当成了咬口件来排。</div></div>"""),
    ("s04", "ccard", (10, 11), """<div class="ccard" id="s04c"><div class="ch">料厚选成了 <span class="accent">0.75</span></div><div class="glass"><div class="m" style="font-size:48px;font-weight:700">焊接件 ≠ 咬口件</div><div class="m">焊接成型对板厚的要求，是另一回事。</div></div></div>"""),
    ("s05", "dual",  (12, 14), """<div class="dual" id="s05d"><div class="dcard"><div class="dh" style="color:#2563eb">不锈钢满焊</div><div class="dd" style="font-size:64px;color:#2563eb;font-weight:900;margin:10px 0">≥0.75</div><div class="dd m">一般项目不敢排 0.75</div></div><div class="dcard"><div class="dh" style="color:#dc2626">镀锌板满焊</div><div class="dd" style="font-size:64px;color:#dc2626;font-weight:900;margin:10px 0">≥1.0</div><div class="dd m">0.75 只够点焊</div></div></div>"""),
    ("s06", "warn",  (15, 16), """<div class="warn" id="s06w"><div class="wl">结果</div><div class="wm">整批返工<br><span class="hl">报废三块板</span></div><div class="ws m">从那以后，料厚检查写进了排版流程第一条。</div></div>"""),
    ("s07", "bare",  (17, 18), """<div class="bare"><div class="bn" style="font-size:96px;color:#0f172a">焊接件的</div><div class="bn" style="font-size:132px;color:#2563eb">三道坎</div><div class="bl" style="font-size:48px;color:#f97316;font-weight:700">今天一次给你说清楚</div></div>"""),
    ("s08", "warn",  (19, 19), """<div class="warn" id="s08w"><div class="wl">第一道坎</div><div class="wm"><span class="hl">料厚门槛</span></div><div class="ws m">薄板焊接，热量散不出去。</div></div>"""),
    ("s09", "ccard", (20, 21), """<div class="ccard" id="s09c"><div class="ch">一枪下去就是</div><div class="glass"><div class="m" style="font-size:52px;font-weight:900;color:#dc2626">烧穿 · 变形 · 焊疤</div><div class="m">镀锌板更麻烦：高温烧掉镀锌层，焊缝一圈生锈。</div></div></div>"""),
    ("s10", "dual",  (22, 24), """<div class="dual" id="s10d"><div class="dcard"><div class="dh" style="color:#dc2626">镀锌板问题</div><div class="dd m">焊接高温</div><div class="dd m" style="font-weight:700">烧掉镀锌层</div></div><div class="dcard"><div class="dh" style="color:#2563eb">焊缝一圈</div><div class="dd" style="font-size:60px;color:#2563eb;font-weight:900;margin:10px 0">容易生锈</div><div class="dd m">所以满焊标准卡得更死</div></div></div>"""),
    ("s11", "ask",   (25, 25), """<div class="ask" id="s11a"><div class="aq">国标里 0.5 能用？<br><span class="hl">那是咬口厚度表</span></div><div class="aa m" style="color:#475569">GB50243 板材厚度表，是按咬口成型给的。</div></div>"""),
    ("s12", "grid3", (26, 30), """<div style="text-align:center;width:88%"><div class="btitle" id="s12t">一张表，<span class="accent">两种读法</span></div><div class="grid3" id="s12g"><div class="gitem"><div class="gh">很多人看到</div><div class="gd" style="font-size:44px;color:#2563eb;font-weight:900">0.5 能用</div></div><div class="gitem"><div class="gh">但那是</div><div class="gd" style="font-size:44px;color:#f97316;font-weight:900">咬口成型</div></div><div class="gitem"><div class="gh">焊接成型</div><div class="gd" style="font-size:44px;color:#dc2626;font-weight:900">是另一回事</div></div></div><div class="m" style="font-size:44px;color:#dc2626;font-weight:700;margin-top:28px">国标最低值 ≠ 能焊</div></div>"""),
    ("s13", "warn",  (31, 31), """<div class="warn" id="s13w"><div class="wl">第二道坎</div><div class="wm">拼板只能<br><span class="hl">直边对接</span></div><div class="ws m">不做咬口，不做翻边。</div></div>"""),
    ("s14", "ccard", (32, 33), """<div class="ccard" id="s14c"><div class="ch">直边碰直边</div><div class="glass"><div class="m" style="font-size:48px;font-weight:700">满焊拉通</div><div class="m">圆管分段对接、满焊法兰接口，全部直边。</div></div></div>"""),
    ("s15", "bare",  (34, 36), """<div class="bare"><div class="bn" style="font-size:120px;color:#2563eb">1250</div><div class="bn" style="font-size:72px;color:#0f172a">默认板宽 · 不锈钢偏窄 1240</div><div class="bl" style="font-size:48px;color:#dc2626;font-weight:700">CAD 放样，限制在 1230 以内</div></div>"""),
    ("s16", "ask",   (37, 40), """<div class="ask" id="s16a"><div class="aq">卡在 1240 要拼板？<br><span class="hl">务必调整</span></div><div class="aa m" style="color:#475569">改排版 · 改尺寸 · 五线开平</div><div class="aa m" style="color:#2563eb;font-weight:700;font-size:46px">做到不用拼板</div></div>"""),
    ("s17", "dual",  (41, 41), """<div class="dual" id="s17d"><div class="dcard"><div class="dh" style="color:#2563eb">硬拼</div><div class="dd m">不是不行</div></div><div class="dcard"><div class="dh" style="color:#dc2626">但</div><div class="dd m">焊缝多了</div><div class="dd" style="font-size:44px;color:#dc2626;font-weight:900">变形 · 漏风全上来</div></div></div>"""),
    ("s18", "warn",  (42, 42), """<div class="warn" id="s18w"><div class="wl">第三道坎</div><div class="wm">成型方案<br><span class="hl">两套逻辑</span></div><div class="ws m">焊接直管，按半周长定片数。</div></div>"""),
    ("s19", "grid3", (43, 46), """<div style="text-align:center;width:88%"><div class="btitle" id="s19t">半周长定片数</div><div class="grid3" id="s19g"><div class="gitem"><div class="gh" style="font-size:52px;color:#2563eb;font-weight:900">≤1500</div><div class="gd" style="font-size:44px;font-weight:700">1 片式</div></div><div class="gitem"><div class="gh" style="font-size:52px;color:#f97316;font-weight:900">≤3000</div><div class="gd" style="font-size:44px;font-weight:700">L 型</div></div><div class="gitem"><div class="gh" style="font-size:52px;color:#dc2626;font-weight:900">&gt;3000</div><div class="gd" style="font-size:44px;font-weight:700">4 片式</div></div></div></div>"""),
    ("s20", "dual",  (47, 50), """<div class="dual" id="s20d"><div class="dcard"><div class="dh" style="color:#2563eb">咬口管</div><div class="dd m">6 片 · 8 片都排过</div></div><div class="dcard"><div class="dh" style="color:#dc2626">焊接管</div><div class="dd m">最多 4 片</div><div class="dd" style="font-size:44px;color:#dc2626;font-weight:900">别按咬口习惯多排</div></div></div>"""),
    ("s21", "ccard", (51, 54), """<div class="ccard" id="s21c"><div class="ch">弯头两条硬规矩</div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">管高 &gt; 1400mm → 必须做<span class="hl">内菱角</span></div><div class="m" style="font-size:46px;font-weight:700">变径弯头内弧 → 不做<span class="hl">直角</span></div><div class="m">做了直角，焊缝应力集中，用久了开裂。</div></div></div>"""),
    ("s22", "ask",   (55, 59), """<div class="ask" id="s22a"><div class="aq">特殊件怎么做？<br><span class="hl">先下样品</span></div><div class="aa m" style="color:#475569">异形件 · 非标件，超过 3 件先做 1 件样品。</div><div class="aa m" style="color:#dc2626;font-weight:700;font-size:46px">确认合格，再批量</div></div>"""),
    ("s23", "bare",  (60, 60), """<div class="bare"><div class="bn" style="font-size:84px;color:#0f172a">小厂都不爱接</div><div class="bn" style="font-size:104px;color:#dc2626">焊接件的活</div><div class="bl" style="font-size:48px;color:#475569;font-weight:700">为什么？</div></div>"""),
    ("s24", "ccard", (61, 64), """<div class="ccard" id="s24c"><div class="ch">焊工<span class="accent">断层</span>是明摆着的</div><div class="glass"><div class="m">会氩弧焊的老师傅越来越少，年轻人不愿意干。</div><div class="m" style="font-size:48px;font-weight:700;color:#dc2626">好手一天工钱，顶排版半个月工资</div><div class="m">小厂养不起。</div></div></div>"""),
    ("s25", "dual",  (65, 68), """<div class="dual" id="s25d"><div class="dcard"><div class="dh" style="color:#2563eb">咬口错了</div><div class="dd m">重咬一枪就行</div></div><div class="dcard"><div class="dh" style="color:#dc2626">焊接错了</div><div class="dd m">补焊疤 · 报废板</div><div class="dd" style="font-size:44px;color:#dc2626;font-weight:900">返工成本大得多</div></div></div>"""),
    ("s26", "tale",  (69, 72), """<div class="tale" id="s26t"><div class="glass"><div class="tt">我们的办法<span class="accent">就一条</span></div><div class="ts m">把规矩写进手册。</div><div class="ts m" style="color:#2563eb;font-weight:700;font-size:48px">新人照着排，也能排对。</div></div></div>"""),
    ("s27", "ccard", (73, 76), """<div class="ccard" id="s27c"><div class="ch">现在</div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">周师傅那批管，换成了 <span style="color:#2563eb">1.0</span> 的板</div><div class="m">焊得顺，质检也过了。</div><div class="m" style="font-size:46px;font-weight:700;color:#dc2626">0.75 的板，系统里直接标红</div></div></div>"""),
    ("s28", "bare",  (77, 79), """<div class="bare"><div class="bn" style="font-size:92px;color:#0f172a">板子厚一档</div><div class="bn" style="font-size:116px;color:#2563eb">心里踏实一截</div><div class="bl" style="font-size:44px;color:#f97316;font-weight:700">规矩不是添堵，是让焊工少较劲</div></div>"""),
]

# 视觉多样性检查：≥3 连续 beat 不重复容器
types = [s[1] for s in scenes]
for i in range(len(types)):
    if i+2 < len(types) and types[i] == types[i+1] == types[i+2]:
        print("⚠️ 3连重复容器:", scenes[i][0], types[i])
print("容器序列:", " ".join(types))

def scene_window(sc):
    sid, typ, br, _ = sc
    if br[0] is None:
        return (0.3, 2.8)
    return (beats[br[0]][0], beats[br[1]][1] + 0.6)

windows = [scene_window(s) for s in scenes]
ins = []
prev_out = -10
for i, (s, w) in enumerate(zip(scenes, windows)):
    w0, w1 = w
    if i == 0:
        ins.append(0.3)
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
.btitle{{font-size:60px;font-weight:900;color:#0f172a;text-align:center;margin-bottom:28px;opacity:0}}
.btitle .accent{{color:#2563eb}}
.brand{{position:absolute;bottom:40px;right:80px;text-align:right;opacity:.7}}
.brand .bn{{font-size:28px;color:#64748b;font-weight:600}}
.brand .bu{{font-size:24px;color:#2563eb;margin-top:4px}}
.warn{{text-align:center;opacity:0}}
.warn .wl{{display:inline-block;background:#dc2626;color:#fff;font-size:34px;font-weight:700;padding:10px 28px;border-radius:10px;margin-bottom:18px}}
.warn .wm{{font-size:88px;font-weight:900;color:#0f172a;line-height:1.3}}
.warn .wm .hl{{color:#dc2626}}
.warn .ws{{font-size:44px;color:#64748b;margin-top:12px}}
.split{{display:flex;gap:50px;align-items:center;width:88%;opacity:0}}
.split .left{{flex:1;text-align:left}}
.split .right{{flex:1.2;text-align:left}}
.split .lt{{font-size:64px;font-weight:900;color:#0f172a;line-height:1.2}}
.split .lt .accent{{color:#2563eb}}
.split .rm{{font-size:42px;color:#1e293b;line-height:1.7;margin-bottom:8px}}
.grid3{{display:flex;gap:28px;width:88%;opacity:0}}
.gitem{{flex:1;background:rgba(255,255,255,.22);backdrop-filter:blur(20px) saturate(180%);border-radius:22px;padding:30px 26px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.05)}}
.gitem .gh{{font-size:42px;font-weight:700;color:#1e293b;margin-bottom:10px}}
.gitem .gd{{font-size:40px;color:#475569;line-height:1.6}}
.bare{{text-align:center;opacity:0}}
.bare .bn{{font-size:110px;font-weight:900;color:#2563eb;line-height:1.1}}
.bare .bl{{font-size:36px;color:#64748b;margin-top:6px}}
.dual{{display:flex;gap:40px;width:88%;opacity:0}}
.dcard{{flex:1;background:rgba(255,255,255,.22);backdrop-filter:blur(20px) saturate(180%);border-radius:22px;padding:32px 36px;box-shadow:0 8px 32px rgba(0,0,0,.05)}}
.dcard .dh{{font-size:46px;font-weight:700;color:#0f172a;margin-bottom:16px}}
.dcard .dd{{font-size:40px;color:#475569;line-height:1.6}}
.ask{{text-align:center;opacity:0}}
.ask .aq{{font-size:88px;font-weight:900;color:#0f172a;line-height:1.3}}
.ask .aq .hl{{color:#dc2626}}
.ask .aa{{font-size:46px;color:#64748b;margin-top:16px}}
.tale{{text-align:center;opacity:0;width:75%}}
.tale .glass{{padding:44px 60px}}
.tale .tt{{font-size:64px;font-weight:900;color:#0f172a;line-height:1.3;margin-bottom:14px}}
.tale .tt .accent{{color:#f97316}}
.tale .ts{{font-size:44px;color:#475569;line-height:1.7}}
.ccard{{text-align:center;opacity:0;width:88%}}
.ccard .ch{{font-size:64px;font-weight:900;color:#0f172a;margin-bottom:24px}}
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

with open(r"G:\blog\公众号分发\60-焊接\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html 已生成, duration =", duration)

# -*- coding: utf-8 -*-
"""61-强条 视频 HTML 生成器：VTT beat 时间轴 + 场景 Storyboard → index.html（横屏 1920x1080）"""
import re

def ts(s):
    h, m, rest = s.split(":")
    sec = int(h)*3600 + int(m)*60 + float(rest.replace(",", "."))
    return round(sec, 3)

raw_vtt = open(r"G:\blog\公众号分发\61-强条\narration.vtt", encoding="utf-8").read()
beats = []
for block in re.findall(r"\d+\n([\d:,\\.]+) --> ([\d:,\\.]+)\n(.+)", raw_vtt):
    s, e, t = block
    beats.append((ts(s), ts(e), t.strip()))

print("beats:", len(beats), "总时长:", round(beats[-1][1], 1))

# 场景: (id, 容器类型, beat区间, HTML) —— 横屏版式：A居中大字/B左文右数/C上下分栏/D三列并列/E双栏对比/G全屏警示/H图文
scenes = [
    ("s00", "bare",  (None, None), """<div class="bare"><div class="bn" style="font-size:110px;color:#dc2626">10 条强条</div><div class="bn" style="font-size:92px;color:#0f172a">车间师傅一条都背不出来</div><div class="bl" style="font-size:46px;color:#f97316;font-weight:700">GB50243 强制性条文 · 我们厂怎么落地</div></div>"""),
    ("s01", "tale",  (0, 1), """<div class="tale" id="s01t"><div class="glass"><div class="tt">排烟项目<span class="accent">被监理叫停</span></div><div class="ts m">风管穿防火墙的地方，没做防护套管。</div></div></div>"""),
    ("s02", "warn",  (2, 2), """<div class="warn" id="s02w"><div class="wl">问题</div><div class="wm">镀锌管<br><span class="hl">直接穿墙</span></div><div class="ws m">缝里塞的还是泡沫。</div></div>"""),
    ("s03", "ask",   (3, 5), """<div class="ask" id="s03a"><div class="aq">穿个墙而已，<br><span class="hl">至于吗？</span></div><div class="aa m" style="color:#475569">老赵：我干这行八年，头回听说穿墙要包铁皮。</div></div>"""),
    ("s04", "ccard", (6, 8), """<div class="ccard" id="s04c"><div class="ch">老赵<span class="accent">不冤，也不对</span></div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">从来没人告诉过他这条规矩</div><div class="m">可这条规矩写的是 <span style="color:#dc2626;font-weight:900;font-size:52px">"必须"</span> 两个字</div></div></div>"""),
    ("s05", "warn",  (9, 10), """<div class="warn" id="s05w"><div class="wl">GB50243-2016</div><div class="wm">强制性<br><span class="hl">条文</span></div><div class="ws m">违反了，不是质量问题，是违规问题。</div></div>"""),
    ("s06", "tale",  (11, 12), """<div class="tale" id="s06t"><div class="glass"><div class="tt">十条强条<span class="accent">抄出来看半宿</span></div><div class="ts m">越看越冒汗。</div><div class="ts m" style="color:#dc2626;font-weight:700;font-size:46px">跟风管有关的五条，一条都没在执行。</div></div></div>"""),
    ("s07", "bare",  (13, 13), """<div class="bare"><div class="bn" style="font-size:92px;color:#0f172a">先说强条</div><div class="bn" style="font-size:118px;color:#2563eb">是什么</div><div class="bl" style="font-size:44px;color:#64748b;font-weight:600">十条黑体字，必须严格执行</div></div>"""),
    ("s08", "ccard", (14, 15), """<div class="ccard" id="s08c"><div class="ch">通风与空调工程<br><span class="accent">施工质量验收规范</span></div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">十条黑体字条文</div><div class="m">就叫 <span style="color:#dc2626;font-weight:900;font-size:50px">强制性条文</span></div></div></div>"""),
    ("s09", "ask",   (16, 17), """<div class="ask" id="s09a"><div class="aq">黑体字不是<br><span class="hl">"这条重要，请重视"</span></div><div class="aa m" style="color:#2563eb;font-weight:700;font-size:52px">是"必须严格执行"，没得商量。</div></div>"""),
    ("s10", "bare",  (18, 18), """<div class="bare"><div class="bn" style="font-size:84px;color:#0f172a">跟风管厂直接相关的</div><div class="bn" style="font-size:116px;color:#f97316">头五条</div><div class="bl" style="font-size:44px;color:#475569;font-weight:600">一条一条说清楚</div></div>"""),
    ("s11", "dual",  (19, 20), """<div class="dual" id="s11d"><div class="dcard"><div class="dh" style="color:#dc2626">4.2.2</div><div class="dd" style="font-size:52px;font-weight:900;margin:10px 0">防火风管</div><div class="dd m">从里到外，必须是不燃材料</div></div><div class="dcard"><div class="dh" style="color:#2563eb">4.2.5</div><div class="dd" style="font-size:52px;font-weight:900;margin:10px 0">复合风管</div><div class="dd m">覆面和夹芯，都不能烧</div></div></div>"""),
    ("s12", "ccard", (21, 21), """<div class="ccard" id="s12c"><div class="ch">5.2.7 <span class="accent">柔性短管</span></div><div class="glass"><div class="m" style="font-size:46px;font-weight:700">防排烟系统的软连接</div><div class="m">必须采用 <span style="color:#dc2626;font-weight:900;font-size:52px">不燃材料</span></div></div></div>"""),
    ("s13", "warn",  (22, 22), """<div class="warn" id="s13w"><div class="wl">6.2.2 穿墙红线</div><div class="wm">1.6mm<br><span class="hl">钢制防护套管</span></div><div class="ws m">穿越防火防爆墙，用矿棉封堵，不能塞泡沫。</div></div>"""),
    ("s14", "ccard", (23, 23), """<div class="ccard" id="s14c"><div class="ch">6.2.3 <span class="accent">安装安全</span></div><div class="glass"><div class="m" style="font-size:44px;font-weight:700">风管内严禁走别的管线</div><div class="m" style="font-size:44px;font-weight:700">易燃易爆环境要接地</div><div class="m" style="font-size:44px;font-weight:700">拉索不能搭避雷针</div></div></div>"""),
    ("s15", "warn",  (24, 25), """<div class="warn" id="s15w"><div class="wl">老赵撞上的</div><div class="wm">就是<br><span class="hl">第四条</span></div><div class="ws m">返工那天，我坐在车间想了很久。</div></div>"""),
    ("s16", "tale",  (26, 28), """<div class="tale" id="s16t"><div class="glass"><div class="tt">老赵<span class="accent">不是懒人</span></div><div class="ts m">他焊的焊缝，是我见过最齐整的。</div><div class="ts m" style="color:#f97316;font-weight:700;font-size:44px">问题出在哪？三层。</div></div></div>"""),
    ("s17", "dual",  (29, 30), """<div class="dual" id="s17d"><div class="dcard"><div class="dh" style="color:#64748b">规范说</div><div class="dd" style="font-size:44px;font-weight:700;margin:10px 0">不燃柔性材料<br>封堵严密</div><div class="dd m">师傅脑子里没有对应物</div></div><div class="dcard"><div class="dh" style="color:#2563eb">车间说</div><div class="dd" style="font-size:44px;font-weight:700;margin:10px 0">矿棉塞紧塞满<br>不能留缝</div><div class="dd m">他立刻就懂</div></div></div>"""),
    ("s18", "ccard", (31, 32), """<div class="ccard" id="s18c"><div class="ch">第二层<span class="accent">责任没落工序</span></div><div class="glass"><div class="m">排版、下料、出厂检查</div><div class="m" style="font-size:46px;font-weight:700">没有一个环节问过：这条管穿不穿墙</div></div></div>"""),
    ("s19", "warn",  (33, 33), """<div class="warn" id="s19w"><div class="wl">第三层</div><div class="wm">验收前才<br><span class="hl">翻规范</span></div><div class="ws m">临时抱佛脚，抱出来的多半是错的。</div></div>"""),
    ("s20", "bare",  (34, 34), """<div class="bare"><div class="bn" style="font-size:88px;color:#0f172a">我们的做法</div><div class="bn" style="font-size:100px;color:#2563eb">翻译成车间动作</div><div class="bl" style="font-size:44px;color:#f97316;font-weight:700">三个卡点，嵌进流程</div></div>"""),
    ("s21", "ask",   (35, 36), """<div class="ask" id="s21a"><div class="aq">排版时先问<br><span class="hl">什么墙</span></div><div class="aa m" style="color:#475569">防火防爆墙？</div><div class="aa m" style="color:#2563eb;font-weight:700;font-size:48px">料单自动带出防护套管</div></div>"""),
    ("s22", "ccard", (37, 37), """<div class="ccard" id="s22c"><div class="ch">出厂检查<span class="accent">加一栏</span></div><div class="glass"><div class="m" style="font-size:44px">排烟软接头：</div><div class="m" style="font-size:50px;font-weight:900;color:#dc2626">必须是不燃织物</div><div class="m">PVC 软接头，直接打回。</div></div></div>"""),
    ("s23", "dual",  (38, 39), """<div class="dual" id="s23d"><div class="dcard"><div class="dh" style="color:#2563eb">安装交底</div><div class="dd" style="font-size:44px;font-weight:700;margin:10px 0">巴掌大的卡<br>贴在工具车上</div></div><div class="dcard"><div class="dh" style="color:#dc2626">天天看</div><div class="dd" style="font-size:56px;font-weight:900;margin:10px 0">就记住了</div></div></div>"""),
    ("s24", "tale",  (40, 40), """<div class="tale" id="s24t"><div class="glass"><div class="tt">想明白一个<span class="accent">道理</span></div><div class="ts m">强条落不了地，根子不在工人，在管理。</div></div></div>"""),
    ("s25", "warn",  (41, 42), """<div class="warn" id="s25w"><div class="wl">关键</div><div class="wm">工人其实<br><span class="hl">都讲规矩</span></div><div class="ws m">问题是没人用他听得懂的话，把规矩讲给他听。</div></div>"""),
    ("s26", "dual",  (43, 44), """<div class="dual" id="s26d"><div class="dcard"><div class="dh" style="color:#dc2626">等监理来上课</div><div class="dd m">被动挨查</div></div><div class="dcard"><div class="dh" style="color:#2563eb">自己先备课</div><div class="dd m">一张对照表</div><div class="dd" style="font-size:44px;font-weight:900;color:#16a34a">少返工 · 不违规</div></div></div>"""),
    ("s27", "tale",  (45, 46), """<div class="tale" id="s27t"><div class="glass"><div class="tt">上礼拜工地<span class="accent">遇见老赵</span></div><div class="ts m">"这墙我看是防火墙，防护套管我带了两根过来。"</div></div></div>"""),
    ("s28", "bare",  (47, 47), """<div class="bare"><div class="bn" style="font-size:84px;color:#0f172a">记不住条文号</div><div class="bn" style="font-size:100px;color:#2563eb">记住了穿墙先问什么墙</div><div class="bl" style="font-size:44px;color:#f97316;font-weight:700">强条落地，落到这一步，就算成了。</div></div>"""),
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

with open(r"G:\blog\公众号分发\61-强条\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html 已生成, duration =", duration)

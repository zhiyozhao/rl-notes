#!/usr/bin/env python3
"""把 _content.html 里的章节合并成单页滚动文档 index.html"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "_content.html").read_text(encoding="utf-8")

secs = []
for m in re.finditer(r"<!--S:([^|]+)\|([^\n]*?)-->\n(.*?)\n<!--/S-->", src, re.S):
    secs.append({"id": m.group(1).strip(), "title": m.group(2).strip(), "body": m.group(3)})

TITLES = {
 "1":"记号表","2":"MDP","3":"Bellman 方程","4":"策略改进","5":"POMDP 与信念",
 "6":"蒙特卡洛","7":"TD(0)","8":"n 步与 TD(λ)","9":"致命三角","10":"动态规划",
 "11":"无模型控制","12":"Double Q","13":"策略梯度","14":"Actor-Critic","15":"探索",
 "16":"Dyna 与规划","17":"MCTS 与 MuZero","18":"Dreamer","19":"四条轴",
 "20":"五个根本难题","21":"实务必踩的坑","A":"公式卡","B":"数学准备","C":"术语表",
}
ORDER = [str(i) for i in range(1,22)] + ["A","B","C"]
GROUPS = [
 ("I · 形式化", ["2","3","4","5"]),
 ("II · 估计", ["6","7","8","9"]),
 ("III · 控制", ["10","11","12","13","14"]),
 ("IV · 探索与模型", ["15","16","17","18"]),
 ("V · 收束", ["19","20","21"]),
 ("附录", ["A","B","C"]),
]

by_id = {s["id"]: s for s in secs}
missing = [i for i in ORDER if i not in by_id]
assert not missing, f"missing sections: {missing}"

def link(i):
    return (f'<a href="#s{i}"><span class="n">{i}</span>'
            f'<span class="t">{TITLES[i]}</span></a>')

nav = [link("1")]
for g, ids in GROUPS:
    nav.append(f'<div class="grp">{g}</div>')
    nav.extend(link(i) for i in ids)
sidebar = "\n    ".join(nav)

parts = []
for i in ORDER:
    s = by_id[i]
    parts.append(
        f'<section class="chap" id="s{i}">\n'
        f'<h2><span class="num">{i}</span>{TITLES[i]}</h2>\n'
        f'{s["body"]}\n</section>'
    )
body = "\n\n".join(parts)

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>强化学习专项 · 原理、公式与算法全景</title>
<script>
(function(){
  var t;
  try { t = localStorage.getItem('rl-theme'); } catch(e){}
  if (!t) t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
})();
</script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<link rel="stylesheet" href="assets/style.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body id="top">
<div id="progress"></div>
<div class="layout">

<aside>
  <div class="brand">强化学习专项<small>原理 · 公式 · 算法全景</small></div>
  <button id="themeBtn" class="theme-btn" type="button" title="切换明暗主题" aria-label="切换明暗主题">
    <svg class="i-moon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    <svg class="i-sun" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.2v2.2M12 19.6v2.2M2.2 12h2.2M19.6 12h2.2M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M19.1 4.9l-1.6 1.6M6.5 17.5l-1.6 1.6"/></svg>
  </button>
  <nav id="toc">
    __SIDEBAR__
  </nav>
</aside>

<main>
<p class="kicker">Reinforcement Learning</p>
<h1>强化学习：原理、公式与算法全景</h1>
<p class="sub">从 MDP 的形式化开始，到 TD(λ)、策略梯度、PPO、SAC、MCTS、Dreamer。
每个算法给出正确的数学形式、推导线索和它要解决的问题。最后用四条轴和五个根本难题把整个领域串起来。</p>
<div class="meta">
  <span class="chip">21 节 + 3 附录</span>
  <span class="chip">__NFORM__ 个公式</span>
  <span class="chip">单页滚动</span>
  <span class="chip">明暗双主题</span>
</div>
<div class="callout">
  <span class="label">怎么用</span>
  <p>左侧目录可直接跳转，滚动时自动高亮当前节；右上角图标切换明暗主题。</p>
  <p><strong>三条路线：</strong>看懂论文符号 → 1,2,3,6,7,8,19；能手推算法 → 全部，跳过 16–18；做工程实现 → 7,9,11,13,14,21。</p>
</div>

__BODY__

<footer>
  <p>强化学习专项 · 单页滚动版 · 与《世界模型地基》配套</p>
</footer>
</main>
</div>

<a id="toTop" href="#top" title="回到顶部" aria-label="回到顶部">↑</a>

<script>
(function(){
  /* ================= KaTeX ================= */
  function render(){
    if (typeof renderMathInElement !== 'function') return;
    renderMathInElement(document.body, {
      delimiters: [
        {left:'$$', right:'$$', display:true},
        {left:'$', right:'$', display:false}
      ],
      ignoredTags: ['script','noscript','style','textarea','pre','code','option'],
      throwOnError: false,
      strict: false
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();

  /* ================= 主题 ================= */
  var root = document.documentElement;
  var btnT = document.getElementById('themeBtn');
  function setTheme(t){
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('rl-theme', t); } catch(e){}
    if (btnT) btnT.setAttribute('aria-pressed', t === 'dark');
  }
  if (btnT){
    btnT.addEventListener('click', function(){
      setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  /* ================= 目录跳转 ================= */
  var links = [].slice.call(document.querySelectorAll('#toc a'));
  var byId = {};
  links.forEach(function(a){ byId[a.getAttribute('href').slice(1)] = a; });
  var secs = [].slice.call(document.querySelectorAll('section.chap'));
  var btn  = document.getElementById('toTop');
  var prog = document.getElementById('progress');

  var lockId = null;
  var unlockTimer = null;

  function setActive(id){
    for (var i = 0; i < links.length; i++) links[i].classList.remove('active');
    if (id && byId[id]) byId[id].classList.add('active');
  }

  function easeInOutCubic(t){
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  /* 距离越远，时间略长；始终平滑起步、平滑收尾 */
  function scrollToY(targetY){
    var startY = window.scrollY;
    var diff = targetY - startY;
    if (Math.abs(diff) < 2) return 0;
    var dur = Math.round(Math.max(420, Math.min(820, 320 + Math.sqrt(Math.abs(diff)) * 7.5)));
    var t0 = performance.now();
    function step(now){
      var p = Math.min(1, (now - t0) / dur);
      window.scrollTo(0, startY + diff * easeInOutCubic(p));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    return dur;
  }

  function jumpTo(id){
    var el = document.getElementById(id);
    if (!el) return;
    setActive(id);
    lockId = id;
    clearTimeout(unlockTimer);
    var dur = scrollToY(Math.max(0, el.offsetTop - 12));
    unlockTimer = setTimeout(function(){
      lockId = null;
      update(true);
    }, dur + 160);
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  }

  links.forEach(function(a){
    a.addEventListener('click', function(e){
      e.preventDefault();
      jumpTo(a.getAttribute('href').slice(1));
    });
  });

  if (btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      lockId = null;
      setActive(null);
      scrollToY(0);
      if (history.replaceState) history.replaceState(null, '', '#top');
    });
  }

  function update(force){
    if (force || !lockId){
      var y = window.scrollY + 140;
      var cur = secs[0];
      for (var i = 0; i < secs.length; i++){
        if (secs[i].offsetTop <= y) cur = secs[i]; else break;
      }
      if (cur) setActive(cur.id);
    }
    if (btn) btn.classList.toggle('show', window.scrollY > 700);
    if (prog){
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function(){
    if (!ticking){
      ticking = true;
      requestAnimationFrame(function(){ ticking = false; update(false); });
    }
  }, {passive:true});
  window.addEventListener('resize', function(){ update(true); });

  if (location.hash && document.getElementById(location.hash.slice(1))){
    setActive(location.hash.slice(1));
  }
  update(true);
})();
</script>
</body>
</html>
"""

tmp = body.replace('$$', '\x00')
n_disp = tmp.count('\x00') // 2
n_inl  = len(re.findall(r'\$[^$\n]+\$', tmp))
nform  = n_disp + n_inl

html = (HEAD.replace("__SIDEBAR__", sidebar)
            .replace("__BODY__", body)
            .replace("__NFORM__", str(nform)))
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("sections:", len(secs), "| formulas:", nform, "| chars:", len(html))

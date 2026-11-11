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
  <nav id="toc">
    __SIDEBAR__
  </nav>
</aside>

<main>
<p class="kicker">Reinforcement Learning</p>
<h1>强化学习：原理、公式与算法全景</h1>
<p class="sub">从 MDP 的形式化开始，到 TD(λ)、策略梯度、PPO、SAC、MCTS、Dreamer。
每个算法给出正确的数学形式、推导线索和它要解决的问题。最后用四条轴和五个根本难题把整个领域串起来。</p>
<div class="callout">
  <span class="label">怎么用</span>
  <p>单页滚动，左侧目录可直接跳转，滚动时自动高亮当前节。公式用 KaTeX 渲染（首次打开需联网）。</p>
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
  /* ---------- KaTeX ---------- */
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

  /* ---------- 目录跳转 ---------- */
  var links = [].slice.call(document.querySelectorAll('#toc a'));
  var byId = {};
  links.forEach(function(a){ byId[a.getAttribute('href').slice(1)] = a; });
  var secs = [].slice.call(document.querySelectorAll('section.chap'));
  var btn  = document.getElementById('toTop');
  var prog = document.getElementById('progress');

  var lockId = null;      // 跳转期间锁定高亮，不让滚动监听改动
  var unlockTimer = null;

  function setActive(id){
    for (var i = 0; i < links.length; i++) links[i].classList.remove('active');
    if (id && byId[id]) byId[id].classList.add('active');
  }

  function easeInOutQuad(t){
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }

  function scrollToY(targetY, duration){
    var startY = window.scrollY;
    var diff = targetY - startY;
    if (Math.abs(diff) < 2){ window.scrollTo(0, targetY); return; }
    var t0 = performance.now();
    function step(now){
      var p = Math.min(1, (now - t0) / duration);
      window.scrollTo(0, startY + diff * easeInOutQuad(p));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function jumpTo(id){
    var el = document.getElementById(id);
    if (!el) return;
    setActive(id);                       // 先立刻亮起目标项
    lockId = id;                          // 锁定
    clearTimeout(unlockTimer);
    unlockTimer = setTimeout(function(){
      lockId = null;
      update(true);
    }, 460);
    scrollToY(Math.max(0, el.offsetTop - 12), 300);
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
      scrollToY(0, 300);
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

html = HEAD.replace("__SIDEBAR__", sidebar).replace("__BODY__", body)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("sections:", len(secs), "| chars:", len(html))

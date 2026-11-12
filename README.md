# 强化学习专项

单页滚动的强化学习教程：MDP → TD(λ) → 策略梯度 → PPO/SAC → MCTS/MuZero/Dreamer。

## 打开方式

```bash
open ~/Desktop/Learn/强化学习/index.html
```

左侧目录可直接跳转，滚动时自动高亮当前节。

- **桌面**：左侧固定目录
- **手机**：左上角 ☰ 打开抽屉式目录（点遮罩 / × / 点条目 / Esc 关闭）
- **主题**：右上角图标切换明暗，记住选择

## 目录结构

```
强化学习/
├── index.html       全部内容（单页，约 75 KB）
├── assets/
│   └── style.css    样式（深色模式 + 打印）
├── _content.html    章节源文件（带 <!--S:id|标题--> 标记）
├── build.py         合并生成 index.html
└── README.md
```

## 修改

**改正文或公式**：两种方式都行。

1. 直接改 `index.html`（快，但下次 build 会被覆盖）
2. 改 `_content.html` 里对应的 `<section>`，然后：

```bash
cd ~/Desktop/Learn/强化学习
python3 build.py
```

推荐第 2 种，源文件干净。

## 公式

KaTeX 从 CDN 加载，页面里是普通源码：

```html
$G_t = r_t + \gamma G_{t+1}$
$$V^\pi(s)=\sum_a \pi(a|s)\left[R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\pi(s')\right]$$
```

首次打开需联网。要彻底离线，把 KaTeX 下载到 `assets/katex/` 并改掉 `<link>` / `<script>` 的路径即可。

## 结构

| 范围 | 内容 |
|---|---|
| 1 | 记号表 |
| 2–5 | 形式化：MDP、Bellman、策略改进、POMDP |
| 6–9 | 估计：MC、TD(0)、n 步与 TD(λ)、致命三角 |
| 10–14 | 控制：DP、SARSA/Q-learning、Double Q、策略梯度、AC/PPO/SAC |
| 15–18 | 探索与模型：遗憾、Dyna/MPC、MCTS/MuZero、Dreamer |
| 19–21 | 收束：四条轴、五个根本难题、实践坑 |
| A–C | 公式卡、数学准备、术语表 |

## 配套

同目录外还有《世界模型地基手册》。两者符号约定一致：$(s_t,a_t,r_t,s_{t+1})$。

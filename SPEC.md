# FClassPal 主题包规范 · spec 1

FClassPal 的应用本体只带五套内置皮肤（液态玻璃 / MD3 / Fluent / MIUI / 鸿蒙）。
其余主题一律以**主题包（`.fcpt`）**的形式分发：一个 zip，导入后立刻生效，删掉就干净消失。
本文是这个包格式的唯一规范，同时说明「一套主题能改到什么程度」。

- 规范版本：`spec 1`（对应 FClassPal 2.5.0 起）
- 参考实现：本仓库 `themes/` 下 13 套主题，全部符合本规范
- 最小示例：`examples/minimal/`（只有两个文件，可直接改）

---

## 1. 包结构

一个 `.fcpt` 就是一个普通 zip。**zip 根目录直接放文件**，不要再套一层目录。

```
kitty.fcpt  （zip，扩展名改成 .fcpt）
├── manifest.json        必需 · 元数据
├── theme.css            必需 · 全套样式
├── assets/              可选 · 素材（PNG/JPG/SVG/WebP）
│   ├── kitty-head.png
│   └── …
├── preview.png          可选 · 预览图（仓库展示用，安装不校验）
└── README.txt           可选 · 给人看的说明
```

解压开是这样的目录（安装后本体把它放到 `主题目录/<id>/`）：

```
themes/kitty/
├── manifest.json
├── theme.css
└── assets/
```

> 大小上限 24 MB，条目上限 400 个。条目名不许出现绝对路径、盘符或 `..`，
> 否则整包被拒（并且不会在磁盘上留下任何残留）。

---

## 2. manifest.json

```json
{
  "spec": 1,
  "id": "my-theme",
  "name": "我的主题",
  "version": "1.0.0",
  "author": "你的名字",
  "description": "一句话说明这套主题长什么样。",
  "accent": "#5B7CFA",
  "accentSecondary": "#A8B8FF",
  "fixedPalette": true,
  "minApp": "2.5.0",
  "preview": "preview.png",
  "license": "CC BY-NC-SA 4.0"
}
```

| 字段 | 类型 | 必填 | 说明与校验 |
| --- | --- | --- | --- |
| `spec` | int | 否 | 包规范版本，当前固定 `1`。缺省按 1 处理。 |
| `id` | string | **是** | 主题唯一标识。只允许 `^[a-zA-Z][a-zA-Z0-9-]{1,23}$`（字母开头，2–24 位，大小写敏感——内置 id 的大写变体也不许占用，例如 `NaiWa`）。**不能**占用内置 id：`glass` / `md3` / `fluent` / `miuix` / `harmony`。 |
| `name` | string | 否 | 界面显示名，最长 40 字符。缺省用 `id`。 |
| `version` | string | 否 | 主题自身版本，最长 20 字符。缺省 `1.0.0`。 |
| `author` | string | 否 | 作者，最长 40 字符。缺省「未署名」。 |
| `description` | string | 否 | 一句话简介，最长 200 字符。也可写 `desc`。 |
| `accent` | string | 否 | 推荐主色，必须 `#RRGGBB`。用在主题列表色点和「手动指定取色」的起点。**格式不对会被丢弃**，界面回退到基线紫。 |
| `accentSecondary` | string | 否 | 次色，仅供展示，不参与渲染。 |
| `fixedPalette` | bool | 否 | `true`（缺省）= 固定配色，设置里会隐藏取色面板；`false` = 跟随壁纸取色（见 §5.3）。 |
| `minApp` | string | 否 | 需要的最低本体版本，例如 `2.5.0`。仅作提示，不拦截安装。 |
| `preview` | string | 否 | 预览图文件名，仓库/商店展示用。 |
| `license` | string | 否 | 素材与样式授权。**用同人素材请务必写明限个人非商业使用。** |

`id` 的取值决定了 `theme.css` 里所有选择器的前缀，两处必须一致。

---

## 3. theme.css 铁律

这七条不是风格建议，是会导致「装上去整个界面坏掉」的硬约束。

### 3.1 每条选择器都以 `body.theme-<id>` 开头

```css
/* 对 */
body.my-theme .item { … }
body.my-theme .titlebar::after { … }

/* 错：裸类名会糊死所有主题（包括内置五套） */
.item { … }
```

安装时会检查 `theme.css` 里至少出现一次 `body.theme-<id>`，没有就拒绝安装。

前缀必须整体带上，不能写成 `body.my-theme` 之外的形式；多条选择器共用一段声明时：

```css
body.my-theme .item,
body.my-theme .usb-item { … }
```

### 3.2 `--t-veil` 必须和 `background` 同一条规则

面纱透明度 `--glass-alpha` 是运行时写在 `#widget` 上的，`body` 那一层取不到它。
若把 `--t-veil` 放进 `body.my-theme { … }` 的 token 块，`var()` 替换失败会让整条
`background` 变成 invalid-at-computed-value-time —— 表现是**面纱整个消失，只剩一圈描边**。

```css
/* 对：两者同一条规则 */
body.my-theme .glass-veil {
  --t-veil: linear-gradient(160deg,
              rgb(255 255 255 / calc(0.84 + 0.16 * var(--glass-alpha))) 0%,
              rgb(244 246 255 / calc(0.72 + 0.28 * var(--glass-alpha))) 100%);
  background: var(--t-veil);
}

/* 错 */
body.my-theme { --t-veil: …; }
body.my-theme .glass-veil { background: var(--t-veil); }
```

### 3.3 不要改定位元素的 `position`

`.ctx-menu` 是 `fixed`，`.panel` 是 `absolute`。主题里出现 `position: relative`
会让菜单/面板跑出窗口。要调位置就用 `top / inset / margin`，不要换定位方式。

### 3.4 素材只写 `url("assets/xxx.png")`

```css
body.my-theme .titlebar::after { background-image: url("assets/head.png"); }
```

导入后本体把这类相对路径改写成绝对 `file:///` 路径（渲染层是注入 `<style>`，
相对路径会按 `index.html` 解析，写死了会 404）。素材缺失时该 `url()` 会被替换成
`none` —— 不会崩，但也不会有图形，所以发布前自己确认文件都在。

### 3.5 `@keyframes` 名字带自己的 id 前缀

```css
@keyframes t-in-my-theme { … }   /* 对 */
@keyframes slide-in { … }        /* 错：可能和别人撞 */
```

### 3.6 不用 emoji

界面源码有 emoji 检查，主题包同样不引入 emoji。要图形就用 `assets/` 里的 PNG
或内联 SVG data-URL（`url("data:image/svg+xml,…")`）。

### 3.7 `var()` 取不到值会整条声明作废

写 `backdrop-filter: var(--t-blur)` 之前确保 `--t-blur` 真的在祖先上有定义。
同理：`drop-shadow()` 没有 `spread` 参数；`backdrop-filter` 里不允许 `url(#…)`。

---

## 4. 可以改什么

### 4.1 设计 token（推荐从这里入手）

整包定义在 `body.theme-<id> { … }` 的 token 块里，改一处，全套表面跟着变。

| 变量 | 作用 | 示例 |
| --- | --- | --- |
| `--t-r-win` | 窗口圆角 | `28px` |
| `--t-r-card` | 卡片 / 列表项圆角 | `24px` |
| `--t-r-ctl` | 控件圆角 | `18px` |
| `--t-r-small` | 小圆角（输入框内部等） | `14px` |
| `--t-btn-r` | 按钮圆角（`999px` = 胶囊） | `999px` |
| `--t-blur` | 玻璃模糊 | `blur(18px) saturate(140%)` |
| `--t-surface` / `-2` / `-3` | 三级表面色（越靠后越实） | `rgb(255 250 252 / 0.82)` |
| `--t-accent` | 强调色 | `#E8548A` |
| `--t-on-accent` | 强调色上的文字色 | `#FFFFFF` |
| `--t-accent-c` / `--t-on-accent-c` | 强调色 + 文字色的「三元组」形式，供 `rgb(R G B / A)` 使用 | `232 84 138` |
| `--t-line` | 分隔线 | `rgb(232 84 138 / 0.16)` |
| `--t-veil-border` | 面纱描边 | `rgb(255 255 255 / 0.65)` |
| `--t-veil-shadow` | 面纱投影 | `0 10px 30px rgb(232 84 138 / 0.18)` |
| `--t-shadow-hover` | 悬停投影 | `0 8px 20px rgb(232 84 138 / 0.22)` |
| `--t-shadow-menu` | 菜单投影 | `0 12px 32px rgb(120 60 90 / 0.24)` |
| `--t-ease` / `--t-ease-in` | 缓动曲线 | `cubic-bezier(0.2, 0, 0, 1)` |
| `--t-dur` / `--t-dur-mid` | 动画时长 | `260ms` / `160ms` |
| `--t-stagger` | 列表错峰步长 | `40ms` |
| `--t-fw-title` / `--t-fw-name` / `--t-fw-btn` | 三级字重 | `600` / `500` / `600` |

### 4.2 表面与结构钩子

| 部件 | 选择器 |
| --- | --- |
| 窗口 | `.widget`、`.glass-warp`（折射/滤镜层）、`.glass-veil`（面纱）、`.sheen`（光斑） |
| 标题栏 | `.titlebar`、`.title-icon`、`.title-input`、`.tb-btn` |
| 列表项 | `.item`、`.item-icon`、`.item-name`、`.item:active`、`.item:hover` |
| U 盘区 | `.usb-section`、`.usb-item`、`.usb-icon`、`.usb-hint`、`.usb-btn`（含 `.primary`） |
| 设置面板 | `.panel`、`.row`、`.group-title`、`.field`、`.size-controls`、`.theme-select` |
| 右键菜单 | `.ctx-menu`、`.ctx-item`、`.ctx-danger` |
| 弹窗 | `.modal-card`、`.modal-footer` |
| 按钮 | `.primary-btn`、`.ghost-btn`、`.danger-btn`、`.pick-btn`、`.text-btn`、`.seg-btn`、`.btn-row` |
| 反馈 | `.toast`、`.ripple`、`.t-enter`（列表入场，配合 `--i` 与 `--t-stagger`） |
| 装饰位 | 上述元素的 `::before` / `::after` —— 13 套主题的贴纸全部挂在这里 |

> `.size-controls` 是**固定 30×30 的方形图标按钮容器**。别往里塞文字按钮，
> 塞了会被压成 30px、文字溢出到盒外，溢出的部分不在点击区内 —— 表现为「按钮完全没反应」。
> 文字按钮请放 `.btn-row` 并加 `class="text-btn"`。

### 4.3 body 状态类（条件样式）

选择器里可以叠加这些状态，做「只在某状态下」的样式：

| 状态类 | 含义 |
| --- | --- |
| `body.dark` | 系统/配置处于深色模式 |
| `body.dyn` | 当前是动态配色主题（跟随壁纸取色） |
| `body.over-light` | 底材偏亮（玻璃主题会提高模糊并压一层薄墨） |
| `body.locked` | 位置锁定 |
| `body.is-moving` | 正在拖动（折射被摘掉的窗口） |
| `body.is-resizing` | 正在调整尺寸 |
| `body.item-dragging` | 正在拖动列表项 |
| `body.edit-mode` | 编辑模式 |
| `body.lg-ready` | 液态玻璃滤镜已就绪 |
| `body.bg-custom` | 用了自定义背景图 |
| `body.ic-ring` / `ic-mono` / `ic-contain` / `ic-none` / `ic-shape` | 图标外观档位 |
| `body.mobile` | 运行在安卓壳里（桌面专属行会被 `data-mobile-hide` 藏掉） |
| `body.preview` | 浏览器预览模式（没有主进程） |

用法示例：

```css
body.dark.my-theme .glass-veil { background: rgb(20 16 24 / calc(0.62 * var(--glass-alpha))); }
body.mobile.my-theme .size-controls { display: none; }
```

### 4.4 固定配色主题：还要覆盖 `--md3-*` 角色

界面大量使用 `--text: var(--md3-on-surface)`、`--accent: var(--md3-primary)` 这类重定向，
所以只改 `--t-accent` 不够 —— 壁纸一偏色，整套主题的颜色就跟着跑（Kitty 曾经因此「不粉了」）。
固定配色主题应当在 `body.theme-<id> { … }` 里把整套角色钉死：

```css
body.my-theme {
  --md3-primary: #5B7CFA;            --md3-primary-rgb: 91 124 250;
  --md3-primary-container: #DDE4FF;  --md3-primary-container-rgb: 221 228 255;
  --md3-on-primary: #FFFFFF;         --md3-on-primary-rgb: 255 255 255;
  --md3-secondary: #A8B8FF;          --md3-secondary-rgb: 168 184 255;
  --md3-tertiary: #7A9BFF;           --md3-tertiary-rgb: 122 155 255;
  --md3-surface: #F8F9FF;            --md3-surface-rgb: 248 249 255;
  --md3-surface-dim: #E6E9F5;
  --md3-surface-container: #EEF1FA;  --md3-surface-container-rgb: 238 241 250;
  --md3-on-surface: #1B1D22;         --md3-on-surface-rgb: 27 29 34;
  --md3-on-surface-variant: #5A5F6B; --md3-on-surface-variant-rgb: 90 95 107;
  --md3-outline: #C3C8D6;            --md3-outline-variant: #E2E6F0;
  --md3-error: #E57373;              --md3-error-rgb: 229 115 115;
  --md3-on-error: #FFFFFF;
  --danger: #E57373;                 /* 删除类按钮 —— 别用主色，要看得出来 */
}
```

每个角色建议同时给「字面值」和「`-rgb` 三元组」两份；界面里 `rgb(var(--md3-primary-rgb) / 0.12)`
这类写法只认后者。

### 4.5 跟随壁纸取色的主题

`manifest.fixedPalette: false` 时，`--md3-*` 由本体按壁纸（Monet）算出来写进 `document.body`，
主题**不要**再声明它们。这类主题只给 token 和表面规则，例如：

```css
body.my-dynamic-theme {
  --t-accent: var(--md3-primary);
  --t-r-card: 20px;
  --t-blur: blur(20px) saturate(140%);
}
```

深色模式也不需要自己算：本体在 `body.dark` 下给出另一套 `--md3-*`，
主题只需保证在自己的规则里引用变量而不是写死颜色。

---

## 5. 打包

### 5.1 手工打包

`manifest.json`、`theme.css` 必须位于 zip 根目录。

```bash
# macOS / Linux
cd my-theme && zip -r ../my-theme.fcpt manifest.json theme.css assets preview.png README.txt
```

```powershell
# Windows（先 cd 进去，保证根部就是这四个条目）
cd my-theme
Compress-Archive -Path manifest.json,theme.css,assets,preview.png,README.txt -DestinationPath ..\my-theme.fcpt
```

```python
# 跨平台、结果最可控
import zipfile, os
os.chdir('my-theme')
with zipfile.ZipFile('../my-theme.fcpt', 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk('.'):
        for f in sorted(files):
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, '.').replace('\\', '/'))
```

最后把扩展名改成 `.fcpt`（若压缩工具加了自己的后缀）。

### 5.2 发布前自检

1. zip 根部有 `manifest.json` 和 `theme.css`（不是套在 `my-theme/` 下）。
2. `theme.css` 里搜得到 `body.theme-<id>`，`<id>` 与 manifest 一致。
3. 花括号成对（`{` 数 = `}` 数），没有 `{{` 这类笔误。
4. **圆括号也要成对**（`(` 数 = `)` 数）—— 多一个或少一个都不是"只坏这一条声明"，
   渲染引擎会**从出错点把后面整份样式表丢掉**。本体的主题包是一个包一份样式表，
   坏包只坏自己；但你自己这份主题的**后半段会全部失效**，表现为"主题只生效了一半 /
   贴图消失"。2026-10 有 8 套官方主题栽在 `linear-gradient(` 少一个 `)` 上。
   数括号前先把注释和字符串剥掉，否则 `url("assets/x.png")` 会把人绕晕。
5. 每条规则的选择器都带 `body.theme-<id>` 前缀（`@keyframes` 内部的 `from`/`to`/百分比除外）。
6. `url("assets/…")` 引用的文件都在包里。
7. 没有裸 `.类名` 规则、没有 emoji、没有改 `position`。
8. `--t-veil` 与 `background: var(--t-veil)` 在同一条规则内。
9. 深浅色适配：token 块末尾追加一段 `body.theme-<id>.dark`（压暗 surface 族/文字/描边/面纱，强调色不动），否则暗色模式下包的浅色 token 会赢过本体的全局深色层（包 CSS 注入更靠后、同特异性树序赢）。参考各角色包 theme.css 末尾的「深色模式适配」段，或用本体 _rt/_darkify.py 生成。

### 5.3 安装

FClassPal → 右键 / 长按 → 设置 → 主题 → **导入主题包**，选 `.fcpt` 文件即可。
随本体发布的 13 套主题可以在同一个弹窗里**一键安装**（离线，不联网）。
删除也在那个弹窗里。内置五套皮肤不能被主题包覆盖或删除。

---

## 6. 示例

| 目录 | 说明 |
| --- | --- |
| `examples/minimal/` | 最小可用主题：只有 `manifest.json` + `theme.css`，无素材，用作起手模板 |
| `examples/sticker/` | 带素材与装饰位：演示 `url("assets/…")`、伪元素贴纸、`--t-veil` 的正确写法 |
| `themes/*` | 13 套完整主题，真实项目里的写法参考 |

自己改一套最快的路径：复制 `themes/kitty/` 改个 `id` 与配色，改完重新打包。

---

## 7. 兼容性

- `spec 1` 自 FClassPal 2.5.0 起支持。
- 本体会忽略它不认识的 manifest 字段（前向兼容），所以给新字段加注释说明是安全的。
- 主题包不执行任何代码 —— 只有 CSS 与图片，没有 JS 入口。

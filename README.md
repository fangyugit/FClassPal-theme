# FClassPal-theme

FClassPal（[fangyugit/FClassPal](https://github.com/fangyugit/FClassPal)）的**主题包仓库**。
应用本体只带五套内置皮肤（液态玻璃 / MD3 / Fluent / MIUI / 鸿蒙），这里的所有主题以
`.fcpt` 主题包形式独立分发 —— 装上生效、删掉干净、改两行就能变自己的样子。

- 包格式规范：[SPEC.md](SPEC.md)（`spec 1`，含字段表、CSS 铁律、可自定义清单）
- 起手示例：[examples/minimal/](examples/minimal/)（两个文件的最小主题）、[examples/sticker/](examples/sticker/)（带素材）

## 下载

两种方式拿到主题：

1. **Release（推荐）**：到 [Releases](../../releases) 页面下载 `*.fcpt`，然后在
   FClassPal → 右键 / 长按 → 设置 → 主题 → **导入主题包** 选择文件即可。
2. **随包附带**：FClassPal 2.5.0 安装包内已带全部 13 套（`themes/` 目录），
   主题管理弹窗里可以**一键离线安装**，不用联网。

也可以直接改：`.fcpt` 就是 zip，解压后 `theme.css` 是纯文本，改完重新打包即可。

## 主题一览（13 套）

| id | 名称 | 主色 | 素材 | 说明 |
| --- | --- | --- | --- | --- |
| kitty | Hello Kitty | `#C2185B` | 6 张 | 蝴蝶结与爱心、超圆角、粉白奶油配色 |
| dog | 玉桂狗 | `#4FA8E8` | 5 张 | 天空蓝：云朵与长耳朵，清爽的浅蓝白玻璃 |
| kuromi | 库洛米 | `#8E5BC8` | 6 张 | 紫色小恶魔：尖角兜帽与骷髅装饰，暗紫配色 |
| melody | 美乐蒂 | `#EC6FA8` | 4 张 | 粉兔：长耳朵与蝴蝶结，奶油粉白配色 |
| sanrio | 三丽鸥混合 | `#E8548A` | 9 张 | 四角色同框：Kitty 粉主色 / 库洛米紫次色 / 玉桂狗蓝点缀 |
| pochacco | 帕恰狗 | `#4D8FE0` | 6 张 | 运动蓝：圆润蓝色系，轻快的浅蓝白玻璃 |
| purin | 布丁狗 | `#D9962E` | 6 张 | 焦糖布丁配色，暖洋洋的奶油黄 |
| milk | 奶蛙 | `#C08552` | 6 张 | 奶蛙 meme：黄绿皮与呆滞大眼，奶茶色系 |
| tianyi | 洛天依 | `#2FA98C` | 6 张 | 灰发青衣的电子国风，青绿色系 |
| ling | 乐正绫 | `#D8433F` | 6 张 | 红发红瞳的热情系，正红与暖白 |
| miku | 初音未来 | `#1FB5AA` | 6 张 | 葱绿双马尾，清爽的薄荷青配色 |
| teto | 重音Teto | `#E0557F` | 6 张 | 粉色钻头双马尾，活泼的玫粉配色 |
| whale | DS鲸鱼娘 | `#3E6FD8` | 6 张 | DeepSeek 鲸鱼娘：海蓝与白色的科技感配色 |

每一套都是**完整的自足设计系统**（形状 / 模糊 / 表面 / 强调色 / 动效全套 token +
全部表面规则 + 贴纸装饰位），互相之间没有共底 —— 改一套不会牵动另一套。

## 高度自定义

`.fcpt` 是「CSS + 图片」的组合，能改到什么程度取决于你愿意写多少 CSS：

- **改色**：改 `body.theme-<id> { … }` token 块里的 `--t-accent` 与 `--md3-*` 角色色；
- **改形状**：`--t-r-win` / `--t-r-card` / `--t-btn-r` 一处改全套圆角跟随；
- **改质感**：`--t-blur`、`--t-surface(-2/-3)`、`--t-veil` 控制玻璃与面纱；
- **换贴纸**：替换 `assets/` 里的 PNG（保持文件名不变最省事）；
- **做新主题**：复制 `examples/minimal/` 改 `id` 与配色，规范见 [SPEC.md](SPEC.md)。

主题包**不执行任何代码**（只有 CSS 与图片），安装时有 zip-slip / 路径越界 /
id 冲突 / 体积上限（24 MB / 400 条目）等多重校验。

## 目录结构

```
├── SPEC.md          包规范（spec 1）：manifest 字段表 + theme.css 铁律 + 自定义清单
├── themes/<id>/     13 套主题的源树（manifest.json + theme.css + assets/ + preview.png）
├── examples/        起手示例（minimal / sticker）
├── tools/           示例素材生成脚本（零依赖 Python）
└── dist/            打包好的 .fcpt（与 Release 资产一致）
```

## 贡献

欢迎提交新主题：fork → 在 `themes/` 下按 SPEC.md 建目录 → 本地打包自测 → PR。
用同人素材的主题请注明素材出处并声明「仅供个人非商业使用」。

## 许可

仓库内代码（CSS / 脚本 / 文档）遵循 MIT。各主题的**图片素材版权归原作者 /
版权方所有**，仅供个人非商业使用 —— 请勿将含同人素材的主题用于商业用途。

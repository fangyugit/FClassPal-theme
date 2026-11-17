# -*- coding: utf-8 -*-
"""FClassPal-theme 模糊度适配 + 打包：
① theme.css：--t-blur 乘 var(--blur-bg-mul,1)（主界面背景档）；
   --glass-alpha 耦合放宽（floor+span>=0.9 的 veil 才动，floor 减半）
② manifest.json：版本 minor +1，加 "blur": true 与 "repo": "fangyugit/FClassPal-theme"
③ 圆括号配平校验
④ 打 dist/<id>.fcpt（zip 根目录直接放文件）
"""
import io, json, os, re, zipfile

REPO = 'fangyugit/FClassPal-theme'
THEMES = 'themes'
DIST = 'dist'

changed = []
for name in sorted(os.listdir(THEMES)):
    d = os.path.join(THEMES, name)
    if not os.path.isdir(d):
        continue
    cssp = os.path.join(d, 'theme.css')
    mfp = os.path.join(d, 'manifest.json')
    css = io.open(cssp, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in css else '\n'

    # ① --t-blur 乘主界面背景档
    def blur_mul(m):
        return 'blur(calc(%spx * var(--blur-bg-mul, 1))) saturate(%s%%)' % (m.group(1), m.group(2))
    css2, n1 = re.subn(r'blur\((\d+)px\) saturate\((\d+)%\)', blur_mul, css)
    css = css2

    # ①b 透明度耦合放宽：floor + span >= 0.9 的 veil（floor 减半，顶不变）
    def widen(m):
        floor = float(m.group(1)); span = float(m.group(2))
        if floor + span < 0.9:
            return m.group(0)          # 装饰性小系数不动
        f2 = round(floor * 0.5, 2)
        s2 = round(1.0 - f2, 2)
        return 'calc(%.2f + %.2f * var(--glass-alpha))' % (f2, s2)
    css2, n2 = re.subn(r'calc\((0\.\d+) \+ (0\.\d+) \* var\(--glass-alpha\)\)', widen, css)
    css = css2

    if n1 or n2:
        io.open(cssp, 'w', encoding='utf-8', newline='').write(css)
    changed.append('%s: blur×%d alpha×%d' % (name, n1, n2))

    # ①c 括号配平
    if css.count('(') != css.count(')'):
        raise SystemExit('括号不配平: ' + name)

    # ② manifest
    mf = json.load(io.open(mfp, encoding='utf-8'))
    v = str(mf.get('version', '1.0.0'))
    parts = v.split('.')
    if len(parts) >= 2:
        parts[1] = str(int(parts[1]) + 1)
        mf['version'] = '.'.join(parts)
    mf['blur'] = True
    mf['repo'] = REPO
    io.open(mfp, 'w', encoding='utf-8', newline='').write(
        json.dumps(mf, ensure_ascii=False, indent=2) + '\n')
    changed.append('%s -> v%s' % (name, mf['version']))

    # ④ 打包
    out = os.path.join(DIST, name + '.fcpt')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(d):
            for f in sorted(files):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, d).replace('\\', '/')
                z.write(full, rel)
print('\n'.join(changed))
print('packed:', len([f for f in os.listdir(DIST) if f.endswith('.fcpt')]), '个 .fcpt')

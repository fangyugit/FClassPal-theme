# -*- coding: utf-8 -*-
"""生成 examples/sticker 的示例素材（零依赖：手写 PNG 编码器）。
   跑法：python tools/make-example-assets.py
   产物：examples/sticker/assets/badge.png、sparkle.png、preview.png
   这些图纯粹是"示例长什么样"，换成自己的素材直接覆盖同名文件即可。
"""
import io, os, zlib, struct, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples', 'sticker')


def png(path, w, h, px):
    """px: (x, y) -> (r, g, b, a)"""
    raw = bytearray()
    for y in range(h):
        raw.append(0)                      # filter type 0
        for x in range(w):
            raw.extend(bytes(px(x, y)))
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data +
                struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))
    body = (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(body)
    print('  %s  %dx%d  %.1f KB' % (os.path.basename(path), w, h, len(body) / 1024))


def mix(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(3))


def badge(size=128):
    """圆形徽章：径向渐变 + 白环 + 左上高光"""
    c = (size - 1) / 2.0
    R = size / 2.0

    def px(x, y):
        dx, dy = x - c, y - c
        d = math.hypot(dx, dy)
        if d > R - 0.5:
            return (0, 0, 0, 0)
        # 抗锯齿：最外 1px 淡出
        a = 255 if d < R - 1.2 else int(255 * max(0.0, (R - 0.5 - d)))
        t = min(1.0, d / R)
        col = mix((122, 158, 255), (52, 74, 196), t ** 0.85)
        # 白环（外圈 12% 半径）
        if d > R * 0.86:
            col = mix(col, (255, 255, 255), 0.92)
        # 左上高光
        hl = math.hypot(dx + R * 0.34, dy + R * 0.40)
        if hl < R * 0.30:
            col = mix(col, (255, 255, 255), 0.38 * (1 - hl / (R * 0.30)))
        return (col[0], col[1], col[2], a)

    return px


def sparkle(size=128):
    """四角闪光：菱形凹边，白到浅蓝"""
    c = (size - 1) / 2.0
    R = size / 2.0

    def px(x, y):
        dx, dy = (x - c) / R, (y - c) / R
        # 四角星的隐式曲线 |x|^0.62 + |y|^0.62 = 1（凹边，比菱形更像星光）
        v = abs(dx) ** 0.62 + abs(dy) ** 0.62
        if v > 1.02:
            return (0, 0, 0, 0)
        a = 255 if v < 0.94 else int(255 * max(0.0, (1.02 - v) / 0.08))
        t = min(1.0, v)
        col = mix((255, 255, 255), (150, 186, 255), t)
        return (col[0], col[1], col[2], a)

    return px


def preview(w=256, h=144, accent=(96, 132, 240)):
    """仓库展示用的预览图：accent 底色 + 一枚徽章 + 一枚闪光"""
    px_badge = badge(64)
    px_spark = sparkle(48)

    def px(x, y):
        base = mix(mix((255, 255, 255), accent, 0.10), accent, y / float(h) * 0.55)
        out = list(base) + [255]
        # 徽章左下
        bx, by = x - 62, y - 84
        if 0 <= bx < 64 and 0 <= by < 64:
            r, g, b, a = px_badge(bx, by)
            if a:
                k = a / 255.0
                out = [int(out[i] * (1 - k) + (r, g, b)[i] * k) for i in range(3)] + [255]
        # 闪光右上
        sx, sy = x - 176, y - 28
        if 0 <= sx < 48 and 0 <= sy < 48:
            r, g, b, a = px_spark(sx, sy)
            if a:
                k = a / 255.0
                out = [int(out[i] * (1 - k) + (r, g, b)[i] * k) for i in range(3)] + [255]
        return tuple(out)

    return px


if __name__ == '__main__':
    d = os.path.join(OUT, 'assets')
    if not os.path.isdir(d):
        os.makedirs(d)
    print('生成示例素材 →', os.path.normpath(OUT))
    png(os.path.join(d, 'badge.png'), 128, 128, badge())
    png(os.path.join(d, 'sparkle.png'), 128, 128, sparkle())
    png(os.path.join(OUT, 'preview.png'), 256, 144, preview())

"""Home-screen icon for iPhone (apple-touch-icon.png) from the sun drawing in favicon.svg.

iOS always puts the icon on a rounded square and fills anything transparent with black,
so the tile is drawn on purpose: a white sun on black, the same pair as the tab icon.
The drawing's lines are thin, so they are thickened a little to stay clear at 180px.
Run after changing favicon.svg:  python tools/make_touch_icon.py   (needs Pillow)
"""
import os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
svg = open(os.path.join(ROOT, 'favicon.svg'), encoding='utf-8').read()
d = re.search(r'<path[^>]* d="([^"]+)"', svg).group(1)
MW, MH = 612, 418          # the drawing's own box inside the path
THICKEN = 8                # extra line weight, in the drawing's units

loops, cur, pos = [], None, (0, 0)
for cmd, args in re.findall(r'([MLQZ])([-\d. ]*)', d):
    n = [float(t) for t in args.split()]
    if cmd == 'M':
        if cur: loops.append(cur)
        pos = (n[0], n[1]); cur = [pos]
    elif cmd == 'L':
        pos = (n[0], n[1]); cur.append(pos)
    elif cmd == 'Q':
        c, p = (n[0], n[1]), (n[2], n[3])
        for i in range(1, 9):
            t = i / 8
            cur.append(((1-t)**2*pos[0] + 2*(1-t)*t*c[0] + t*t*p[0],
                        (1-t)**2*pos[1] + 2*(1-t)*t*c[1] + t*t*p[1]))
        pos = p
    elif cmd == 'Z' and cur:
        loops.append(cur); cur = None
if cur: loops.append(cur)

SIZE, SS = 180, 4                     # final size, supersampling for smooth edges
big = SIZE * SS
w = big * 0.70                        # drawing width: clear of the corners iOS rounds off
k = w / MW
ox, oy = (big - w) / 2, (big - MH * k) / 2

mask = np.zeros((big, big), bool)
for lp in loops:
    im = Image.new('1', (big, big), 0)
    ImageDraw.Draw(im).polygon([(ox + x * k, oy + y * k) for x, y in lp], fill=1)
    mask ^= np.asarray(im, bool)      # even-odd, so enclosed gaps stay open

img = Image.fromarray(np.where(mask, 255, 0).astype(np.uint8))
r = max(1, round(THICKEN * k / 2))
img = img.filter(ImageFilter.MaxFilter(2 * r + 1))   # thicken every line evenly
img.resize((SIZE, SIZE), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, 'apple-touch-icon.png'), optimize=True)
print('apple-touch-icon.png', SIZE, 'x', SIZE)

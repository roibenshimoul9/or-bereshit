"""The picture shown when the site's link is shared (WhatsApp, Facebook) and next to it in Google.

Three product photos side by side, 1200x630, saved as og.jpg in the site root.
Run after changing the photos:  python tools/make_og_image.py   (needs Pillow)
"""
import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = ['judaica-blessing-candlesticks-1.webp', 'personal-memorial-candle-1.webp', 'custom-designed-mezuzah-1.webp']
W, H, GAP = 1200, 630, 6

card = Image.new('RGB', (W, H), '#1A1511')
pw = (W - GAP * (len(PHOTOS) - 1)) // len(PHOTOS)
for i, name in enumerate(PHOTOS):
    im = Image.open(os.path.join(ROOT, 'img', name)).convert('RGB')
    card.paste(ImageOps.fit(im, (pw, H), Image.LANCZOS, centering=(0.5, 0.5)), (i * (pw + GAP), 0))
card.save(os.path.join(ROOT, 'og.jpg'), quality=86, optimize=True, progressive=True)
print('og.jpg', card.size)

import os, sys, shutil
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import sun
s=sun.svg('fav',cls='fav')
# the logo itself on a transparent square: no background tile.
# logo spans x -34.5..34.5 and y -29..14.6, so a 69-unit square centered on y=-7.2 holds it exactly.
head='<svg class="fav" viewBox="-34.5 -29 69 43.6" role="img" aria-label="אור בראשית">'
assert s.count(head)==1
s=s.replace(head,'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-35 -42.2 70 70">',1)
# same drawing as the header logo; lines only slightly heavier so the rays survive at 16px
s=s.replace('stroke-width=".8"','stroke-width="1.4"')
s=s.replace('stroke-width="3" stroke-linecap','stroke-width="3.6" stroke-linecap')
out=r'C:\Users\Asus\Desktop\בניית בוטים ואתרים\אור בראשית קלוד\or-bereshit-vercel\favicon.svg'
open(out,'w',encoding='utf-8').write(s)
shutil.copyfile(out,os.path.join(HERE,'favicon.svg'))
bg=lambda c:f'<div style="background:{c};padding:18px;display:flex;gap:24px;align-items:center">'+''.join(f'<img src="favicon.svg" width="{n}" height="{n}">' for n in (16,32,64,140))+'</div>'
open(os.path.join(HERE,'fav-preview.html'),'w',encoding='utf-8').write(
  '<!doctype html><meta charset="utf-8"><body style="margin:0">'+bg('#3b3a2e')+bg('#f1f1f1')+'</body>')
print('ok',len(s))

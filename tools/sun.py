import math
# Sunrise over clouds and water, redrawn flat (no paper perspective), horizon at y=0.
rays=[]
for side in (-1,1):
    for ang,r1,r2 in [(0,15.8,32.5),(14,15.6,31.4),(30,15.4,30.2),(48,15.2,28.6),(67,15.0,27.4)]:
        a=math.radians(ang)
        x1,y1=side*r1*math.cos(a),-r1*math.sin(a)
        x2,y2=side*r2*math.cos(a),-r2*math.sin(a)
        rays.append(f'M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}')
rays.append('M0 -14.6L0 -26.6')

cloud=('M-30.5 7.3C-29.4 6.2-28.2 6-26.6 6.2C-25.8 4.8-24.2 4.2-22.6 4.9'
       'C-21.2 2.4-18.2 1.4-15.6 2.6C-13.6 1.2-10.6 1.6-9.6 3.6'
       'C-8.2 3-6.6 3.2-5.8 4.4L-3.6 4.4C-2.6 3.5-1 3.4 0 4.2'
       'L7.4 4.2C8.6 3.1 10.8 3 12.2 3.9L32.6 3.9')
water=('M2.2 5.3C3.2 6.7 4.6 7.2 6.4 7.2L27.6 7.2'
       'M-26.2 9.8L-2.8 9.8'
       'M3.6 12.4C4.6 10.6 6 9.8 8 9.8L22.4 9.8'
       'M-15.6 12.4L15.2 12.4')

def svg(uid, cls='brand-logo', extra=''):
    return (f'<svg class="{cls}" viewBox="-34.5 -29 69 43.6" role="img" aria-label="אור בראשית"{extra}>'
            f'<defs><linearGradient id="sunG{uid}" x1="0" y1="-16" x2="0" y2="2" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#F6DDA6"/><stop offset=".55" stop-color="#D9AE66"/><stop offset="1" stop-color="#B98A45"/></linearGradient>'
            f'<linearGradient id="lineG{uid}" x1="-34" y1="0" x2="34" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#C99A55"/><stop offset=".5" stop-color="#EBC98A"/><stop offset="1" stop-color="#C99A55"/></linearGradient>'
            f'<mask id="sky{uid}" maskUnits="userSpaceOnUse" x="-40" y="-40" width="80" height="80"><rect x="-40" y="-40" width="80" height="42.6" fill="#fff"/><path d="{cloud}" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>'
            # the sun sits behind the cloud: cut it just below the cloud line, then knock the cloud out of it
            f'<circle cx="0" cy="1.6" r="13.4" fill="url(#sunG{uid})" mask="url(#sky{uid})"/>'
                        f'<g fill="none" stroke="url(#lineG{uid})" class="lines" stroke-width=".8" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{"".join(rays)}"/><path d="{cloud}"/><path d="{water}"/></g></svg>')

if __name__=='__main__':
    page=('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#1A1511 radial-gradient(circle at 30% 20%,#3a3026,#1A1511 60%);display:grid;gap:30px;padding:30px;justify-items:center">'
          + svg('x', extra=' style="width:620px;height:auto"')
          + '<div style="display:flex;gap:14px;align-items:center;color:#EDE3D2;font:28px Bellefair,serif">'+svg('y', extra=' style="height:46px;width:auto"')+'אור בראשית</div></body>')
    open(r'C:\Users\Asus\AppData\Local\Temp\claude\C--Users-Asus-Desktop\3da7485e-6d7f-47c2-a363-b01f0a30336c\scratchpad\logo\sun.html','w',encoding='utf-8').write(page)
    print('ok')

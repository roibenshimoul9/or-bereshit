"""iPhone / touch layer for the Vercel build of Or Bereshit.

Everything visual is gated behind phone width (max-width: 760px) or a coarse pointer, so the
desktop layout does not change. The only global rules are ones with no visible effect on a
mouse: no tap flash, no text inflation, instant taps, and no text selection on controls.
"""

CSS = r'''
/* ---------- iPhone / touch ---------- */
/* no gray flash on tap, no font inflation in landscape (invisible with a mouse) */
html{-webkit-tap-highlight-color:transparent;-webkit-text-size-adjust:100%;text-size-adjust:100%}
/* taps fire immediately; a long press on a control doesn't select its label */
button,a,summary,[role="button"],.chip,.ptool,.add,.icon-btn{touch-action:manipulation}
button,summary,[role="button"],.chip,.ptool,.add,.icon-btn,.cue,.ask-fab{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}

/* finger-sized targets wherever the pointer is a finger */
@media (pointer:coarse){
  input,textarea,select{font-size:max(16px,1em)}
  .ptool{width:40px;height:40px}
  .ptool svg,.ptool.pfav svg{width:19px;height:19px}
  .pdots button{position:relative}
  .pdots button::after{content:"";position:absolute;inset:-12px -6px}
  .qty button{width:36px;height:36px}
  .line .rm{padding:8px;margin:-6px}
  .close{min-width:44px;min-height:44px}
  .qa summary{min-height:52px}
}

@media (max-width:760px){
  /* header: brand + account + cart on one row, the four links evenly on the second; nothing scrolls sideways */
  .top .wrap{display:flex;flex-wrap:wrap;align-items:center;column-gap:10px;row-gap:2px;padding-block:8px 4px}
  .top .wrap::after{content:"";order:3;flex-basis:100%;height:0}
  .top .brand{order:0;flex:1;min-width:0}
  .top .brand b{font-size:1.35rem;white-space:nowrap}
  .brand .brand-logo{height:32px}
  .top .nav{display:contents}
  .top .nav a{order:4;display:inline-flex;align-items:center;min-height:40px;padding-inline:2px;font-size:.9rem;white-space:nowrap}
  .top .nav a::after{bottom:6px}
  .top .wrap{justify-content:space-between}
  #loginBtn{order:1;padding:6px 10px;max-width:42vw}
  #loginBtn .avatar{flex:none}
  #loginBtn{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #cartBtn{order:2;padding:6px 10px}

  /* products: two per row so a phone shows more than one at a time */
  .pgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
  .pcard{border-radius:14px}
  .pcard .pmedia{aspect-ratio:1/1.05}
  .pbadge{top:8px;inset-inline-start:8px;font-size:.66rem;padding:3px 7px}
  .ptools{top:6px;bottom:auto;inset-inline-end:6px;gap:4px}
  .pdots{bottom:12px}
  .pbody{padding:10px 10px 12px;gap:6px}
  .pmeta{font-size:.66rem}
  .pmeta span+span{display:none}
  .pcard h3{font-size:.92rem;padding-bottom:8px;line-height:1.3}
  .pprice b{font-size:1.1rem}
  .pprice .from,.pprice small{font-size:.68rem}
  .pbuy{gap:6px}
  .pbuy .add{padding:10px 6px;font-size:.8rem;border-radius:9px;min-height:40px}

  /* chat: a round button that doesn't cover the products */
  .ask-fab{padding:0;width:56px;height:56px;justify-content:center;border-radius:50%;font-size:0;gap:0}
  .ask-fab .lion{width:40px;height:40px}

  /* dialogs sit higher and scroll inside themselves */
  dialog{max-height:calc(100dvh - 24px - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px));overflow-y:auto;overscroll-behavior:contain}
  .qv .dlg{padding:14px}
  /* messages drop in from the top, clear of the cart's order button and the chat button */
  .toast{top:calc(10px + env(safe-area-inset-top,0px));bottom:auto;max-width:calc(100% - 24px)}
  @starting-style{.toast{opacity:0;transform:translate(-50%,-14px)}}
}
@media (max-width:360px){
  .top .nav a{font-size:.82rem}
  .pbuy .add{font-size:.74rem}
}
'''


def apply(page):
    def rep(a, b, count=1):
        nonlocal page
        n = page.count(a)
        assert n == count, (a[:70], n)
        page = page.replace(a, b)

    rep('/* ---------- drawer / dialog / toast ---------- */', CSS + '\n/* ---------- drawer / dialog / toast ---------- */')

    # short labels on phones for the two card buttons (full text stays for screen readers and desktop)
    page = page.replace('<span class="go">הזמנה פיזית (הדפסה)</span>',
                        '<span class="go"><span class="lg">הזמנה פיזית (הדפסה)</span><span class="sm">להזמנה</span></span>')
    page = page.replace('<span class="go">לרכישת קובץ דיגיטלי</span>',
                        '<span class="go"><span class="lg">לרכישת קובץ דיגיטלי</span><span class="sm">קובץ דיגיטלי</span></span>')
    page = page.replace('<span class="go">לקבלת הצעת מחיר</span></a>`',
                        '<span class="go"><span class="lg">לקבלת הצעת מחיר</span><span class="sm">הצעת מחיר</span></span></a>`')
    rep('/* ---------- iPhone / touch ---------- */',
        '/* ---------- iPhone / touch ---------- */\n.add .go .sm{display:none}\n@media (max-width:760px){.pcard .add .go .lg{display:none}.pcard .add .go .sm{display:inline}}')

    # iOS fires "resize" whenever the address bar shows or hides; the intro already rebuilds on real
    # width changes through its ResizeObserver, so the height-only resize must not restart the particles
    rep("    addEventListener('resize',build);\n", '')

    # the chat button still announces its name without the visible label
    rep('<button class="ask-fab" type="button" id="askFab" aria-controls="ask" aria-expanded="false">',
        '<button class="ask-fab" type="button" id="askFab" aria-controls="ask" aria-expanded="false" aria-label="צ\'אט עם ארי">')
    return page

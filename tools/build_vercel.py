SRC=r'C:\Users\Asus\Desktop\בניית בוטים ואתרים\אור בראשית קלוד\or-bereshit\or-bereshit.html'
OUT=r'C:\Users\Asus\Desktop\בניית בוטים ואתרים\אור בראשית קלוד\or-bereshit-vercel\index.html'
s=open(SRC,encoding='utf-8').read()

def rep(a,b,count=1):
    global s
    n=s.count(a)
    assert n==count,(a[:70],n)
    s=s.replace(a,b)

# the page no longer depends on Claude: honest footnote under the chat
rep('<p class="ask-foot">ארי עונה בעזרת Claude, על חשבון Claude שלכם. כדאי לוודא פרטים חשובים מול הצוות.</p>',
    '<p class="ask-foot">ארי הוא עוזר דיגיטלי ועלול לטעות. כדאי לוודא פרטים חשובים מול הצוות.</p>')

start=s.index('  /* ---------- smart assistant (ארי) ---------- */')
end=s.index('  /* ---------- pages ---------- */')
ASSISTANT=r'''  /* ---------- smart assistant (ארי) — answered by /api/chat (Gemini on the server) ---------- */
  (()=>{
    const fab=$('askFab'), panel=$('ask'), log=$('askLog'), form=$('askForm'), input=$('askInput'), go=$('askGo'), sugg=$('askSugg');
    const ENDPOINT='/api/chat';
    const WA_LINK='https://wa.me/972546843548';
    const SEND_ICON=go.innerHTML;
    const STOP_ICON='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2"/></svg>';
    let offline=false, busy=false, ctl=null;
    const turns=[];

    const scrollDown=()=>{log.scrollTop=log.scrollHeight;};
    function addMsg(kind,text){
      const m=document.createElement('div'); m.className='msg '+kind; m.textContent=text;
      log.appendChild(m); scrollDown(); return m;
    }
    const clean=t=>t.replace(/\*\*(.+?)\*\*/g,'$1').replace(/^#+\s*/gm,'').replace(/^\s*[-*]\s+/gm,'• ');

    function goOffline(){
      if(offline) return; offline=true;
      const m=document.createElement('div'); m.className='msg bot ask-off';
      m.innerHTML='<span>העוזר החכם לא זמין כרגע. הצוות שלנו ישמח לעזור בוואטסאפ.</span>';
      const a=document.createElement('a'); a.className='btn btn-primary'; a.href=WA_LINK; a.target='_blank'; a.rel='noopener'; a.textContent='לשיחה בוואטסאפ';
      m.appendChild(a); log.appendChild(m); scrollDown();
      input.disabled=true; go.disabled=true; sugg.hidden=true;
      input.placeholder='העוזר לא זמין כרגע';
    }

    // what the server may ask the page to do
    const PAGE_HASH={home:'#/',collection:'#collection',engrave:'#engrave',faq:'#faq',support:'#/support',guide:'#/guide',specials:'#/specials',licenses:'#/licenses',privacy:'#/privacy',shipping:'#/shipping',returns:'#/returns'};
    function runAction(a){
      if(!a||typeof a!=='object') return;
      const args=a.args||{};
      if(a.name==='add_to_cart'){
        const p=PRODUCTS.find(x=>x.id===String(args.product_id));
        if(!p) return;
        if(!p.price) return;
        addToCart(p,'phys',p.price);
        addMsg('note','נוסף לסל: '+p.name);
      } else if(a.name==='open_page'){
        const h=PAGE_HASH[String(args.page)];
        if(h){location.hash=h;addMsg('note','פתחתי עבורכם את העמוד');}
      }
    }

    function setBusy(v){
      busy=v; go.classList.toggle('stop',v); go.innerHTML=v?STOP_ICON:SEND_ICON;
      go.setAttribute('aria-label',v?'עצירה':'שליחה'); go.type=v?'button':'submit';
    }

    // reveal the answer quickly word by word, so it reads like it is being written
    function typeOut(el,text){
      if(reduce){el.textContent=text;return Promise.resolve();}
      const words=text.split(/(\s+)/); let i=0;
      return new Promise(done=>{
        const step=()=>{i=Math.min(words.length,i+3);el.textContent=words.slice(0,i).join('');scrollDown();if(i<words.length)requestAnimationFrame(step);else done();};
        step();
      });
    }

    async function send(text){
      text=text.trim();
      if(busy||offline||!text) return;
      sugg.hidden=true;
      addMsg('me',text); input.value=''; autoGrow();
      turns.push({role:'user',content:text.slice(0,1500)});
      const bubble=addMsg('bot thinking','ארי חושב');
      setBusy(true);
      ctl=new AbortController();
      let recent=turns.slice(-16); while(recent.length&&recent[0].role!=='user') recent.shift();
      try{
        const res=await fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:recent}),signal:ctl.signal});
        if(res.status===503||res.status===404){bubble.remove();goOffline();return;}
        const data=await res.json().catch(()=>({}));
        bubble.classList.remove('thinking');
        if(!res.ok){
          bubble.textContent=res.status===429?'יש כרגע עומס. נסו לשלוח שוב בעוד רגע.':'משהו השתבש בחיבור. נסו לשלוח שוב.';
          bubble.classList.add('err');
          return;
        }
        (Array.isArray(data.actions)?data.actions:[]).forEach(runAction);
        const out=clean(String(data.text||''));
        turns.push({role:'assistant',content:out.slice(0,1500)});
        log.appendChild(bubble);                 // keep the answer below any action notes
        await typeOut(bubble,out);
      }catch(e){
        bubble.classList.remove('thinking');
        if(e&&e.name==='AbortError'){bubble.textContent='עצרתי.';}
        else if(location.protocol==='file:'){bubble.remove();goOffline();}
        else{bubble.textContent='אין חיבור לשרת כרגע. בדקו את החיבור ונסו שוב.';bubble.classList.add('err');}
      }finally{setBusy(false);ctl=null;scrollDown();}
    }

    function autoGrow(){input.style.height='auto';input.style.height=Math.min(input.scrollHeight,120)+'px';}
    input.addEventListener('input',autoGrow);
    input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send(input.value);}});
    form.addEventListener('submit',e=>{e.preventDefault();send(input.value);});
    go.addEventListener('click',e=>{if(busy){e.preventDefault();ctl&&ctl.abort();}});
    sugg.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>send(b.textContent)));

    const openAsk=v=>{
      panel.classList.toggle('open',v); panel.inert=!v; fab.setAttribute('aria-expanded',String(v));
      if(v){if(!input.disabled)input.focus({preventScroll:true});scrollDown();} else fab.focus({preventScroll:true});
    };
    fab.addEventListener('click',()=>openAsk(true));
    $('askClose').addEventListener('click',()=>openAsk(false));
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&panel.classList.contains('open'))openAsk(false);});
  })();

'''
s=s[:start]+ASSISTANT+s[end:]
assert 'claude.use' not in s

HEAD='''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="אור בראשית: יודאיקה בהדפסת תלת־ממד ובגימור ידני. פמוטים, גביעי קידוש, חנוכיות ונרות זיכרון בהזמנה אישית.">
<meta name="theme-color" content="#1A1511">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>
'''
# title + fonts + styles belong in <head>; the page body starts at the intro
i=s.index('<header class="intro"')
page=HEAD+s[:i]+'</head>\n<body>\n'+s[i:]+'\n</body>\n</html>\n'
# personal area (Firebase) lives only in the Vercel build
import os, sys
TOOLS=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(TOOLS)
sys.path.insert(0,TOOLS)
import account_layer
page=account_layer.apply(page)
import mobile_layer
page=mobile_layer.apply(page)
open(os.path.join(ROOT,'firestore.rules'),'w',encoding='utf-8').write(account_layer.RULES)
cfg=os.path.join(ROOT,'firebase-config.js')
if not os.path.exists(cfg):   # never overwrite a config the owner already filled in
    open(cfg,'w',encoding='utf-8').write(account_layer.CONFIG_JS)
open(OUT,'w',encoding='utf-8').write(page)
print('ok',len(page))

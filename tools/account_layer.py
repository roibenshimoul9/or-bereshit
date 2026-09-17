"""Personal-area layer for the Vercel build of Or Bereshit.

Adds Firebase sign-in (Google, or an email link with no password), a "my account" page (orders, details and
addresses, favorites), cart sync between devices, order saving at checkout, and an
admin page for order statuses. Applied by build_vercel.py after the base page is built.
The Claude artifact version stays without accounts (it cannot reach outside services).
"""

GOOGLE_G = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.4h6.5a5.6 5.6 0 0 1-2.4 3.7v3h3.9c2.3-2.1 3.5-5.2 3.5-8.8z"/>'
            '<path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z"/>'
            '<path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8z"/>'
            '<path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.3 6.6l4 3.1c.9-2.9 3.6-4.9 6.7-4.9z"/></svg>')
HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.3s-7.5-4.6-9.3-9.2C1.5 8 3.5 4.6 6.8 4.6c2 0 3.6 1.1 4.3 2.6h1.8c.7-1.5 2.3-2.6 4.3-2.6 3.3 0 5.3 3.4 4.1 6.5-1.8 4.6-9.3 9.2-9.3 9.2z"/></svg>'

CSS = r'''
/* ---------- personal area ---------- */
.login .note{margin:0;color:var(--ink-soft);font-size:.92rem}
.login .note.small{font-size:.78rem}
.login .note a{color:var(--brass)}
.google-btn{width:100%;background:#fff;color:#1f1f1f;border:0;border-radius:10px;padding:12px 16px;font-weight:700;gap:10px}
.google-btn svg{width:20px;height:20px}
@media (hover:hover) and (pointer:fine){.google-btn:hover{background:#f1efe9}}
.or{display:flex;align-items:center;gap:12px;color:var(--ink-soft);font-size:.8rem}
.or::before,.or::after{content:"";flex:1;height:1px;background:var(--line)}
#emailLinkForm{display:grid;gap:10px}
#emailLinkForm .btn{width:100%;border-radius:10px}
.login-msg{margin:0;min-height:1.2em;font-size:.86rem;color:var(--ink-soft)}
.login-msg.ok{color:#A9CFA0}.login-msg.bad{color:#E09A86}
.icon-btn.signed{border-color:rgba(216,168,96,.5)}
.icon-btn .avatar{width:22px;height:22px;border-radius:50%;display:inline-grid;place-items:center;background:var(--brass);color:var(--brass-ink);font-size:.72rem;font-weight:700;overflow:hidden}
.icon-btn .avatar img{width:100%;height:100%;object-fit:cover}
.ptool.pfav svg{width:17px;height:17px;fill:none;stroke:#2B231C;stroke-width:1.8;transition:fill 200ms ease,stroke 200ms ease,transform 260ms var(--ease-out)}
.ptool.pfav[aria-pressed="true"] svg{fill:#C4513A;stroke:#C4513A;transform:scale(1.08)}
.acc-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:16px;margin-bottom:clamp(28px,4vw,44px)}
.acc-head h1{font-family:var(--display);font-weight:400;font-size:clamp(2.4rem,5.4vw,3.8rem);line-height:1.05;margin:8px 0 6px}
.acc-head .actions{display:flex;flex-wrap:wrap;gap:10px}
.acc-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:18px;align-items:start}
.acc-grid .span{grid-column:1/-1}
@media (max-width:900px){.acc-grid{grid-template-columns:1fr}}
.acc-grid h2{font-family:var(--display);font-weight:400;font-size:1.7rem;margin:0 0 14px}
.acc-state{padding:clamp(28px,5vw,48px);text-align:center;display:grid;justify-items:center;gap:12px;max-width:620px;margin-inline:auto}
.acc-state h2{margin:0}
.orders{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.order{border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:6px}
.order .top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 12px;align-items:center}
.order .no{font-family:var(--util);font-weight:500;direction:ltr}
.order .when{font-size:.82rem;color:var(--ink-soft)}
.order .items{margin:0;color:var(--ink-soft);font-size:.92rem}
.order .sum{font-family:var(--util);font-weight:500;font-variant-numeric:tabular-nums}
.status{display:inline-flex;align-items:center;gap:6px;font-family:var(--util);font-size:.74rem;font-weight:500;padding:3px 10px;border-radius:999px;background:rgba(241,230,210,.1);color:var(--ink)}
.status::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.status.received{color:#E6C07F;background:rgba(230,192,127,.12)}
.status.printing{color:#9FC4E8;background:rgba(159,196,232,.12)}
.status.shipped{color:#B9A6E8;background:rgba(185,166,232,.12)}
.status.delivered{color:#A9CFA0;background:rgba(169,207,160,.12)}
.status.cancelled{color:#E09A86;background:rgba(224,154,134,.12)}
.muted{color:var(--ink-soft);margin:0}
.addr-list{list-style:none;margin:6px 0 14px;padding:0;display:grid;gap:8px}
.addr-list li{display:grid;grid-template-columns:1fr auto;gap:4px 10px;align-items:start;border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.addr-list b{font-size:.92rem}
.addr-list span{grid-column:1;color:var(--ink-soft);font-size:.88rem;white-space:pre-line}
.addr-list .row-actions{grid-row:1/3;grid-column:2;display:flex;flex-direction:column;gap:4px;align-items:end}
.addr-list button{background:none;border:0;cursor:pointer;color:var(--ink-soft);font:inherit;font-size:.78rem;text-decoration:underline;text-underline-offset:3px}
.addr-list .def{color:var(--brass);text-decoration:none;cursor:default}
.acc-form{display:grid;gap:12px}
.acc-form .two{gap:12px}
.acc-form .btn{justify-self:start}
.fav-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.fav{border:1px solid var(--line);border-radius:12px;overflow:hidden;display:grid}
.fav img{width:100%;aspect-ratio:4/3.4;object-fit:cover;display:block}
.fav div{padding:10px 12px;display:grid;gap:4px}
.fav b{font-size:.92rem;line-height:1.3}
.fav .p{font-family:var(--util);font-size:.86rem;color:var(--ink-soft)}
.fav .acts{display:flex;justify-content:space-between;gap:8px;margin-top:4px}
.fav button{background:none;border:0;padding:0;cursor:pointer;font:inherit;font-size:.8rem;color:var(--brass)}
.fav button.rm{color:var(--ink-soft)}
.saved-addr{width:100%;background:color-mix(in srgb,var(--ground) 70%,var(--niche));border:1px solid var(--line);border-radius:2px;padding:8px 10px;font:inherit;color:inherit}
.admin-table{width:100%;border-collapse:collapse;font-size:.9rem}
.admin-wrap{overflow-x:auto}
.admin-table th,.admin-table td{text-align:start;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.admin-table th{font-family:var(--util);font-size:.74rem;color:var(--ink-soft);font-weight:500}
.admin-table td.num{font-family:var(--util);font-variant-numeric:tabular-nums;white-space:nowrap}
.admin-table select{background:color-mix(in srgb,var(--ground) 70%,var(--niche));border:1px solid var(--line);color:inherit;font:inherit;padding:6px 8px;border-radius:6px}
'''

LOGIN_DIALOG = f'''<dialog id="loginDlg" aria-labelledby="loginTitle">
  <div class="dlg login">
    <div class="dlg-top">
      <div><div class="eyebrow">האזור האישי</div><h3 id="loginTitle">כניסה לחשבון</h3></div>
      <button class="close" type="button" id="closeLogin" aria-label="סגירה">×</button>
    </div>
    <p class="note" id="loginIntro">ההזמנות, הכתובות והמועדפים שלכם, בכל מכשיר. בלי סיסמה.</p>
    <button class="btn google-btn" type="button" id="googleLogin">{GOOGLE_G} המשך עם Google</button>
    <div class="or"><span>או קישור כניסה למייל</span></div>
    <form id="emailLinkForm" novalidate>
      <div class="field"><label for="loginEmail">דוא״ל</label><input id="loginEmail" type="email" autocomplete="email" inputmode="email" required></div>
      <button class="btn btn-ghost" type="submit" id="emailLinkBtn">שלחו לי קישור כניסה</button>
    </form>
    <p class="login-msg" id="loginMsg" aria-live="polite"></p>
    <p class="note small">בכניסה לחשבון אתם מסכימים ל<a href="#/privacy">מדיניות הפרטיות</a>.</p>
  </div>
</dialog>'''

PAGES = '''  <!-- ===== personal area ===== -->
  <section class="page" data-route="account" hidden>
    <div class="wrap">
      <nav class="crumbs" aria-label="מיקום"><a href="#/">דף הבית</a> / האזור האישי</nav>
      <div id="accState"></div>
      <div id="accMain" hidden>
        <div class="acc-head">
          <div><div class="eyebrow">האזור האישי</div><h1 class="carved" id="accHello">שלום</h1><p class="lede" id="accEmail"></p></div>
          <div class="actions"><a class="btn btn-ghost" href="#/admin" id="adminLink" hidden>ניהול הזמנות</a><button class="btn btn-ghost" type="button" id="logoutBtn">התנתקות</button></div>
        </div>
        <div class="acc-grid">
          <div class="panel">
            <h2>ההזמנות שלי</h2>
            <ul class="orders" id="accOrders"></ul>
          </div>
          <div class="panel">
            <h2>פרטים וכתובות</h2>
            <form class="acc-form" id="accForm" novalidate>
              <div class="two">
                <div class="field"><label for="accName">שם מלא</label><input id="accName" type="text" autocomplete="name" maxlength="80"></div>
                <div class="field"><label for="accPhone">טלפון</label><input id="accPhone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" dir="ltr"></div>
              </div>
              <button class="btn btn-primary" type="submit">שמירת פרטים</button>
            </form>
            <h2 style="font-size:1.3rem;margin-top:22px">כתובות למשלוח</h2>
            <ul class="addr-list" id="accAddrs"></ul>
            <form class="acc-form" id="addrForm" novalidate>
              <div class="field"><label for="addrLabel">שם הכתובת (למשל: בית, עבודה)</label><input id="addrLabel" type="text" maxlength="30"></div>
              <div class="field"><label for="addrText">כתובת מלאה</label><textarea id="addrText" rows="2" maxlength="200" placeholder="עיר, רחוב, מספר בית ודירה"></textarea></div>
              <button class="btn btn-ghost" type="submit">הוספת כתובת</button>
            </form>
          </div>
          <div class="panel span">
            <h2>מועדפים</h2>
            <div class="fav-grid" id="accFavs"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="page" data-route="admin" hidden>
    <div class="wrap">
      <nav class="crumbs" aria-label="מיקום"><a href="#/">דף הבית</a> / <a href="#/account">האזור האישי</a> / ניהול הזמנות</nav>
      <div class="page-hero"><div class="eyebrow">ניהול</div><h1 class="carved">הזמנות</h1><p class="lede">עדכון סטטוס מופיע ללקוח באזור האישי שלו.</p></div>
      <div id="adminBody"></div>
    </div>
  </section>
'''

JS = r'''  /* ---------- personal area: Firebase sign-in, account page, synced cart, saved orders, admin ---------- */
  (()=>{
    const CFG=window.FIREBASE_CONFIG;
    const ADMINS=(window.OB_ADMIN_EMAILS||[]).map(e=>String(e).toLowerCase());
    const SDK='https://www.gstatic.com/firebasejs/10.14.1/';
    const STATUS={received:'התקבלה',printing:'בהדפסה',shipped:'נשלחה',delivered:'נמסרה',cancelled:'בוטלה'};
    const dlg=$('loginDlg'), msg=$('loginMsg'), loginBtn=$('loginBtn');
    let fb=null, auth=null, db=null, user=null, bootError=false, completingLink=false;
    let profile={name:'',phone:'',addresses:[],defaultAddr:null,favorites:[]};
    let orders=[], ordersState='idle', unsubOrders=null, unsubAdmin=null, saveT=null, route='';
    const isAdmin=()=>!!(user&&user.email&&user.emailVerified&&ADMINS.includes(user.email.toLowerCase()));
    const say=(t,kind)=>{msg.textContent=t||'';msg.className='login-msg'+(kind?' '+kind:'');};
    const when=ts=>{try{const d=ts&&ts.toDate?ts.toDate():null;return d?d.toLocaleDateString('he-IL',{day:'numeric',month:'long',year:'numeric'}):'';}catch(e){return '';}};
    const newOrderNo=()=>'OB-'+Date.now().toString(36).toUpperCase().slice(-5)+Math.random().toString(36).slice(2,4).toUpperCase();
    const slimCart=()=>cart.map(l=>({key:String(l.key),id:String(l.id),name:String(l.name),type:l.type==='file'?'file':'phys',price:Number(l.price)||0,qty:Math.max(1,Math.min(99,l.qty|0))}));

    function openLogin(note){
      say('');
      $('loginIntro').textContent=note||(completingLink?'כדי להשלים את הכניסה, הקלידו שוב את כתובת הדוא״ל שאליה נשלח הקישור.':'ההזמנות, הכתובות והמועדפים שלכם, בכל מכשיר. בלי סיסמה.');
      $('googleLogin').hidden=completingLink;
      if(completingLink) setTimeout(()=>$('loginEmail').focus(),50);
      $('emailLinkBtn').textContent=completingLink?'השלמת הכניסה':'שלחו לי קישור כניסה';
      if(!dlg.open) dlg.showModal();
      if(!CFG||!CFG.apiKey) say('האזור האישי עוד לא מחובר. ההפעלה תושלם בקרוב.','bad');
      else if(bootError) say('לא הצלחנו להתחבר לשירות הכניסה. בדקו את החיבור ורעננו את הדף.','bad');
    }
    acct.openLogin=openLogin;
    $('closeLogin').addEventListener('click',()=>dlg.close());
    dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close();});

    function paintLoginBtn(){
      if(user){
        const first=(profile.name||user.displayName||'').trim().split(/\s+/)[0]||'האזור שלי';
        const pic=user.photoURL?`<img src="${esc(user.photoURL)}" alt="" referrerpolicy="no-referrer">`:esc(first.charAt(0));
        loginBtn.innerHTML=`<span class="avatar">${pic}</span>${esc(first)}`;
        loginBtn.classList.add('signed'); loginBtn.setAttribute('aria-label','האזור האישי');
      }else{
        loginBtn.textContent='כניסה'; loginBtn.classList.remove('signed'); loginBtn.removeAttribute('aria-label');
      }
    }
    loginBtn.addEventListener('click',()=>{ if(user) location.hash='#/account'; else openLogin(); });

    const loadScript=src=>new Promise((res,rej)=>{const s=document.createElement('script');s.src=src;s.async=true;s.onload=res;s.onerror=()=>rej(new Error('load '+src));document.head.appendChild(s);});

    /* --- cart sync --- */
    function mergeRemoteCart(remote){
      if(!Array.isArray(remote)||!remote.length) return;
      let changed=false;
      remote.forEach(r=>{
        const p=PRODUCTS.find(x=>x.id===r.id); if(!p) return;
        const type=r.type==='file'?'file':'phys';
        if(type==='phys'&&!p.price) return;
        const key=p.id+'|'+type+'|';
        const line=cart.find(l=>l.key===key);
        const qty=Math.max(1,Math.min(99,r.qty|0));
        if(line){ if(qty>line.qty){line.qty=qty;changed=true;} }
        else{ cart.push({key,id:p.id,name:p.name,type,finish:null,price:type==='phys'?p.price:(Number(r.price)||0),qty,thumb:thumbOf(p.id)}); changed=true; }
      });
      if(changed){ renderCart(); try{localStorage.setItem(STORE,JSON.stringify({cart,coupon}));}catch(e){} }
    }
    function saveCartSoon(){
      if(!user||!db) return;
      clearTimeout(saveT);
      const uid=user.uid;
      saveT=setTimeout(()=>{
        if(!user||user.uid!==uid) return;
        db.collection('users').doc(uid).set({cart:slimCart(),updatedAt:fb.firestore.FieldValue.serverTimestamp()},{merge:true}).catch(()=>{});
      },700);
    }
    acct.cartChanged=saveCartSoon;

    /* --- saved addresses in the cart --- */
    function paintSavedAddr(){
      const box=$('addrBox'); let sel=$('savedAddr');
      if(!user||!profile.addresses.length){ if(sel) sel.hidden=true; return; }
      if(!sel){
        sel=document.createElement('select'); sel.id='savedAddr'; sel.className='saved-addr'; sel.setAttribute('aria-label','בחירת כתובת שמורה');
        box.insertBefore(sel,$('shipAddr'));
        sel.addEventListener('change',()=>{const a=profile.addresses.find(x=>x.id===sel.value); if(a){$('shipAddr').value=a.text;$('shipAddr').dispatchEvent(new Event('input'));}});
      }
      sel.hidden=false;
      sel.innerHTML='<option value="">כתובת שמורה…</option>'+profile.addresses.map(a=>`<option value="${esc(a.id)}">${esc(a.label||'כתובת')}</option>`).join('');
      if(!$('shipAddr').value.trim()){
        const a=profile.addresses.find(x=>x.id===profile.defaultAddr)||profile.addresses[0];
        if(a){ $('shipAddr').value=a.text; sel.value=a.id; $('shipAddr').dispatchEvent(new Event('input')); }
      }
    }

    /* --- checkout: keep a copy of the order in the account --- */
    function refreshOrderNo(){ acct.orderNo=user?newOrderNo():null; renderCart(); }
    acct.checkout=()=>{
      if(!user||!db||!acct.orderNo) return;
      const id=acct.orderNo, t=totals(), uid=user.uid;
      db.collection('orders').doc(id).set({
        uid, email:user.email||'', name:profile.name||user.displayName||'', phone:profile.phone||'',
        items:slimCart(), subtotal:Math.round(t.sub), discount:Math.round(t.disc), coupon:coupon||null, total:Math.round(t.total),
        address:$('shipAddr').value.trim().slice(0,300), status:'received', createdAt:fb.firestore.FieldValue.serverTimestamp()
      }).then(()=>toast('ההזמנה '+id+' נשמרה באזור האישי')).catch(()=>toast('ההזמנה נשלחה בוואטסאפ, אבל לא נשמרה באזור האישי'));
      setTimeout(refreshOrderNo,0);
    };

    /* --- favorites --- */
    function paintFavButtons(){
      document.querySelectorAll('.pfav').forEach(b=>{
        const on=!!user&&profile.favorites.includes(b.dataset.id);
        b.setAttribute('aria-pressed',String(on));
        b.setAttribute('aria-label',(on?'הסרה מהמועדפים: ':'הוספה למועדפים: ')+b.dataset.name);
      });
    }
    function toggleFav(id){
      if(!user){ openLogin('כדי לשמור מוצרים במועדפים, היכנסו לחשבון.'); return; }
      const on=profile.favorites.includes(id);
      profile.favorites=on?profile.favorites.filter(x=>x!==id):[...profile.favorites,id];
      paintFavButtons(); renderAccount();
      const FV=fb.firestore.FieldValue;
      db.collection('users').doc(user.uid).set({favorites:on?FV.arrayRemove(id):FV.arrayUnion(id),updatedAt:FV.serverTimestamp()},{merge:true})
        .then(()=>toast(on?'הוסר מהמועדפים':'נשמר במועדפים'))
        .catch(()=>{ profile.favorites=on?[...profile.favorites,id]:profile.favorites.filter(x=>x!==id); paintFavButtons(); renderAccount(); toast('לא הצלחנו לשמור. נסו שוב.'); });
    }
    document.addEventListener('click',e=>{const b=e.target.closest('.pfav'); if(!b) return; e.stopPropagation(); toggleFav(b.dataset.id);},true);

    /* --- orders --- */
    function watchOrders(){
      if(unsubOrders){unsubOrders();unsubOrders=null;}
      if(!user) return;
      ordersState='loading'; renderAccount();
      unsubOrders=db.collection('orders').where('uid','==',user.uid).onSnapshot(qs=>{
        orders=qs.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>((b.createdAt&&b.createdAt.toMillis?b.createdAt.toMillis():Infinity)-(a.createdAt&&a.createdAt.toMillis?a.createdAt.toMillis():Infinity)));
        ordersState='ready'; renderAccount();
      },()=>{ordersState='error';renderAccount();});
    }

    /* --- account page --- */
    function renderAccount(){
      if(route!=='account') return;
      const state=$('accState'), main=$('accMain');
      const showState=html=>{state.innerHTML=html;state.hidden=false;main.hidden=true;};
      if(!CFG||!CFG.apiKey) return showState('<div class="panel acc-state"><h2 class="carved">האזור האישי בדרך</h2><p class="muted">בקרוב תוכלו לשמור כאן הזמנות, כתובות ומועדפים.</p><a class="btn btn-ghost" href="#collection">חזרה לקולקציה</a></div>');
      if(bootError) return showState('<div class="panel acc-state"><h2 class="carved">לא הצלחנו להתחבר</h2><p class="muted">בדקו את החיבור לאינטרנט ורעננו את הדף.</p></div>');
      if(!auth) return showState('<div class="panel acc-state"><p class="muted">טוען…</p></div>');
      if(!user){
        showState('<div class="panel acc-state"><h2 class="carved">היכנסו לאזור האישי</h2><p class="muted">ההזמנות, הכתובות והמועדפים שלכם, בכל מכשיר. נכנסים עם קישור שנשלח למייל, בלי סיסמה.</p><button class="btn btn-primary" type="button" id="accLogin">כניסה לחשבון</button></div>');
        $('accLogin').addEventListener('click',()=>openLogin());
        return;
      }
      state.hidden=true; main.hidden=false;
      $('accHello').textContent='שלום'+(profile.name?', '+profile.name.split(/\s+/)[0]:'');
      $('accEmail').textContent=user.email||'';
      $('adminLink').hidden=!isAdmin();
      if(document.activeElement!==$('accName')) $('accName').value=profile.name||'';
      if(document.activeElement!==$('accPhone')) $('accPhone').value=profile.phone||'';
      const ol=$('accOrders');
      if(ordersState==='loading') ol.innerHTML='<li class="muted">טוען הזמנות…</li>';
      else if(ordersState==='error') ol.innerHTML='<li class="muted">לא הצלחנו לטעון את ההזמנות. רעננו את הדף.</li>';
      else if(!orders.length) ol.innerHTML='<li class="muted">עוד אין הזמנות. הזמנה שתשלחו מהסל תופיע כאן, עם הסטטוס שלה.</li>';
      else ol.innerHTML=orders.map(o=>{
        const st=STATUS[o.status]?o.status:'received';
        const items=(o.items||[]).map(i=>`${esc(i.name)} × ${i.qty|0}`).join(' · ');
        return `<li class="order"><div class="top"><span class="no">${esc(o.id)}</span><span class="status ${st}">${STATUS[st]}</span></div>
          <p class="items">${items}</p><div class="top"><span class="when">${when(o.createdAt)}</span><span class="sum">₪${fmt(o.total|0)}</span></div></li>`;
      }).join('');
      const al=$('accAddrs');
      al.innerHTML=profile.addresses.length?profile.addresses.map(a=>`<li><b>${esc(a.label||'כתובת')}</b><span>${esc(a.text)}</span>
        <div class="row-actions">${profile.defaultAddr===a.id?'<span class="def">ברירת מחדל</span>':`<button type="button" data-def="${esc(a.id)}">קבע כברירת מחדל</button>`}<button type="button" data-del="${esc(a.id)}">מחיקה</button></div></li>`).join(''):'<li class="muted" style="border:0;padding:0">עוד לא שמרתם כתובות.</li>';
      const fg=$('accFavs');
      const favs=profile.favorites.map(id=>PRODUCTS.find(p=>p.id===id)).filter(Boolean);
      fg.innerHTML=favs.length?favs.map(p=>`<div class="fav"><img src="${esc(p.images[0])}" alt="" loading="lazy"><div><b>${esc(p.name)}</b><span class="p">${p.price?'₪'+fmt(p.price):'מחיר לפי הזמנה'}</span>
        <div class="acts">${p.price?`<button type="button" data-add="${esc(p.id)}">הוספה לסל</button>`:''}<button type="button" class="rm" data-unfav="${esc(p.id)}">הסרה</button></div></div></div>`).join(''):'<p class="muted">לחצו על הלב בכרטיס מוצר כדי לשמור אותו כאן.</p>';
    }
    $('accAddrs').addEventListener('click',e=>{
      const def=e.target.closest('[data-def]'), del=e.target.closest('[data-del]');
      if(def){ profile.defaultAddr=def.dataset.def; saveProfile({defaultAddr:profile.defaultAddr},'כתובת ברירת המחדל עודכנה'); }
      if(del){ profile.addresses=profile.addresses.filter(a=>a.id!==del.dataset.del); if(profile.defaultAddr===del.dataset.del) profile.defaultAddr=profile.addresses[0]?profile.addresses[0].id:null; saveProfile({addresses:profile.addresses,defaultAddr:profile.defaultAddr},'הכתובת נמחקה'); }
    });
    $('accFavs').addEventListener('click',e=>{
      const add=e.target.closest('[data-add]'), un=e.target.closest('[data-unfav]');
      if(add){ const p=PRODUCTS.find(x=>x.id===add.dataset.add); if(p) addToCart(p,'phys',p.price); }
      if(un) toggleFav(un.dataset.unfav);
    });
    function saveProfile(patch,done){
      if(!user) return;
      renderAccount(); paintLoginBtn(); paintSavedAddr();
      db.collection('users').doc(user.uid).set({...patch,updatedAt:fb.firestore.FieldValue.serverTimestamp()},{merge:true})
        .then(()=>done&&toast(done)).catch(()=>toast('לא הצלחנו לשמור. נסו שוב.'));
    }
    $('accForm').addEventListener('submit',e=>{
      e.preventDefault();
      profile.name=$('accName').value.trim().slice(0,80); profile.phone=$('accPhone').value.trim().slice(0,20);
      saveProfile({name:profile.name,phone:profile.phone},'הפרטים נשמרו');
    });
    $('addrForm').addEventListener('submit',e=>{
      e.preventDefault();
      const text=$('addrText').value.trim().slice(0,200), label=$('addrLabel').value.trim().slice(0,30);
      if(!text){ toast('כתבו כתובת מלאה לפני השמירה'); $('addrText').focus(); return; }
      if(profile.addresses.length>=10){ toast('אפשר לשמור עד 10 כתובות'); return; }
      const a={id:Math.random().toString(36).slice(2,10),label:label||'כתובת',text};
      profile.addresses=[...profile.addresses,a]; if(!profile.defaultAddr) profile.defaultAddr=a.id;
      $('addrText').value=''; $('addrLabel').value='';
      saveProfile({addresses:profile.addresses,defaultAddr:profile.defaultAddr},'הכתובת נשמרה');
    });
    $('logoutBtn').addEventListener('click',()=>{ if(auth) auth.signOut().then(()=>{toast('התנתקתם מהחשבון');location.hash='#/';}); });

    /* --- admin: order statuses --- */
    function renderAdmin(){
      if(route!=='admin'){ if(unsubAdmin){unsubAdmin();unsubAdmin=null;} return; }
      const body=$('adminBody');
      if(!auth||!user){ body.innerHTML='<div class="panel acc-state"><p class="muted">היכנסו עם חשבון המנהל כדי לראות הזמנות.</p></div>'; return; }
      if(!isAdmin()){ body.innerHTML='<div class="panel acc-state"><p class="muted">לחשבון הזה אין הרשאת ניהול.</p></div>'; return; }
      if(unsubAdmin) return;
      body.innerHTML='<p class="muted">טוען הזמנות…</p>';
      unsubAdmin=db.collection('orders').orderBy('createdAt','desc').limit(200).onSnapshot(qs=>{
        if(!qs.size){ body.innerHTML='<div class="panel acc-state"><p class="muted">עוד אין הזמנות שמורות.</p></div>'; return; }
        body.innerHTML=`<div class="panel admin-wrap"><table class="admin-table"><thead><tr><th>הזמנה</th><th>תאריך</th><th>לקוח</th><th>פריטים</th><th>סה״כ</th><th>סטטוס</th></tr></thead><tbody>${qs.docs.map(d=>{const o=d.data();const st=STATUS[o.status]?o.status:'received';
          return `<tr><td class="num">${esc(d.id)}</td><td class="num">${when(o.createdAt)}</td><td>${esc(o.name||'')}<br><span class="muted">${esc(o.phone||'')} ${esc(o.email||'')}</span><br><span class="muted">${esc(o.address||'')}</span></td>
          <td>${(o.items||[]).map(i=>`${esc(i.name)} × ${i.qty|0}`).join('<br>')}</td><td class="num">₪${fmt(o.total|0)}</td>
          <td><select data-order="${esc(d.id)}" aria-label="סטטוס הזמנה ${esc(d.id)}">${Object.entries(STATUS).map(([k,v])=>`<option value="${k}"${k===st?' selected':''}>${v}</option>`).join('')}</select></td></tr>`;}).join('')}</tbody></table></div>`;
      },()=>{ body.innerHTML='<div class="panel acc-state"><p class="muted">אין הרשאה לקרוא את ההזמנות. בדקו את כללי האבטחה ב־Firebase.</p></div>'; unsubAdmin=null; });
    }
    $('adminBody').addEventListener('change',e=>{
      const s=e.target.closest('select[data-order]'); if(!s) return;
      db.collection('orders').doc(s.dataset.order).update({status:s.value,updatedAt:fb.firestore.FieldValue.serverTimestamp()})
        .then(()=>toast('הסטטוס עודכן')).catch(()=>toast('לא הצלחנו לעדכן את הסטטוס'));
    });

    acct.onRoute=r=>{ route=r; renderAccount(); renderAdmin(); };

    /* --- sign-in flows --- */
    const AUTH_ERR={'auth/popup-closed-by-user':'','auth/cancelled-popup-request':'','auth/invalid-email':'כתובת הדוא״ל לא תקינה.','auth/operation-not-allowed':'שיטת הכניסה הזו עוד לא הופעלה.','auth/unauthorized-domain':'הכתובת של האתר עוד לא אושרה בשירות הכניסה.','auth/unauthorized-continue-uri':'הכתובת של האתר עוד לא אושרה בשירות הכניסה.','auth/invalid-action-code':'קישור הכניסה לא תקף או שכבר נוצל. בקשו קישור חדש.','auth/expired-action-code':'תוקף קישור הכניסה פג. בקשו קישור חדש.','auth/too-many-requests':'יותר מדי ניסיונות. נסו שוב בעוד כמה דקות.','auth/network-request-failed':'אין חיבור לאינטרנט. נסו שוב.'};
    const errText=e=>(e&&e.code in AUTH_ERR)?AUTH_ERR[e.code]:'משהו השתבש בכניסה. נסו שוב.';
    $('googleLogin').addEventListener('click',async()=>{
      if(!auth){ openLogin(); return; }
      say('פותח את חלון Google…');
      try{ await auth.signInWithPopup(new fb.auth.GoogleAuthProvider()); }
      catch(e){
        if(e&&(e.code==='auth/popup-blocked'||e.code==='auth/operation-not-supported-in-this-environment')){ auth.signInWithRedirect(new fb.auth.GoogleAuthProvider()); return; }
        const t=errText(e); say(t,t?'bad':'');
      }
    });
    $('emailLinkForm').addEventListener('submit',async e=>{
      e.preventDefault();
      if(!auth){ openLogin(); return; }
      const email=$('loginEmail').value.trim();
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ say('כתבו כתובת דוא״ל תקינה.','bad'); $('loginEmail').focus(); return; }
      try{
        if(completingLink){
          say('משלים כניסה…');
          await auth.signInWithEmailLink(email,location.href);
          completingLink=false; cleanLinkUrl();
        }else{
          say('שולח…');
          await auth.sendSignInLinkToEmail(email,{url:location.origin+'/?login=link',handleCodeInApp:true});
          try{localStorage.setItem('ob-login-email',email);}catch(err){}
          say('שלחנו קישור כניסה ל־'+email+'. פתחו את המייל במכשיר הזה ולחצו על הקישור. לא מוצאים? בדקו גם בספאם.','ok');
        }
      }catch(err){ say(errText(err)||'משהו השתבש. נסו שוב.','bad'); }
    });
    function cleanLinkUrl(){ try{history.replaceState(null,'',location.pathname+'#/account');}catch(e){} dispatchEvent(new HashChangeEvent('hashchange')); }

    async function onUser(u){
      user=u||null;
      if(unsubOrders){unsubOrders();unsubOrders=null;}
      if(unsubAdmin){unsubAdmin();unsubAdmin=null;}
      orders=[]; ordersState='idle';
      if(!user){
        profile={name:'',phone:'',addresses:[],defaultAddr:null,favorites:[]};
        paintLoginBtn(); paintFavButtons(); paintSavedAddr(); refreshOrderNo(); renderAccount(); renderAdmin();
        return;
      }
      if(dlg.open){ dlg.close(); toast('נכנסתם לחשבון'); }
      const ref=db.collection('users').doc(user.uid);
      let data={};
      try{ const snap=await ref.get(); data=snap.exists?snap.data():null; }
      catch(e){ data={}; toast('לא הצלחנו לטעון את פרטי החשבון. נסו לרענן.'); }
      const FV=fb.firestore.FieldValue;
      if(data===null){
        data={};
        ref.set({email:user.email||'',name:user.displayName||'',phone:'',addresses:[],favorites:[],cart:slimCart(),createdAt:FV.serverTimestamp(),updatedAt:FV.serverTimestamp()}).catch(()=>{});
      }
      profile={
        name:String(data.name||user.displayName||''), phone:String(data.phone||''),
        addresses:Array.isArray(data.addresses)?data.addresses.filter(a=>a&&a.id&&a.text):[],
        defaultAddr:data.defaultAddr||null,
        favorites:Array.isArray(data.favorites)?data.favorites.map(String):[]
      };
      mergeRemoteCart(data.cart); saveCartSoon();
      paintLoginBtn(); paintFavButtons(); paintSavedAddr(); refreshOrderNo(); watchOrders(); renderAccount(); renderAdmin();
    }

    async function boot(){
      paintLoginBtn();
      if(!CFG||!CFG.apiKey){ renderAccount(); return; }
      try{
        await loadScript(SDK+'firebase-app-compat.js');
        await Promise.all([loadScript(SDK+'firebase-auth-compat.js'),loadScript(SDK+'firebase-firestore-compat.js')]);
        fb=window.firebase; fb.initializeApp(CFG);
        auth=fb.auth(); auth.languageCode='he'; db=fb.firestore();
      }catch(e){ bootError=true; renderAccount(); renderAdmin(); return; }
      auth.getRedirectResult().catch(e=>{const t=errText(e); if(t) toast(t);});
      if(auth.isSignInWithEmailLink(location.href)){
        let email=null; try{email=localStorage.getItem('ob-login-email');}catch(e){}
        if(email){
          try{ await auth.signInWithEmailLink(email,location.href); try{localStorage.removeItem('ob-login-email');}catch(e){} }
          catch(e){ toast(errText(e)||'קישור הכניסה לא תקף. בקשו קישור חדש.'); }
          cleanLinkUrl();
        }else{ completingLink=true; openLogin(); }
      }
      auth.onAuthStateChanged(onUser);
    }
    boot();
  })();

'''

RULES = r'''rules_version = '2';
// Firestore security rules for Or Bereshit.
// Paste into Firebase console → Firestore Database → Rules, then Publish.
// Keep the admin list in sync with OB_ADMIN_EMAILS in firebase-config.js.
service cloud.firestore {
  match /databases/{database}/documents {
    function signedIn() { return request.auth != null; }
    function isAdmin() {
      return signedIn()
        && request.auth.token.email_verified == true
        && request.auth.token.email.lower() in ['roibenshimoul9@gmail.com'];
    }

    // One document per customer: details, saved addresses, favorites and synced cart.
    match /users/{uid} {
      allow read: if signedIn() && (request.auth.uid == uid || isAdmin());
      allow create, update: if signedIn() && request.auth.uid == uid
        && request.resource.data.keys().hasOnly(['email','name','phone','addresses','defaultAddr','favorites','cart','createdAt','updatedAt'])
        && (!('addresses' in request.resource.data) || request.resource.data.addresses.size() <= 10)
        && (!('favorites' in request.resource.data) || request.resource.data.favorites.size() <= 100)
        && (!('cart' in request.resource.data) || request.resource.data.cart.size() <= 50);
      allow delete: if signedIn() && request.auth.uid == uid;
    }

    // Orders are written once by the customer at checkout; only the admin changes the status.
    match /orders/{orderId} {
      allow create: if signedIn()
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.status == 'received'
        && request.resource.data.createdAt == request.time
        && request.resource.data.items is list
        && request.resource.data.items.size() > 0
        && request.resource.data.items.size() <= 50
        && request.resource.data.total is number
        && request.resource.data.keys().hasOnly(['uid','email','name','phone','items','subtotal','discount','coupon','total','address','status','createdAt']);
      allow read: if signedIn() && (resource.data.uid == request.auth.uid || isAdmin());
      allow update: if isAdmin()
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['status','updatedAt'])
        && request.resource.data.status in ['received','printing','shipped','delivered','cancelled'];
      allow delete: if false;
    }
  }
}
'''

CONFIG_JS = r'''// Firebase web config for Or Bereshit.
// These values identify the Firebase project and are public by design; access to data is
// protected by the Firestore security rules (firestore.rules) and the authorized domains list.
// Paste the object from Firebase console → Project settings → Your apps → Web app → Config.
window.FIREBASE_CONFIG = null;
/* example:
window.FIREBASE_CONFIG = {
  apiKey: "...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "...",
  appId: "..."
};
*/

// Accounts that see the admin page (#/admin). Keep in sync with isAdmin() in firestore.rules.
window.OB_ADMIN_EMAILS = ['roibenshimoul9@gmail.com'];
'''


def apply(page):
    def rep(a, b, count=1):
        nonlocal page
        n = page.count(a)
        assert n == count, (a[:70], n)
        page = page.replace(a, b)

    # config script before any page script
    rep('<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n',
        '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n<script src="/firebase-config.js"></script>\n')

    # styles
    rep('/* ---------- drawer / dialog / toast ---------- */', CSS + '\n/* ---------- drawer / dialog / toast ---------- */')

    # login dialog: real sign-in instead of the demo form
    i = page.index('<dialog id="loginDlg">'); j = page.index('</dialog>', i) + len('</dialog>')
    page = page[:i] + LOGIN_DIALOG + page[j:]

    # account + admin pages
    rep('  <!-- ===== support ===== -->', PAGES + '\n  <!-- ===== support ===== -->')

    # favorite heart on each product card
    rep("el.className='pcard rv'; el.dataset.cat=p.cat;", "el.className='pcard rv'; el.dataset.cat=p.cat; el.dataset.id=p.id;")
    rep('<div class="ptools"><button class="ptool pexpand"',
        '<div class="ptools"><button class="ptool pfav" type="button" aria-pressed="false" data-id="${esc(p.id)}" data-name="${esc(p.name)}" aria-label="הוספה למועדפים: ${esc(p.name)}">' + HEART + '</button><button class="ptool pexpand"')

    # hooks the account layer fills in
    rep("  const persist=()=>{try{localStorage.setItem(STORE,JSON.stringify({cart,coupon}));}catch(e){}};",
        "  const acct={cartChanged(){},checkout(){},onRoute(){},openLogin(){},orderNo:null};\n"
        "  const persist=()=>{try{localStorage.setItem(STORE,JSON.stringify({cart,coupon}));}catch(e){} acct.cartChanged();};")
    rep("    return ['שלום אור בראשית, אשמח להזמין:',...rows,'',",
        "    return ['שלום אור בראשית, אשמח להזמין:',...(acct.orderNo?['מספר הזמנה: '+acct.orderNo]:[]),...rows,'',")
    rep("    if(cart.some(l=>l.type==='phys')&&!$('shipAddr').value.trim()){e.preventDefault();toast('הוסיפו כתובת למשלוח לפני שליחת ההזמנה');$('shipAddr').focus();}\n  });",
        "    if(cart.some(l=>l.type==='phys')&&!$('shipAddr').value.trim()){e.preventDefault();toast('הוסיפו כתובת למשלוח לפני שליחת ההזמנה');$('shipAddr').focus();return;}\n    acct.checkout();\n  });")

    # the old demo login script goes away
    i = page.index('  /* ---------- login ---------- */'); j = page.index('  /* ---------- engraving ---------- */', i)
    page = page[:i] + page[j:]

    # account module sits with the other feature modules, before the router
    rep('  /* ---------- pages ---------- */', JS + '  /* ---------- pages ---------- */')

    # router knows the new pages and tells the account module where we are
    rep("const ROUTES=['support','guide','specials','licenses','privacy','shipping','returns'];",
        "const ROUTES=['support','guide','specials','licenses','privacy','shipping','returns','account','admin'];")
    rep("returns:'החזרות וביטולים'};", "returns:'החזרות וביטולים',account:'האזור האישי',admin:'ניהול הזמנות'};")
    rep("      document.title=isPage?`${TITLES[r]} · אור בראשית`:'אור בראשית';",
        "      document.title=isPage?`${TITLES[r]} · אור בראשית`:'אור בראשית';\n      acct.onRoute(r);")

    # the assistant can open the account page too
    rep("returns:'#/returns'};", "returns:'#/returns',account:'#/account'};")
    return page

/* 服务内容发布后同步前台；原型配置仅保存于当前浏览器。 */
(() => {
  const defaults = window.CSU_SERVICE_DEFAULTS;
  const context = window.CSU_SERVICE_CONTEXT;
  if (!defaults || !context) return;
  const storageKey = 'csu-prototype-service-content-v1';
  const carryPrefix = '后勤服务展示配置：';
  const copy = x => JSON.parse(JSON.stringify(x));
  const query = new URLSearchParams(location.search);
  const icons = ['fa-screwdriver-wrench','fa-comments','fa-person-swimming','fa-file-lines','fa-bus','fa-hotel','fa-newspaper','fa-magnifying-glass','fa-bolt','fa-bullhorn','fa-utensils'];
  let state = copy(defaults);
  function load() {
    let saved;
    try { saved = JSON.parse(localStorage.getItem(storageKey) || 'null'); } catch (_) {}
    try {
      if (window.name.startsWith(carryPrefix)) {
        const carried = JSON.parse(window.name.slice(carryPrefix.length));
        if (!saved || (carried.updated || 0) > (saved.updated || 0)) saved = carried;
      }
    } catch (_) {}
    state = { ...copy(defaults), ...saved, display: { ...defaults.display, ...(saved?.display || {}) }, services: { ...copy(defaults.services), ...(saved?.services || {}) } };
    Object.keys(state.services).forEach(id=>{state.services[id]={entryType:'web',miniProgramShare:'',miniProgramUrl:'',miniProgramCode:'',miniProgramCodeName:'',...(defaults.services[id]||{}),...state.services[id]};});
  }
  function save() {
    state.updated = Date.now();
    try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {}
    try {window.name = carryPrefix + JSON.stringify(state);}catch(_){}
  }
  function el(tag, text, cls) {
    const n = document.createElement(tag);
    if (text !== undefined && text !== null) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  }
  function icon(name) { const n = el('i', null, 'fa-solid ' + (icons.includes(name) ? name : name === 'fa-arrow-up-right-from-square' ? name : name === 'fa-circle-info' ? name : 'fa-circle-info')); n.setAttribute('aria-hidden','true'); return n; }
  function anchor(text, href, cls = 'btn') { const n = el('a', text, cls); n.href = href; return n; }
  function badge(text, cls = '') { return el('span', text, 'badge ' + cls); }
  function note(text) { const n=el('div',null,'note service-content-notice'); n.append(icon('fa-circle-info'),el('div',text)); return n; }
  function card(title) { const n=el('section',null,'card'); if(title)n.append(el('h2',title)); return n; }
  function heading(title, subtitle, action) { const n=el('div',null,'page-heading');const h=el('div');h.append(el('div','中南大学 · 智慧后勤','eyebrow'),el('h1',title),el('p',subtitle));n.append(h);if(action)n.append(action);return n; }
  function details(items) { const n=el('dl',null,'summary-list');items.forEach(([label,text])=>{const r=el('div');r.append(el('dt',label),el('dd',text));n.append(r);});return n; }
  function validURL(value) { try { const u=new URL(value);return ['http:','https:'].includes(u.protocol)?u.href:''; } catch(_){return '';} }
  function miniProgramURL(value) {
    try {const u=new URL((value||'').trim());if(u.protocol==='https:')return u.href;if(u.protocol==='weixin:'&&u.hostname==='dl'&&u.pathname==='/business/'&&u.searchParams.get('t'))return u.href;}catch(_){}return '';
  }
  function codeImageURL(value) {
    if(!value)return '';if(/^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+$/.test(value))return value;
    try{const u=new URL(value,location.href);if(u.protocol==='https:'||(u.origin===location.origin&&['http:','file:'].includes(u.protocol)))return u.href;}catch(_){}return '';
  }
  function endpoint(s, port) { if(s.terminal==='无地址，仅文字说明')return '';if(port==='pc'&&s.terminal==='仅手机')return '';if(port==='mobile'&&s.terminal==='仅电脑')return '';return validURL(s[port]||''); }
  function allowed(s, role=context.role) { if(role==='visitor'||role==='admin'||s.who==='全部用户（说明）'||s.who==='学生、教职工')return true;return role==='student'?s.who==='学生':role==='staff'?s.who==='教职工':false; }
  function label(s) { if(s.entryType==='miniprogram')return '手机微信';return ({'电脑与手机分别配置':'电脑、手机','仅电脑':'仅电脑','仅手机':'仅手机','无地址，仅文字说明':'办事说明'})[s.terminal]||s.terminal; }
  function guideURL(s) { if(context.role==='visitor')return 'login-required.html?intent=service&service='+encodeURIComponent(s.id);return defaults.services[s.id]?s.id+'.html':'service-guide.html?service='+encodeURIComponent(s.id); }
  function current(fallback='repair') { return state.services[query.get('service')||fallback]; }
  function actionFor(s, port) {
    if(s.entryType==='miniprogram')return port==='mobile'?[s.buttonText||'打开校内送餐',miniProgramURL(s.miniProgramUrl)||'mini-program-handoff.html?service='+encodeURIComponent(s.id)]:[s.qrButtonText||'微信扫码打开','mini-program.html?service='+encodeURIComponent(s.id)];
    if(endpoint(s,port)) return [s.buttonText,'service-handoff.html?service='+encodeURIComponent(s.id)];
    if(port==='pc'&&endpoint(s,'mobile'))return [s.qrButtonText,'service-mobile.html?service='+encodeURIComponent(s.id)];
    return ['查看替代渠道','service-unavailable.html?service='+encodeURIComponent(s.id)];
  }
  function blocked(host,s) {
    host.replaceChildren(heading(state.display.guideTitle,state.display.guideSubtitle));
    const c=card(!s?'未找到这项服务':!s.enabled?'服务暂未开放':'当前身份暂不可使用此服务');
    c.append(el('p',!s?'该服务可能尚未发布，请返回服务大厅选择已开放的服务。':!s.enabled?'服务当前已停用，请查看其他服务或联系后勤了解办理方式。':'服务根据适用对象展示，请使用相应校园身份查看办理入口。'),anchor('返回服务大厅','services.html','btn primary'));
    host.append(c);
  }
  function guide(s,port,{preview=false}={}) {
    const root=el('div',null,'service-config-guide');
    if(!preview&&(!s||!s.enabled||!allowed(s))){blocked(root,s);return root;}
    root.append(heading(state.display.guideTitle,state.display.guideSubtitle,preview?null:anchor('全部服务','services.html','btn sm')));
    const split=el('div',null,'split-detail');const left=el('div'),right=el('div');const body=card();
    const banner=el('div',null,'detail-banner'),si=el('div',null,'service-icon'),title=el('div');si.append(icon(s.icon));title.append(el('h1',s.name),el('p',s.summary));banner.append(si,title);
    body.append(banner,el('p',s.detail,'service-content-body'),el('hr',null,'divider'),el('h2','办理步骤'));
    const list=el('div',null,'steps');(s.steps||[]).forEach((step,i)=>{const r=el('div',null,'service-content-step'),t=el('div');t.append(el('h3',step.title),el('p',step.text));r.append(el('span',String(i+1)),t);list.append(r);});body.append(list);left.append(body);
    const info=card('办理信息');info.append(details([['适用对象',s.who],['办理渠道',s.channel],['终端支持',label(s)]]));
    const [text,href]=actionFor(s,port),actions=el('div',null,'actions');actions.style.marginTop='22px';
    if(preview){const b=el('button',text,'btn primary');b.type='button';b.disabled=true;actions.append(b);}else actions.append(anchor(text,href,'btn primary'));
    if(s.entryType==='miniprogram'&&port==='pc'){info.append(miniProgramCodeImage(s),el('p','打开手机微信扫一扫，扫描上方小程序码。','muted'));}info.append(actions);if(preview&&s.entryType==='miniprogram'){const detail=el('div',null,'mini-config-preview');detail.append(el('strong','移动端跳转地址'),el('p',miniProgramURL(s.miniProgramUrl)||'待配置；当前展示跳转演示页'),el('strong','微信小程序分享口令'),el('p',s.miniProgramShare||'未配置备用口令')); info.append(detail);}right.append(info,note(s.notice));split.append(left,right);root.append(split);return root;
  }
  function renderCatalog() {
    const host=document.querySelector('[data-service-catalog]');if(!host)return;
    const previous=host.querySelector('#service-catalog-search')?.value||'';
    host.replaceChildren(heading(state.display.hallTitle,state.display.hallSubtitle));
    const filters=el('div',null,'filters'),input=el('input');input.id='service-catalog-search';input.placeholder=state.display.searchPlaceholder;input.setAttribute('aria-label','搜索服务');input.value=previous;filters.append(input);
    const grid=el('div',null,'grid3'),empty=el('div','暂无匹配服务，请换一个关键词或联系后勤。','card empty');grid.id='service-catalog-grid';empty.id='service-catalog-empty';
    const draw=()=>{grid.replaceChildren();let found=0;Object.values(state.services).sort((a,b)=>a.sort-b.sort).filter(s=>s.enabled&&s.showInHall&&allowed(s)).forEach(s=>{
      if(!(s.name+s.summary+s.category+s.triggers).includes(input.value.trim()))return;
      found++;const a=anchor('',guideURL(s),'service-card'),si=el('div',null,'service-icon');si.append(icon(s.icon));a.append(si,el('h3',s.name),el('p',s.summary),badge(s.tag));grid.append(a);
    });empty.hidden=found>0;};input.addEventListener('input',draw);host.append(filters,grid,empty);draw();
  }
  function miniProgramCodeImage(s) {
    const src=codeImageURL(s.miniProgramCode);
    if(!src)return el('p','小程序码待配置，请使用备用打开方式。','mini-code-empty');
    const image=el('img');image.src=src;image.alt=s.name+'微信小程序码';image.className='mini-program-code';
    image.addEventListener('error',()=>{image.hidden=true;image.after(el('p','小程序码暂时无法显示，请使用备用打开方式。'));});return image;
  }
  function miniProgramPanel(s, {preview=false, port=context.port}={}) {
    const root=el('div',null,'mini-program-grid');
    const main=card(),hero=el('div',null,'mini-program-hero'),mark=el('div',null,'service-icon'),intro=el('div');
    mark.append(icon(s.icon));intro.append(el('h2',s.name),el('p',s.channel));hero.append(mark,intro);main.append(hero);
    if(port==='mobile'){
      main.append(el('h2','一键前往校内送餐'),el('p','点击下方按钮，在小程序中选择餐品、确认配送地址并下单。'));
      if(preview){const b=el('button',s.buttonText||'打开校内送餐','btn primary');b.type='button';b.disabled=true;main.append(b);}
      else main.append(anchor(s.buttonText||'打开校内送餐',miniProgramURL(s.miniProgramUrl)||'mini-program-handoff.html?service='+encodeURIComponent(s.id),'btn primary'));
      main.append(el('p',miniProgramURL(s.miniProgramUrl)?'即将前往已配置的小程序地址，相关服务由美团提供。':'当前为跳转效果演示，正式小程序地址将由管理员配置。','muted'),el('hr',null,'divider'));
    }
    main.append(el('h2',port==='pc'?'备用打开方式':'也可以使用分享口令'),el('p','复制口令，在微信聊天中粘贴发送，再点击识别的小程序卡片。'));
    const label=el('label','小程序分享口令'),field=el('textarea',null,'mini-share-field');
    field.id='mini-program-share-'+port;label.htmlFor=field.id;field.value=s.miniProgramShare||'';field.readOnly=true;field.rows=3;field.setAttribute('aria-label','小程序分享口令');main.append(label,field);
    const actions=el('div',null,'actions'),button=el('button','复制小程序口令','btn'),status=el('p','复制后，请切换到微信继续操作。','mini-copy-status');
    button.type='button';button.disabled=preview||!s.miniProgramShare;status.setAttribute('role','status');status.setAttribute('aria-live','polite');
    if(!preview)button.addEventListener('click',async()=>{
      try {
        if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(field.value);
        else {field.focus();field.select();if(!document.execCommand('copy'))throw new Error('复制未完成');}
        button.textContent='已复制小程序口令';status.textContent='已复制。请打开微信，将口令粘贴到聊天中并发送。';
      }catch(_){field.focus();field.select();status.textContent='暂时无法自动复制，已选中口令，请长按或使用复制快捷键手动复制。';}
    });
    actions.append(button);main.append(actions,status);
    if(port==='pc'){
      const qr=card('微信扫码，打开校内送餐');qr.classList.add('mini-qr-card');
      qr.append(el('p','使用手机微信“扫一扫”，扫描下方小程序码。'),miniProgramCodeImage(s),badge('美团外卖小程序','green'));
      const steps=el('ol',null,'mini-program-steps');['打开手机微信，点击右上角“扫一扫”。','扫描小程序码，在小程序中选择餐品。','核对校内收货地址的可配送范围后再下单。'].forEach(text=>steps.append(el('li',text)));
      qr.append(steps);root.append(qr,main);
    }else root.append(main);
    return root;
  }
  function renderMiniHandoff() {
    const host=document.querySelector('[data-miniprogram-handoff]');if(!host)return;
    const s=current('food-delivery');if(!s||!s.enabled||!allowed(s)){blocked(host,s);return;}
    host.replaceChildren(heading('前往'+s.name,'从后勤助手出发，在小程序中继续'));
    const c=card(),wrap=el('div',null,'mini-handoff'),symbol=el('div',null,'mini-handoff-symbol');symbol.append(icon(s.icon));wrap.append(symbol,badge('小程序跳转演示'),el('h1','即将打开'+s.name),el('p','正式地址配置后，移动端点击服务按钮即可前往对应小程序。'));
    const url=miniProgramURL(s.miniProgramUrl),actions=el('div',null,'actions');
    if(url){actions.append(anchor('继续前往小程序',url,'btn primary'));wrap.append(el('p','已配置正式跳转地址。','muted'));}
    else wrap.append(el('p','当前展示跳转效果，正式小程序地址待后续提供。','muted'));
    actions.append(anchor('返回送餐服务',guideURL(s),'btn'),anchor('查看备用打开方式','mini-program.html?service='+encodeURIComponent(s.id),'btn'));
    wrap.append(actions);c.append(wrap);host.append(c,note(s.notice));
  }
  function renderRoutes() {
    renderMiniHandoff();
    const miniHost=document.querySelector('[data-service-miniprogram]');
    if(miniHost){const s=current('food-delivery');if(!s||!s.enabled||!allowed(s)){blocked(miniHost,s);}else if(s.entryType!=='miniprogram'){miniHost.replaceChildren(heading('服务打开方式已更新',s.name),anchor('查看最新服务指引',guideURL(s),'btn primary'));}else{miniHost.replaceChildren(heading(s.name,context.port==='pc'?'使用手机微信扫码，前往小程序':'点击打开小程序，继续校内送餐',anchor('返回服务指引',guideURL(s),'btn sm')),miniProgramPanel(s),note(s.notice));}}
    document.querySelectorAll('[data-service-guide]').forEach(host=>{const id=host.dataset.serviceGuide;const s=state.services[id==='query'?(query.get('service')||'repair'):id];host.replaceChildren(guide(s,context.port));});
    const handoff=document.querySelector('[data-service-handoff]');
    if(handoff){const s=current(handoff.dataset.serviceHandoff||'repair');if(!s||!s.enabled||!allowed(s)){blocked(handoff,s);return;}
      const url=endpoint(s,context.port);handoff.replaceChildren(heading('即将前往官方服务','请在原业务系统内完成后续操作'));
      const c=card(s.name);c.append(details([['办理渠道',s.channel],['适用对象',s.who],['访问地址',url||'当前终端未配置可用地址'],['办理记录','在原业务系统查看']]));
      const actions=el('div',null,'actions');actions.style.marginTop='25px';if(url)actions.append(anchor('打开官方服务',url,'btn primary'));else{const [text,href]=actionFor(s,context.port);actions.append(anchor(text,href,'btn primary'));}actions.append(anchor('返回服务指引',guideURL(s)));c.append(actions);handoff.append(c,note(s.notice));
    }
    const qrHost=document.querySelector('[data-service-qr]');
    if(qrHost){const s=current('utility-pay');if(!s||!s.enabled||!allowed(s)){blocked(qrHost,s);return;}
      const url=endpoint(s,'mobile');qrHost.replaceChildren(heading(s.name+'，请在手机上办理',s.summary));const c=card('使用手机打开官方服务');
      if(url){const box=el('div',null,'service-qr');if(window.qrcode){try{const qr=qrcode(0,'M');qr.addData(url);qr.make();box.innerHTML=qr.createSvgTag({cellSize:5,margin:12,scalable:true});box.querySelector('svg')?.setAttribute('aria-label',s.name+'官方服务地址二维码');}catch(_){box.textContent='二维码暂时不可用，请在手机中打开下方地址。';}}else box.textContent='二维码暂时不可用，请在手机中打开下方地址。';
        const caption=el('p',url,'service-content-link');caption.style.textAlign='center';c.append(box,caption,el('p','扫码后，按原业务平台要求登录并完成办理。'));
      }else c.append(el('p','当前未配置可用的手机地址，请联系后勤了解办理方式。'));
      c.append(anchor('返回服务指引',guideURL(s)));qrHost.append(c,note(s.notice));
    }
    const unavailable=document.querySelector('[data-service-unavailable]');
    if(unavailable){const s=current('announcement');if(!s||!s.enabled||!allowed(s)){blocked(unavailable,s);return;}
      unavailable.replaceChildren(heading('换一种方式，继续办理',s.name));const c=card('当前终端暂未提供办理地址');c.append(el('p',s.fallbackText,'service-content-body'),el('p',s.detail,'service-content-body'));
      const actions=el('div',null,'actions');actions.append(anchor('联系后勤','contacts.html','btn primary'),anchor('返回服务指引',guideURL(s)));c.append(actions);unavailable.append(c,note(s.notice));
    }
  }
  function updateShortcuts() {
    if(context.role==='admin')return;
    document.querySelectorAll('a[href]').forEach(a=>{
      const url=new URL(a.getAttribute('href'),location.href);if(url.origin!==location.origin)return;
      const page=url.pathname.split('/').pop().replace(/\.html$/,'');
      const id=['login-required','service-guide','service-handoff','service-mobile','service-unavailable'].includes(page)?url.searchParams.get('service'):page;const s=state.services[id];if(!s)return;
      if(a.closest('.sidebar,.bottom-nav,.topbar'))return;
      a.hidden=!s.enabled||!allowed(s);if(a.hidden)return;
      if(context.role==='visitor')a.href=guideURL(s);
      if(a.matches('a.quick,.mini-apps a'))a.replaceChildren(icon(s.icon),document.createTextNode(s.name));
    });
    document.querySelectorAll('.quick-grid').forEach(grid=>{const count=[...grid.children].filter(a=>!a.hidden).length;grid.hidden=count===0;if(count)grid.style.gridTemplateColumns='repeat('+Math.min(5,count)+', minmax(0, 1fr))';});
  }
  function renderAdminList() {
    const host=document.querySelector('#admin-service-content-list');if(!host)return;
    const text=document.querySelector('#admin-service-search')?.value.trim()||'';host.replaceChildren();
    Object.values(state.services).sort((a,b)=>a.sort-b.sort).filter(s=>(s.name+s.category+s.who).includes(text)).forEach(s=>{
      const row=el('tr'),name=el('td');name.append(el('strong',s.name),el('p',s.summary));const status=el('td');status.append(badge(s.enabled?'启用':'停用',s.enabled?'green':'gray'));const operation=el('td');operation.append(anchor('配置内容','service-edit.html?service='+encodeURIComponent(s.id),'textlink'));row.append(name,el('td',s.category),el('td',s.who),status,el('td',String(s.sort)),operation);host.append(row);
    });
    if(!host.children.length){const tr=el('tr'),td=el('td','暂无匹配服务','service-admin-empty');td.colSpan=6;tr.append(td);host.append(tr);}
  }
  const collectSteps=()=>[...document.querySelectorAll('#service-steps-editor [data-service-step]')].map(row=>({title:row.querySelector('[data-step-title]').value.trim(),text:row.querySelector('[data-step-text]').value.trim()}));
  function drawSteps(steps) {
    const host=document.querySelector('#service-steps-editor');host.replaceChildren();
    steps.forEach((step,i)=>{
      const row=el('div',null,'service-step-edit');row.dataset.serviceStep='';const order=el('div',null,'service-step-order'),actions=el('div',null,'actions');order.append(el('strong','步骤 '+(i+1)));
      const control=(text,action,disabled=false)=>{const b=el('button',text,'btn sm');b.type='button';b.disabled=disabled;b.addEventListener('click',action);return b;};
      actions.append(control('上移',()=>{const data=collectSteps();[data[i-1],data[i]]=[data[i],data[i-1]];drawSteps(data);},i===0),control('下移',()=>{const data=collectSteps();[data[i+1],data[i]]=[data[i],data[i+1]];drawSteps(data);},i===steps.length-1),control('删除',()=>{const data=collectSteps();data.splice(i,1);drawSteps(data);},steps.length===1));order.append(actions);
      const titleField=el('div',null,'field'),titleLabel=el('label','步骤标题 *'),title=el('input');title.id='step-title-'+i;title.dataset.stepTitle='';titleLabel.htmlFor=title.id;title.value=step.title;title.maxLength=60;title.required=true;titleField.append(titleLabel,title);
      const bodyField=el('div',null,'field'),bodyLabel=el('label','步骤说明 *'),body=el('textarea');body.id='step-text-'+i;body.dataset.stepText='';bodyLabel.htmlFor=body.id;body.value=step.text;body.rows=3;body.required=true;body.maxLength=1000;bodyField.append(bodyLabel,body);row.append(order,titleField,bodyField);host.append(row);
    });
  }
  function setupMiniCodeUpload(form) {
    const picker=form.querySelector('#mini-code-upload'),value=form.querySelector('[name=miniProgramCode]'),name=form.querySelector('[name=miniProgramCodeName]'),preview=form.querySelector('#mini-code-preview'),error=form.querySelector('#mini-code-error'),filename=form.querySelector('#mini-code-filename');
    const draw=()=>{const src=codeImageURL(value.value);preview.hidden=!src;if(src)preview.src=src;else preview.removeAttribute('src');filename.textContent=name.value||'尚未上传小程序码';form.querySelector('#mini-code-remove').disabled=!value.value;};draw();
    let revision=0;
    picker.addEventListener('change',async()=>{
      const file=picker.files?.[0];if(!file)return;const currentRevision=++revision;error.textContent='';
      if(!['image/png','image/jpeg','image/webp'].includes(file.type)||file.size>1024*1024){error.textContent='请上传不超过1MB的PNG、JPG或WEBP小程序码图片。';picker.value='';return;}
      const submit=form.querySelector('[type=submit]');submit.disabled=true;
      try {
        const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(file);});
        await new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=reject;img.src=data;});
        if(currentRevision!==revision)return;value.value=data;name.value=file.name;draw();filename.textContent=file.name+' · 已选择，预览确认发布后生效';
      }catch(_){error.textContent='图片无法读取，请选择有效的小程序码原图。';}finally{submit.disabled=false;picker.value='';}
    });
    form.querySelector('#mini-code-remove').addEventListener('click',()=>{revision++;value.value='';name.value='';picker.value='';error.textContent='';draw();});
  }
  function editForm() {
    const form=document.querySelector('#service-content-form');if(!form)return;
    const newMode=query.has('new');const id=query.get('service')||'repair';let s;
    if(state.draft&&(state.draft.id===id||newMode&&state.draft.isNew))s=copy(state.draft);
    else if(newMode)s={...copy(defaults.services.repair),id:'service-'+Date.now(),name:'',summary:'',detail:'',pc:'',mobile:'',triggers:'',sort:Object.keys(state.services).length+1,terminal:'无地址，仅文字说明',steps:[{title:'了解办事说明',text:''}],isNew:true};
    else s=copy(state.services[id]||defaults.services.repair);
    form.querySelectorAll('[name]').forEach(n=>{if(s[n.name]!==undefined)n.value=['enabled','showInHall'].includes(n.name)?(s[n.name]?'是':'否'):String(s[n.name]);});drawSteps(s.steps);
    const typeField=form.querySelector('[name=entryType]'),shareField=form.querySelector('[name=miniProgramShare]');
    const toggleType=()=>{const mini=typeField.value==='miniprogram';form.querySelector('[data-web-service-fields]').hidden=mini;form.querySelector('[data-web-service-fields]').querySelectorAll('input').forEach(n=>n.disabled=mini);form.querySelector('[data-miniprogram-fields]').hidden=!mini;form.querySelector('[data-miniprogram-fields]').querySelectorAll('input,textarea').forEach(n=>n.disabled=!mini);shareField.required=false;const terminal=form.querySelector('[name=terminal]');terminal.closest('.field').hidden=mini;terminal.disabled=mini;};typeField.addEventListener('change',toggleType);toggleType();
    setupMiniCodeUpload(form);
    document.querySelector('#add-service-step').addEventListener('click',()=>{const data=collectSteps();if(data.length>=12){if(typeof toast==='function')toast('每项服务最多设置12个办理步骤');return;}data.push({title:'',text:''});drawSteps(data);});
    form.addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(form));const data={...s,...d,enabled:d.enabled==='是',showInHall:d.showInHall==='是',sort:Number(d.sort),steps:collectSteps()};let error='';
      if(!data.name.trim()||!data.summary.trim()||!data.detail.trim())error='请完整填写服务名称、卡片简介和详细说明。';
      else if(!icons.includes(data.icon))error='请选择支持的服务图标。';
      else if(!Number.isInteger(data.sort)||data.sort<0||data.sort>999)error='排序请输入0至999的整数。';
      else if(!data.steps.length||data.steps.some(x=>!x.title||!x.text))error='请完整填写每个办理步骤的标题和说明。';
      else if(data.entryType==='miniprogram'&&data.miniProgramShare&&!/^#小程序:\/\/[^\r\n]+\/[^\s/]+$/.test((data.miniProgramShare||'').trim()))error='请填写完整的微信小程序分享口令，以“#小程序://”开头。';
      else if(data.entryType==='miniprogram'&&data.miniProgramUrl&&!miniProgramURL(data.miniProgramUrl))error='请填写有效的HTTPS小程序链接或微信URL Scheme，分享口令请填在备用口令中。';
      else if(data.entryType==='miniprogram'&&data.miniProgramCode&&!codeImageURL(data.miniProgramCode))error='小程序码图片不可用，请重新上传。';
      else if(data.entryType!=='miniprogram'&&data.terminal==='电脑与手机分别配置'&&(!validURL(data.pc)||!validURL(data.mobile)))error='两端均可办理时，请分别填写有效的电脑和手机地址。';
      else if(data.entryType!=='miniprogram'&&data.terminal==='仅电脑'&&!validURL(data.pc))error='请填写有效的电脑正式地址。';
      else if(data.entryType!=='miniprogram'&&data.terminal==='仅手机'&&!validURL(data.mobile))error='请填写有效的手机正式地址。';
      document.querySelector('#service-form-error').textContent=error;if(error)return;
      if(data.entryType==='miniprogram'){data.miniProgramShare=(data.miniProgramShare||'').trim();data.miniProgramUrl=(data.miniProgramUrl||'').trim();data.terminal='仅手机';}state.draft=data;save();location.href='service-preview.html?service='+encodeURIComponent(data.id);
    });
  }
  function previews() {
    const pc=document.querySelector('#service-content-preview-pc'),mobile=document.querySelector('#service-content-preview-mobile');
    if(pc&&mobile){const id=query.get('service')||'repair';const s=(state.draft?.id===id?state.draft:null)||current()||defaults.services.repair;
      const previewFor=port=>{const root=el('div');root.append(el('h3','服务大厅卡片'));const tile=el('div',null,'service-card'),si=el('div',null,'service-icon');si.append(icon(s.icon));tile.append(si,el('h3',s.name),el('p',s.summary),badge(s.tag));root.append(tile,el('p',`${s.enabled?'已启用':'已停用'} · ${s.showInHall?'在大厅展示':'不在大厅展示'} · ${s.who} · 排序 ${s.sort}`,'service-publish-summary'),guide(s,port,{preview:true}));if(s.entryType==='miniprogram')root.append(el('h3','小程序打开页'),miniProgramPanel(s,{preview:true,port}));return root;};
      pc.replaceChildren(previewFor('pc'));const phone=el('div',null,'service-preview-phone');phone.append(previewFor('mobile'));mobile.replaceChildren(phone);document.querySelector('#service-back-edit').href='service-edit.html?service='+encodeURIComponent(s.id);
      document.querySelector('#service-content-confirm').addEventListener('submit',e=>{e.preventDefault();state.services[s.id]=copy(s);delete state.services[s.id].isNew;delete state.draft;save();location.href='service-saved.html?service='+encodeURIComponent(s.id);});
    }
    const name=document.querySelector('#service-saved-name');if(name){const s=current();name.textContent=s?.name||'服务内容';if(s){const role=s.who==='教职工'?'staff':'student';document.querySelector('#service-view-pc').href='../../'+role+'/pc/'+guideURL(s);document.querySelector('#service-view-mobile').href='../../'+role+'/mobile/'+guideURL(s);}}
  }
  function displayForm() {
    const form=document.querySelector('#service-display-form');
    if(form){const data=state.draftDisplay||state.display;form.querySelectorAll('[name]').forEach(n=>n.value=data[n.name]||'');form.addEventListener('submit',e=>{e.preventDefault();state.draftDisplay=Object.fromEntries(new FormData(form));save();location.href='service-display-preview.html';});}
    const host=document.querySelector('#service-display-preview');
    if(host){const d=state.draftDisplay||state.display;host.replaceChildren(heading(d.hallTitle,d.hallSubtitle));const input=el('input');input.placeholder=d.searchPlaceholder;input.disabled=true;host.append(input,el('hr',null,'divider'),heading(d.guideTitle,d.guideSubtitle));document.querySelector('#service-display-confirm').addEventListener('submit',e=>{e.preventDefault();state.display={...d};delete state.draftDisplay;save();location.href='service-display-saved.html';});}
  }
  function front() { renderCatalog();renderRoutes();updateShortcuts(); }
  load();
  document.addEventListener('DOMContentLoaded',()=>{front();renderAdminList();editForm();previews();displayForm();document.querySelector('#admin-service-search')?.addEventListener('input',renderAdminList);});
  window.addEventListener('storage',e=>{if(e.key===storageKey){load();front();renderAdminList();}});
  window.addEventListener('csu-prototype-reset',()=>{state=copy(defaults);front();renderAdminList();});
  window.addEventListener('pageshow',()=>{load();front();renderAdminList();});
})();

"""按各内页设计组织展示结构，复用原有地址、数据和交互脚本。"""

def deep_text(source):
    return html.unescape(re.sub(r'<[^>]+>','',source)).strip()


def deep_avatar(staff=False):
    g='deep-profile'
    face=figma_image(g,'img389833121','','deep-avatar-person')
    circle=figma_image(g,'img4','','deep-avatar-background')
    ribbon=figma_image(g,'imgGroup1142813274','','deep-ribbon-left')+figma_image(g,'imgGroup1142813273','','deep-ribbon-right')
    return '<div class="deep-avatar" aria-hidden="true"><div class="deep-avatar-circle">'+circle+face+'</div><div class="deep-avatar-ribbon">'+ribbon+'<span>'+('教职工' if staff else '学生')+'</span></div></div>'


def deep_skyline():
    parts=[]
    for i in range(1,7):
        g='deep-skyline-'+str(i)
        keys=FIGMA_SKYLINE_LAYERS.get(g,[])
        parts.append('<span class="deep-building deep-building-'+str(i)+'">'+''.join(figma_image(g,k,'') for k in keys)+'</span>')
    return '<div class="deep-skyline" aria-hidden="true">'+''.join(parts)+'</div>'


def deep_campus_hero(kind):
    group={'meetings':'deep-meeting-identity','profile':'deep-staff-profile-title','hall':'deep-hall-title'}[kind]
    marker={'meetings':'img','profile':'imgFrame2147227789','hall':'imgFrame'}[kind]
    desc='中南大学 · 智慧后勤' if kind=='profile' else '找到办事入口，让校园生活少一点等待'
    return '<div class="deep-campus-hero deep-campus-'+kind+'"><div class="deep-campus-title">'+figma_image(group,marker,'','deep-campus-mark')+figma_image(group,'imgGroup',{'meetings':'我的会议','profile':'我的后勤服务','hall':'服务大厅'}[kind],'deep-campus-word')+'</div><p>'+desc+'</p><div class="deep-campus-watermark" aria-hidden="true">I '+figma_image('deep-profile','imgVector','')+' CSU</div>'+deep_skyline()+'</div>'


def deep_student_profile(content):
    first=figma_find(content,'card')
    first_html=content[first['start']:first['end']] if first else ''
    title=re.search(r'<h2>(.*?)</h2>',first_html,re.S)
    name=deep_text(re.sub(r'<span class="avatar">.*?</span>','',title[1] if title else '陈同学'))
    info=figma_find(first_html,'summary-list')
    info_html=first_html[info['start']:info['end']] if info else ''
    identity='<details class="deep-profile-identity"><summary aria-label="查看校园身份信息">'+deep_avatar()+'<div class="deep-profile-name"><h1>'+esc(name)+'</h1><p>'+figma_image('deep-profile','imgElements1','')+'中南大学统一身份认证</p><span>2026******12</span></div></summary><div class="deep-profile-expanded">'+info_html+'</div></details>'
    cards='<div class="deep-profile-shortcuts">'+link('notifications.html','<span class="deep-profile-symbol">'+figma_image('deep-profile','img3','')+'</span><span><b>我的消息</b><small>你有<span data-unread-total>2</span>条消息</small></span>','deep-profile-shortcut')+link('home.html','<span class="deep-profile-symbol">'+figma_image('deep-profile','imgImage7','')+'</span><span><b>问AI</b><small>你的智慧AI</small></span>','deep-profile-shortcut')+'</div>'
    rows=[]
    for target,label,key in [('contacts.html','联系后勤','imgGroup'),('services.html','寻找服务','img2Px'),('privacy.html','隐私说明','imgGroup1')]:
        rows.append(link(target,'<span class="deep-function-icon">'+figma_image('deep-profile',key,'')+'</span><span>'+label+'</span>'+figma_image('deep-profile','imgFrame','','deep-function-arrow'),'deep-function-row'))
    return '<div class="deep-student-profile">'+identity+cards+'<section class="deep-profile-functions"><h2 class="deep-underlined">常用功能</h2>'+''.join(rows)+link('../../visitor/mobile/home.html','退出登录','deep-profile-logout')+'</section></div>'


def deep_staff_profile(content):
    summary=figma_find(content,'summary-list')
    data=content[summary['start']:summary['end']] if summary else ''
    privacy=re.search(r'<a[^>]+href="privacy.html".*?</a>',content,re.S)
    logout=re.search(r'<a[^>]+href="../../visitor/mobile/home.html".*?</a>',content,re.S)
    p=privacy[0] if privacy else link('privacy.html','隐私与数据使用说明','list-row')
    q=logout[0] if logout else link('../../visitor/mobile/home.html','退出并返回游客服务','list-row')
    p=p.replace('class="list-row"','class="deep-staff-account-row"').replace('>隐私与数据使用说明','>'+figma_image('deep-staff-profile-body','imgElements','')+'隐私与数据使用说明')
    q=q.replace('class="list-row"','class="deep-staff-account-row"').replace('>退出并返回游客服务','>'+figma_image('deep-staff-profile-body','imgElements1','')+'退出并返回游客服务')
    return deep_campus_hero('profile')+'<div class="deep-staff-profile"><section><h2>'+figma_image('deep-staff-profile-body','img','')+'基本信息</h2><div class="deep-staff-identity">'+deep_avatar(True)+data+'</div></section><section><h2>'+figma_image('deep-staff-profile-body','img2','')+'账户与隐私</h2>'+p+q+'</section></div>'


def deep_contacts(content):
    rows=[]
    nodes=[n for n in _FigmaSpans(content).nodes if 'list-row' in n['attrs'].get('class','').split()]
    for n in sorted(nodes,key=lambda n:n['start']):
        old=content[n['inner']:content.rfind('</',n['inner'],n['end'])]
        old=old.replace('class="textlink"','class="deep-contact-phone"')
        rows.append('<div class="deep-contact-row"><span class="deep-contact-icon">'+figma_image('deep-contacts','img2','')+'</span>'+old+'</div>')
    hero='<section class="deep-contact-hero"><div class="deep-contact-title">后勤服务热线 <span>24h</span></div><strong>0731-88836000</strong><p>24小时值班，受理报修、咨询、投诉与建议。</p>'+link('tel:073188836000',figma_image('deep-contacts','imgPhone','')+'拨打电话','deep-hotline-button')+figma_image('deep-contacts','imgImage6','','deep-contact-robot')+'</section>'
    return '<div class="deep-contacts">'+hero+'<section class="deep-contact-centers"><h2 class="deep-underlined">各服务中心</h2>'+''.join(rows)+'</section></div>'


def figma_deep_content(path,content,role,port):
    name=Path(path).stem
    if role=='admin':return deep_kb_content(content,name)
    if name.startswith('chat'):content=content.replace('<div class="chat-layout"><div>','<div class="chat-layout"><div class="chat-main">',1)
    if port!='mobile':return content
    if name=='profile' and role=='student':return deep_student_profile(content)
    if name=='profile' and role=='staff':return deep_staff_profile(content)
    if name=='contacts':return deep_contacts(content)
    if name=='services' and role=='staff':content='<template id="deep-hall-hero">'+deep_campus_hero('hall')+'</template>'+content
    if name=='meetings' and role=='staff':
        head=figma_find(content,'page-heading')
        if head:content=figma_replace(content,head,deep_campus_hero('meetings')+link('notifications.html',icon('fa-bell')+'<span data-unread-count>3</span>','deep-meeting-bell'))
        notice=figma_find(content,'note')
        if notice:
            original=content[notice['start']:notice['end']]
            content=figma_replace(content,notice,'<details class="deep-meeting-help"><summary>会议提醒说明</summary>'+original+'</details>')
        content='<div class="deep-meetings">'+content+'</div>'
    if name in ['notifications','notifications-unread']:
        button=re.search(r'<button\b[^>]*data-mark-all-read[^>]*>.*?</button>',content,re.S)
        if button:
            content=content[:button.start()]+content[button.end():]+'<div class="deep-notification-read">'+button[0]+'</div>'
        content=re.sub(r'(<div class="notification-meta">)([^<]+)',r'\1<span>\2</span>',content)
        content=content.replace('全部消息</a>','全部消息(2)</a>').replace('全部通知</a>','全部通知(3)</a>')
        content=re.sub(r'未读 <span data-unread-total>(\d+)</span>',r'未读(<span data-unread-total>\1</span>)',content)
    return content


def figma_deep_skin(body,path,role,port):
    if role=='admin':return deep_kb_skin(body,Path(path).stem)
    if port!='mobile':return body
    name=Path(path).stem
    labels={'contacts':'联系后勤','profile':'我的' if role=='student' else '智慧后勤AI助手','notifications':'我的消息','notifications-unread':'我的消息','notifications-empty':'我的消息','privacy':'隐私说明'}
    labels.update({s['id']:s['name'] for s in SERVICES})
    labels.update({'notification-detail':'消息详情','notification-service':'消息详情','notification-change':'会议变更通知','notification-cancelled':'会议取消通知','meeting-detail':'会议详情','meeting-changed':'会议最新安排','meeting-cancelled':'已取消会议','meeting-reminded':'会议详情','feedback':'回答反馈','feedback-success':'反馈成功','history':'对话记录','voice':'语音咨询','voice-recording':'语音咨询','voice-review':'语音咨询','voice-error':'语音咨询','knowledge-source':'知识来源','knowledge-source-repair':'知识来源','knowledge-source-shuttle':'知识来源'})
    if name.startswith('handoff-') or name=='service-handoff':labels[name]='前往官方服务'
    if name in labels:body=body.replace('<strong>智慧后勤AI助手</strong>','<strong>'+esc(labels[name])+'</strong>',1)
    body=re.sub(r'(href="profile.html"[^>]*>.*?</i>)个人中心',r'\1我的',body)
    primary=name in ['home','assistant','services','contacts','profile','meetings']
    if not primary:body=body.replace('<div class="mobile">','<div class="mobile deep-secondary">',1)
    if not primary:
        target=name.removeprefix('handoff-')+'.html' if name.startswith('handoff-') else 'chat.html' if name in ['feedback','knowledge-source','knowledge-source-repair','knowledge-source-shuttle'] else 'services.html' if name in [s['id'] for s in SERVICES] or name.startswith(('service-','mini-program')) else 'notifications.html' if name.startswith('notification-') else 'meetings.html' if name.startswith('meeting-') else ('home.html' if role=='visitor' else 'profile.html') if name=='privacy' else 'assistant.html' if role=='staff' else 'home.html'
        body=re.sub(r'<a class="mobile-back".*?</a>',link(target,'返回','mobile-back','fa-arrow-left'),body,count=1,flags=re.S)
    campus=role=='staff' and name in ['profile','meetings','services']
    if campus:body=body.replace('<div class="mobile">','<div class="mobile"><div class="deep-campus-surface" aria-hidden="true"></div>',1)
    elif name in ['profile','contacts','home','assistant'] or name.startswith('chat'):
        watermark='<div class="deep-mobile-watermark" aria-hidden="true">I '+figma_image('deep-profile','imgVector','')+' CSU</div>'
        body=body.replace('</header>','</header>'+watermark,1)
    return (body[:-6]+'<div class="deep-home-indicator" aria-hidden="true"></div></div>').replace('loading="lazy"','decoding="async"')


FIGMA_SKYLINE_LAYERS=json.loads((ROOT/'tools/figma_skyline.json').read_text())
exec((ROOT/'tools/figma_kb.py').read_text())

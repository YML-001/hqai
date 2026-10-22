# -*- coding: utf-8 -*-
"""采用用户Figma设计稿的展示层，保留原型既有交互挂载点。"""
from html.parser import HTMLParser as _FigmaParser

FIGMA_ASSETS=json.loads((ROOT/'tools/figma_assets.json').read_text())
FIGMA_CSS=(ROOT/'tools/figma_theme.css').read_text()


def figma_asset(group,name,prefix='../../'):
    return prefix+FIGMA_ASSETS[group][name]


def figma_image(group,name,alt='',cls='',prefix='../../'):
    return '<img src="'+figma_asset(group,name,prefix)+'" alt="'+esc(alt)+'" class="'+cls+'" loading="lazy">'


def figma_robot_markup(compact=False):
    if compact:
        group='mobile-home-robot';name=next(iter(FIGMA_ASSETS[group]))
    else:group='pc-assistant';name='imgImage1413642'
    return figma_image(group,name,'后勤数字服务助手小助','figma-robot')


class _FigmaSpans(_FigmaParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=False)
        self.source=source;self.stack=[];self.nodes=[];self.offsets=[0]
        for line in source.splitlines(True):self.offsets.append(self.offsets[-1]+len(line))
        self.feed(source)
    def position(self):
        line,column=self.getpos();return self.offsets[line-1]+column
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);start=self.position();end=start+len(self.get_starttag_text())
        if tag not in ['img','input','meta','link','br','hr','source','area','base','col','embed','param','track','wbr']:
            self.stack.append({'tag':tag,'attrs':attrs,'start':start,'inner':end})
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:
                n=self.stack[i];n['end']=self.source.find('>',self.position())+1
                self.nodes.append(n);self.stack=self.stack[:i];break


def figma_find(source,cls,contains=None):
    nodes=_FigmaSpans(source).nodes
    return next((n for n in sorted(nodes,key=lambda n:n['start']) if cls in n['attrs'].get('class','').split() and (contains is None or contains in source[n['start']:n['end']])),None)


def figma_replace(source,node,value):
    return source[:node['start']]+value+source[node['end']:] if node else source


def figma_theme_content(path,content,role,port):
    if 'data-figma-body' in content:return content
    def service_href(sid):
        return 'login-required.html?intent=service&service='+sid if role=='visitor' else sid+'.html'
    if '<div class="welcome' in content and '<div class="quick-grid">' in content:
        welcome=figma_find(content,'welcome');quick=figma_find(content,'quick-grid')
        if welcome and quick:
            intro=content[welcome['start']:welcome['end']]
            grid=content[quick['start']:quick['end']]
            for svc in SERVICES:
                grid=grid.replace('href="'+svc['id']+'.html"','data-caption="'+esc(svc['summary'])+'" href="'+svc['id']+'.html"')
            if port=='mobile':
                order=['repair','shuttle','utility-pay','supervision','food-delivery']
                grid='<div class="quick-grid">'+''.join(link(service_href(sid),icon(next(s for s in SERVICES if s['id']==sid)['icon'])+next(s for s in SERVICES if s['id']==sid)['name'],'quick') for sid in order)+'</div>'
                title=link('services.html','后勤服务 '+icon('fa-angle-right'),'figma-section-link')
                content=content[:welcome['start']]+intro+'<section class="figma-mobile-services">'+title+grid+'</section>'+content[quick['end']:]
            else:
                content=content[:welcome['start']]+'<section class="figma-home-intro">'+intro+grid+'</section>'+content[quick['end']:]
                common=figma_find(content,'contact-box','mini-apps')
                common_html=content[common['start']:common['end']] if common else ''
                if common:
                    content=figma_replace(content,common,'')
                    common_html=common_html.replace('<h2>常用服务</h2>','<h2>热门服务'+link('services.html','全部服务 '+icon('fa-circle-chevron-right'),'figma-all-services')+'</h2>')
                    apps=figma_find(common_html,'mini-apps')
                    featured=[next(s for s in SERVICES if s['id']==sid) for sid in ['newspaper','pool','lost','announcement']]
                    common_html=figma_replace(common_html,apps,'<div class="mini-apps">'+''.join(link(service_href(s['id']),icon(s['icon'])+s['name'],'') for s in featured)+'</div>')
                    for svc in SERVICES:
                        common_html=common_html.replace('href="'+svc['id']+'.html"','data-caption="'+esc(svc['summary'])+'" href="'+svc['id']+'.html"')
                    question=figma_find(content,'card','question-list')
                    if question:content=figma_replace(content,question,'<div class="figma-question-panels">'+content[question['start']:question['end']]+common_html+'</div>')
        if port=='mobile' and role=='staff':
            intro=figma_find(content,'welcome');services=figma_find(content,'figma-mobile-services');questions=figma_find(content,'card','question-list')
            if services and questions and services['end']<=questions['start']:
                service_html=content[services['start']:services['end']]
                content=content[:services['start']]+content[services['end']:questions['end']]+service_html+content[questions['end']:]
        if port=='mobile':
            content=content.replace('同学你好，今天有什么可以帮你？','同学～有什么可以帮你？')
            content=content.replace('报修、水电缴纳、班车和生活服务，<br>从一个问题开始，找到你的办事入口。','你的智慧后勤AI助手')
    if port=='mobile' and role=='staff':
        student_group='mobile-home-robot';student_name=next(iter(FIGMA_ASSETS[student_group]))
        content=content.replace(figma_asset(student_group,student_name),figma_asset('staff-mobile-banner','imgImage5'))
    if role=='admin' and Path(path).stem=='dashboard':
        pending=figma_find(content,'card','待办事项')
        pending_html=content[pending['start']:pending['end']] if pending else ''
        if pending:
            content=figma_replace(content,pending,'')
            pending_html=re.sub(r'class="card\s*"','class="figma-admin-pending"',pending_html).replace('待办事项','我的待办')
        trend=figma_find(content,'grid2','bars')
        if trend:
            content=figma_replace(content,trend,content[trend['start']:trend['end']].replace('class="grid2"','class="figma-admin-trend"',1))
        heading_node=figma_find(content,'page-heading')
        if heading_node:
            banner='<div class="figma-admin-welcome"><div class="figma-campus-banner"><h2>中南大学智慧后勤</h2><p>让每一次服务都有回应</p></div>'+pending_html+'</div>'
            content=figma_replace(content,heading_node,content[heading_node['start']:heading_node['end']]+banner)
    content=figma_deep_content(path,content,role,port)
    return '<div data-figma-body data-screen="'+Path(path).stem+'">'+content+'</div>'


def figma_brand(role,port,prefix):
    if port=='mobile' and role!='guide':return '<div class="brand figma-mobile-brand"><strong>智慧后勤AI助手</strong></div>'
    group='admin-knowledge' if role=='admin' else 'pc-header'
    if role=='admin':
        logo=figma_image(group,'imgGroup1','中南大学','figma-admin-seal',prefix)+figma_image(group,'imgGroup2','中南大学','figma-admin-wordmark',prefix)
    else:
        logo=figma_image(group,'imgVector','中南大学校徽','figma-seal',prefix)+figma_image(group,'imgUnion','中南大学','figma-wordmark',prefix)
    return '<div class="brand figma-brand"><div class="figma-school-logo">'+logo+'</div><div class="figma-unit"><strong>后勤保障部</strong><span>智能助手</span></div></div>'


def figma_skin(body,path,role,port):
    prefix='../'*(len(Path(path).parts)-1)
    body=body.replace(BRAND,figma_brand(role,port,prefix))
    if port=='mobile' and role!='guide':
        status='<div class="figma-mobile-status" aria-hidden="true"><span>9:41</span><div>'+''.join(figma_image('mobile-header',key,'','',prefix) for key in ['imgNetworkSignalLight','imgWiFiSignalLight','imgBatteryLight'])+'</div></div>'
        body=body.replace('<header class="topbar">',status+'<header class="topbar">',1)
    if role!='admin' and port=='pc' and role!='guide':
        sticker=figma_image('pc-sidebar','img11','','figma-sidebar-robot',prefix)
        body=body.replace('</aside><main class="main">',sticker+'</aside><main class="main">',1)
    if role=='admin':
        body=body.replace('<aside class="sidebar">','<aside class="sidebar"><label class="figma-menu-search">'+icon('fa-magnifying-glass')+'<input aria-label="查找管理菜单" placeholder="输入功能关键词" data-figma-menu-search></label>',1)
    return figma_deep_skin(body,path,role,port)


def figma_theme_assets(path):
    prefix='../'*(len(Path(path).parts)-1)
    css=FIGMA_CSS+'\n'+(ROOT/'tools/figma_deep.css').read_text()+'\n'+(ROOT/'tools/figma_kb.css').read_text()
    css=re.sub(r'\{\{([\w-]+)\.([\w]+)\}\}',lambda m:figma_asset(m[1],m[2],prefix),css)
    script=(ROOT/'tools/figma_theme.js').read_text()
    script+='\n'+(ROOT/'tools/figma_deep.js').read_text()
    return '<style data-figma-theme>'+css+'</style><script data-figma-interactions>'+script+'</script>'


exec(compile((ROOT/'tools/figma_deep.py').read_text(),'figma_deep.py','exec'),globals())

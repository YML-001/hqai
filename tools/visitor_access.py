# 游客可先咨询、查看功能，使用具体服务或获取本人信息时再登录。
def build_visitor_access_pages():
    script='<script>'+(ROOT/'tools/visitor_access.js').read_text()+'</script>'
    def emit(role,port,name,title,body,active='home'):
        path=f'{role}/{port}/{name}.html'
        PAGES[:]=[p for p in PAGES if p['path']!=path]
        output(path,title,body,role=role,port=port,active=active)

    def public_links(body):
        for number,sid,answer in [(4,'pool','chat-pool'),(5,'supervision','chat-supervision')]:
            body=body.replace(f'href="{sid}.html"><span class="number">{number}</span>',f'href="{answer}.html"><span class="number">{number}</span>')
        for sid in SERVICE_CONTENT_DEFAULTS['services']:
            body=body.replace(f'href="{sid}.html"',f'href="login-required.html?intent=service&amp;service={sid}"')
        return body.replace('href="feedback.html"','href="login-required.html?intent=feedback"')

    for port in ['pc','mobile']:
        home=CONTENTS[f'student/{port}/home.html'].replace('同学你好，今天有什么可以帮你？','你好，今天有什么可以帮你？')
        home=note('游客可直接提问、查看公开知识和功能列表。使用具体服务或查询本人信息时，再登录校园身份。')+public_links(home)
        emit('visitor',port,'home','游客智能问答',home)
        for item in list(PAGES):
            name=Path(item['path']).stem
            if item['role']=='student' and item['port']==port and (name.startswith('chat') or name.startswith('knowledge-source') or name in ['contacts','privacy']):
                emit('visitor',port,name,item['title'],public_links(CONTENTS[item['path']]),'services' if name=='contacts' else 'home')
        for name,title,text,sid,source in [
            ('chat-pool','游泳馆怎么预约？','潇湘校区游泳馆周一闭馆检修，其他开放场次与预约规则以预约系统公示为准。可在场馆预约平台查看可预约场次，按要求携带证件到场。咨询电话0731-88877959。','pool','后勤服务知识库 · 场馆服务'),
            ('chat-supervision','后勤服务问题可以向谁反馈？','后勤服务热线0731-88836000受理咨询、报修、建议与投诉。需要在线提交服务监督事项时，可登录校园身份后前往原平台办理。','supervision','后勤服务知识库 · 服务监督'),
        ]:
            body='<div class="chat-layout"><div><div class="bubble-user" data-question>'+title+'</div>'+card('后勤小助手','<div data-answer><h2>'+title+'</h2><p>'+text+'</p></div><p class="source">来源：《'+source+'》；资料截止2026年9月17日，场次以最新公示为准。</p>'+link('login-required.html?intent=service&amp;service='+sid,'登录后使用服务','btn primary'))+composer()+'</div>'+rail()+'</div>'
            emit('visitor',port,name,'公开问答 · '+title,public_links(body))
        d=SERVICE_CONTENT_DEFAULTS['display']
        entries=''.join(link('login-required.html?intent=service&amp;service='+s['id'],'<div class="service-icon">'+icon(s['icon'])+'</div><h3>'+esc(s['name'])+'</h3><p>'+esc(s['summary'])+'</p>'+badge('登录后使用'),'service-card') for s in SERVICE_CONTENT_DEFAULTS['services'].values() if s['showInHall'])
        catalog='<div data-service-catalog>'+heading(d['hallTitle'],d['hallSubtitle'])+'<div class="filters"><input id="service-catalog-search" aria-label="搜索服务" placeholder="'+esc(d['searchPlaceholder'])+'"></div><div class="grid3" id="service-catalog-grid">'+entries+'</div></div>'
        emit('visitor',port,'services','游客服务大厅',note('可以先查看所有已启用的服务功能；点击具体服务后，登录校园身份继续使用。')+catalog,'services')

        gate=heading('登录后，继续刚才的操作','公开咨询无需登录，涉及身份的服务由你确认后继续',link('home.html','继续以游客身份咨询','btn sm','fa-arrow-left'))
        gate+=card('','<div style="max-width:650px;margin:auto;padding:18px 0"><div class="service-icon">'+icon('fa-user-lock')+'</div><h1 id="access-title">这项服务需要校园身份</h1><p id="access-reason">登录后可核对服务适用对象，并继续刚才的操作。</p><div id="access-pending" class="note" hidden></div><div class="actions"><a class="btn primary" id="access-login" href="login.html">登录并继续</a><a class="btn" id="access-cancel" href="home.html">暂不登录</a></div></div>')+note('原型不采集校园密码；演示登录仅用于展示身份切换与继续办理，不连接真实个人数据。')+script
        emit('visitor',port,'login-required','登录提示',gate)
        form='<form data-context-login><div class="field"><label for="login-role">选择演示身份</label><select id="login-role" name="loginRole"><option value="student">学生</option><option value="staff">教职工</option></select></div><div id="login-pending" class="note" hidden></div><label class="checkline"><input type="checkbox" required><span>我已阅读'+link('privacy.html','隐私与数据使用说明','textlink')+'，了解必要身份信息的使用范围。</span></label><button class="btn primary" type="submit">'+icon('fa-shield-halved')+' 统一身份认证 · 演示登录</button></form>'
        login=card('','<div class="login-card" style="margin:0 auto;padding:15px;max-width:480px">'+BRAND+'<h1>用校园身份，继续服务</h1><p>你的问题或所选功能会保留，登录后回到原来的操作。</p>'+note('演示不输入校园密码，不连接真实认证。')+form+'<a class="btn" id="login-cancel" href="home.html">暂不登录，返回浏览</a></div>')+script
        emit('visitor',port,'login','统一身份认证',login)

    for role in ['student','staff']:
        for port in ['pc','mobile']:
            body=heading('本人信息查询','先确认身份，再由授权业务系统提供个人信息')+'<div class="bubble-user" data-question>查询我的业务信息</div>'+card('已保留你的查询问题','<p>当前已登录为'+('学生' if role=='student' else '教职工')+'身份。原型未接通个人数据接口，不能展示真实余额、欠费、房间或报修记录。</p><p>你可以前往对应服务，在原平台核对身份后查看本人业务信息。</p><div class="actions"><a class="btn primary" data-personal-action href="services.html">查看对应服务</a>'+link('assistant.html' if role=='staff' else 'home.html','继续咨询')+'</div>')+note('身份认证不等于已取得所有个人业务数据权限。正式系统还需执行服务端授权，并遵循原业务系统的查询范围。')+composer()+script
            emit(role,port,'chat-personal','本人信息查询',body)

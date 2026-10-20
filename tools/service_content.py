# 服务内容采用统一配置模型，后台确认发布后用于各角色与终端的展示。
def make_service_defaults():
    items={}
    for i,s in enumerate(SERVICES):
        sid=s['id']
        if sid=='repair':
            how=[('准备报修信息','确认校区、楼栋、房间，描述故障现象，可在原平台上传现场图片。'),('进入网上报修平台','在原平台创建报修单，并核对联系人及联系方式。'),('查看受理和维修进度','返回原平台查看处理记录；紧急故障请拨打后勤服务热线。')]
        elif sid=='utility-pay':
            how=[('打开官方服务入口','进入“中南大学后勤保障部”微信公众号，选择服务中心、服务平台、水电缴费。'),('完成身份认证并绑定房间','按原平台指引注册、认证，核对校区、楼栋及房间信息。'),('在水电平台完成充值','选择账户与充值金额并付款；交易状态、余额和记录均以原平台为准。')]
        elif sid=='pool':
            how=[('查看开放场次','周一闭馆检修，其他日期及场次以现场公示和预约系统为准。'),('在原平台选择场次','可预约范围与剩余名额以预约系统实际显示为准。'),('按预约要求到场','携带有效证件，依预约说明缴费进场。咨询电话0731-88877959。')]
        else:
            how=[('了解办事说明',s['summary']),('前往官方渠道','使用已提供的服务入口，相关规则以原平台为准。'),('需要帮助时联系后勤','后勤服务热线0731-88836000，提供咨询与转接。')]
        terminal='电脑与手机分别配置' if s['pc'] and s['mobile'] else '仅电脑' if s['pc'] else '仅手机' if s['mobile'] else '无地址，仅文字说明'
        category='报修' if sid=='repair' else '水电缴纳' if sid.startswith('utility') else '班车' if sid=='shuttle' else '其他办事'
        items[sid]={
            'id':sid,'name':s['name'],'icon':s['icon'],'summary':s['summary'],'detail':s['detail'],
            'category':category,'who':'全部用户（说明）' if s['who']=='所有人' else s['who'],
            'channel':'原业务系统','terminal':terminal,'pc':s['pc'],'mobile':s['mobile'],
            'triggers':s['triggers'],'tag':'手机办理' if sid=='utility-pay' else '服务指引',
            'sort':i+1,'enabled':True,'showInHall':sid!='utility-info',
            'buttonText':'前往办理','qrButtonText':'手机扫码办理','fallbackText':'当前终端暂未提供在线办理地址，请参考办理说明或联系后勤服务热线0731-88836000。',
            'notice':'服务由原业务系统提供，助手不受理报修单、不处理支付、不保存交易记录。',
            'steps':[{'title':t,'text':d} for t,d in how]
        }
    return {'version':1,'updated':0,'display':{
        'hallTitle':'服务大厅','hallSubtitle':'找到办事入口，让校园生活少一点等待',
        'searchPlaceholder':'搜索服务，如报修、水电、班车','guideTitle':'服务指引','guideSubtitle':'办事之前，先把流程看清楚'
    },'services':items}

SERVICE_CONTENT_DEFAULTS=make_service_defaults()
SERVICE_CONTENT_STYLE='''<style>
[hidden]{display:none!important}.service-config-guide h1,.service-config-guide h3,.service-card h3,.service-card p{overflow-wrap:anywhere}.service-config-guide .detail-banner .service-icon{flex-shrink:0}.service-preview-panel .split-detail{display:block}.service-preview-panel .service-card{margin-bottom:14px}
.service-config-result h1{overflow-wrap:anywhere}.service-content-step{display:grid;grid-template-columns:30px minmax(0,1fr);gap:14px;margin-bottom:0}.service-content-step>span{width:28px;height:28px;border-radius:50%;background:#edf4ff;color:var(--blue);display:grid;place-items:center}.service-content-step p{font-size:13px;margin:5px 0 0;white-space:pre-wrap}.service-content-body{white-space:pre-wrap;color:#66758a}.service-draft-chip{font-size:11px;color:#998355;background:#fff8ea;border-radius:6px;padding:4px 8px}.service-content-notice{white-space:pre-wrap}.service-qr{max-width:210px;margin:15px auto}.service-qr svg{width:100%;height:auto}.service-admin-empty{text-align:center;color:#8a9db7;padding:24px}.service-preview-phone{max-width:420px;margin:auto;background:#f5f8fd;border:1px solid var(--line);border-radius:19px;padding:18px}.service-preview-phone .split-detail{display:block}.service-preview-phone h1{font-size:23px}.service-preview-phone .card{padding:18px}.service-preview-phone .page-heading{display:block}.service-content-disabled{padding:30px;text-align:center}.service-content-disabled i{font-size:34px;color:#a5b9d6;margin-bottom:20px}.service-content-link{overflow-wrap:anywhere;font-size:12px;color:#6d84a5}.service-step-edit{border:1px solid var(--line);border-radius:11px;padding:17px;margin-bottom:13px;background:#fbfcff}.service-step-edit .field{margin-bottom:12px}.service-step-edit textarea{min-height:75px}.service-step-order{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:12px}.service-step-order strong{font-size:13px;color:#7186a5}.service-step-order .actions{gap:5px}.service-step-order button{font-size:11px;padding:5px 8px}.service-preview-title{display:flex;align-items:center;justify-content:space-between;gap:15px;margin-bottom:15px}.service-preview-title h2{margin:0}.service-publish-summary{margin:0 0 23px;font-size:12px;color:#7b8da7}.service-config-form-error{color:var(--red);font-size:13px;margin:14px 0;white-space:pre-wrap}.service-content-meta{font-size:12px;color:#8697ad}.mobile .service-content-step{gap:11px}.mobile .service-content-body{font-size:13px}.mobile .service-config-guide .detail-banner h1{font-size:23px}.mobile .service-config-guide .split-detail{display:block}.mobile .service-config-guide .page-heading{align-items:flex-start}.service-preview-phone .service-card{padding:18px}.service-preview-phone .grid3{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
</style>'''

def service_content_assets(role,port):
    if role not in ['student','staff','admin','visitor']:return ''
    payload=json.dumps(SERVICE_CONTENT_DEFAULTS,ensure_ascii=False).replace('<','\\u003c')
    context=json.dumps({'role':role,'port':port},ensure_ascii=False)
    return SERVICE_CONTENT_STYLE+'<script>window.CSU_SERVICE_DEFAULTS='+payload+';window.CSU_SERVICE_CONTEXT='+context+';</script><script src="../../assets/vendor/qrcode.js"></script><script>'+(ROOT/'tools/service_content.js').read_text()+'</script>'

def service_default_guide(service,role,port):
    s=service;d=SERVICE_CONTENT_DEFAULTS['display']
    content=heading(d['guideTitle'],d['guideSubtitle'],link('services.html','全部服务','btn sm','fa-arrow-left'))
    content+='<div class="split-detail"><div>'+card('',f'<div class="detail-banner"><div class="service-icon">{icon(s["icon"])}</div><div><h1>{s["name"]}</h1><p>{s["summary"]}</p></div></div><p class="service-content-body">{s["detail"]}</p><hr class="divider"><h2>办理步骤</h2>'+steps([(x['title'],x['text']) for x in s['steps']]))+'</div><div>'+card('办理信息',details([('适用对象',s['who']),('办理渠道',s['channel']),('终端支持',s['terminal'])])+link('service-handoff.html?service='+s['id'],s['buttonText'],'btn primary'))+note(s['notice'])+'</div></div>'
    return '<div class="service-config-guide" data-service-guide="'+s['id']+'">'+content+'</div>'

def build_service_content_pages():
    def replace(path,title,body,role,port,active='services'):
        PAGES[:]=[p for p in PAGES if p['path']!=path]
        output(path,title,body,role=role,port=port,active=active)
    for role in ['student','staff']:
        for port in ['pc','mobile']:
            base=f'{role}/{port}/'
            allowed=[s for s in SERVICE_CONTENT_DEFAULTS['services'].values() if s['showInHall'] and (role=='student' or s['who']!='学生')]
            entries=''.join(link(s['id']+'.html','<div class="service-icon">'+icon(s['icon'])+'</div><h3>'+esc(s['name'])+'</h3><p>'+esc(s['summary'])+'</p>'+badge(esc(s['tag'])),'service-card') for s in allowed)
            d=SERVICE_CONTENT_DEFAULTS['display']
            body='<div data-service-catalog>'+heading(d['hallTitle'],d['hallSubtitle'])+'<div class="filters"><input id="service-catalog-search" aria-label="搜索服务" placeholder="'+esc(d['searchPlaceholder'])+'"></div><div class="grid3" id="service-catalog-grid">'+entries+'</div><div id="service-catalog-empty" class="card empty" hidden>暂无匹配服务，请换一个关键词或联系后勤。</div></div>'
            replace(base+'services.html', '服务大厅',body,role,port)
            for sid,s in SERVICE_CONTENT_DEFAULTS['services'].items():
                replace(base+sid+'.html',s['name'],service_default_guide(s,role,port),role,port)
            replace(base+'service-guide.html','服务办理指引','<div class="service-config-guide" data-service-guide="query">'+note('正在读取服务内容，请稍候。')+'</div>',role,port)
            handoff='<div data-service-handoff>'+heading('前往官方服务','请在原业务系统内完成后续操作')+'</div>'
            replace(base+'service-handoff.html','官方服务跳转',handoff,role,port)
            replace(base+'service-mobile.html','手机扫码办理','<div data-service-qr>'+heading('手机扫码办理','使用手机打开对应的官方服务')+'</div>',role,port)
            replace(base+'service-unavailable.html','服务替代办理方式','<div data-service-unavailable>'+heading('换一种方式，继续办理')+'</div>',role,port)
            for item in list(PAGES):
                if item['role']==role and item['port']==port and Path(item['path']).stem.startswith('handoff-'):
                    sid=Path(item['path']).stem[len('handoff-'):]
                    replace(item['path'],item['title'],'<div data-service-handoff="'+sid+'">'+heading('前往官方服务','请在原业务系统内完成后续操作')+'</div>',role,port)

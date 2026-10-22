"""知识库内页采用各自的设计结构，沿用原有表单与数据挂载。"""


def kb_slice(source, node):
    return source[node['start']:node['end']] if node else ''


def kb_card(title, body, key, cls='', group='deep-kb-edit'):
    return '<section class="card deep-kb-card '+cls+'"><h2>'+figma_image(group,key,'')+title+'</h2>'+body+'</section>'


def kb_field(source, name):
    return kb_slice(source, figma_find(source,'field','name="'+name+'"'))


def kb_metadata(label, value, bind=''):
    return '<div><dt>'+label+'</dt><dd'+(' data-bind="'+bind+'"' if bind else '')+'>'+value+'</dd></div>'


def kb_release_info(preview=False):
    status='待确认上线' if preview else '已上线'
    rows=kb_metadata('可见范围','公开','knowledge.visibility')+kb_metadata('维护责任人','张老师 · 后勤指定管理员','knowledge.owner')+kb_metadata('当前版本','版本3 · '+status)
    return kb_card('发布信息','<dl class="deep-kb-metadata">'+rows+'</dl>','imgFrame8',group='deep-kb-detail')


def kb_references(content):
    linked=re.search(r'<a\b[^>]*data-kb-linked-source[^>]*>.*?</a>',content,re.S)
    rows=kb_metadata('来源文档','中南大学后勤服务知识库（公文版）','knowledge.source')+kb_metadata('来源章节','五、水电与能源服务','knowledge.chapter')+kb_metadata('资料截止日期','2026年9月17日','knowledge.sourceDate')+kb_metadata('关联来源文件',linked[0] if linked else '未关联文件')
    return kb_card('引用依据','<dl class="deep-kb-metadata deep-kb-reference-grid">'+rows+'</dl>'+note('请按正式来源核实内容；资料更新后应及时修订知识。'),'imgFrame6',group='deep-kb-detail')


def deep_kb_edit(content):
    first=figma_find(content,'card','<h2>知识内容</h2>')
    old=kb_slice(content,first)
    fields='<div class="deep-kb-fields deep-kb-basic">'+kb_field(old,'title')+kb_field(old,'category')+'</div>'+kb_field(old,'questions')+kb_field(old,'answer')
    content=figma_replace(content,first,kb_card('知识内容',fields,'imgFrame4','deep-kb-answer-editor'))
    source=figma_find(content,'card','<h2>引用依据</h2>')
    old=kb_slice(content,source)
    attachments=kb_slice(old,figma_find(old,'source-card'))
    source_fields='<div class="deep-kb-fields">'+kb_field(old,'source')+kb_field(old,'chapter')+'</div><div class="deep-kb-fields">'+attachments+kb_field(old,'sourceDate')+'</div>'
    content=figma_replace(content,source,kb_card('引用依据',source_fields,'imgFrame6','deep-kb-source-editor'))
    release=figma_find(content,'card','<h2>发布范围</h2>')
    old=kb_slice(content,release)
    content=figma_replace(content,release,kb_card('发布范围',kb_field(old,'visibility')+kb_field(old,'owner')+note('发布人须核对来源、电话、收费与开放时间；缺少依据时保留为草稿。'),'imgFrame9'))
    rule=figma_find(content,'card','<h2>发布规则</h2>')
    original=kb_slice(content,rule)
    checklist='<ul class="deep-kb-checklist">'+''.join('<li>'+figma_image('deep-kb-edit','imgFrame11','')+t+'</li>' for t in ['来源可靠，文档与章节可追溯','电话、收费和开放时间均为最新','可见范围与实际适用人群一致'])+'</ul>'
    content=figma_replace(content,rule,kb_card('上线前，请核对',checklist,'imgFrame10')+original)
    content=content.replace('class="form-layout"','class="form-layout deep-kb-layout"',1)
    content=content.replace('<div class="form-actions">','<div class="form-actions deep-kb-bottom"><p>* 为必填项；知识在确认上线前不会参与问答。</p>',1)
    return content


def deep_kb_read(content, preview=False):
    extras=''.join(match[0] for match in re.finditer(r'<(style|script)\b[^>]*>.*?</\1>',content,re.S))
    heading=kb_slice(content,figma_find(content,'page-heading'))
    cards=[n for n in sorted(_FigmaSpans(content).nodes,key=lambda n:n['start']) if 'card' in n['attrs'].get('class','').split()]
    first=kb_slice(content,cards[0])
    title=re.search(r'<h2>(.*?)</h2>',first,re.S)[1]
    answer=re.search(r'<p\b[^>]*data-bind="knowledge.answer"[^>]*>.*?</p>',first,re.S)[0]
    status=badge('待确认' if preview else '已上线','amber' if preview else 'green')
    summary='<section class="card deep-kb-card deep-kb-answer"><header><h2>'+title+'</h2>'+status+'</header><p class="deep-kb-code">知识编号：知-0001 · 水电缴纳</p><div class="deep-kb-answer-body"><h3>标准答复</h3>'+answer+'</div><div class="deep-kb-question"><small>常见问法</small><p data-bind="knowledge.questions">宿舍电费怎么交；水费在哪里充值；欠费了怎么办</p></div></section>'
    if preview:
        # 确认表单完整搬到底部，必选复选框和原来的提交地址不变。
        form=re.search(r'<form\b.*?</form>',first,re.S)[0]
        bottom='<div class="deep-kb-bottom deep-kb-confirm">'+form+'</div>'
        history=kb_card('版本记录','<ol class="timeline"><li><b>版本3 · 上线</b><p>2026年10月19日16:20 · 张老师 · 补充原平台账单说明</p></li><li><b>版本2 · 修订</b><p>2026年10月17日10:10 · 张老师 · 更新公众号进入路径</p></li></ol>','imgFrame8',group='deep-kb-preview')
        heading=heading.replace('</div></div>','</div>'+link('knowledge-edit.html','返回修改','btn sm')+'</div>',1)
        banner=note('当前内容尚未上线。核对来源、时效与可见范围后，确认上线即可参与问答。')
    else:
        original=kb_slice(content,cards[1])
        offline=re.search(r'<a\b[^>]*href="knowledge-offline.html".*?</a>',original,re.S)[0]
        history=original.replace(offline,'').replace('<h2>版本记录</h2>','<h2>'+figma_image('deep-kb-detail','imgFrame9','')+'版本记录</h2>').replace('class="card ','class="card deep-kb-card ')
        bottom='<div class="deep-kb-bottom"><p>已上线知识可被问答引用，内容不再适用时请及时下线并说明原因。</p>'+offline+'</div>'
        banner=''
    return heading+banner+'<div class="deep-kb-layout"><div>'+summary+kb_references(content)+'</div><aside>'+kb_release_info(preview)+history+'</aside></div>'+bottom+extras


def deep_kb_upload(content):
    # 文件队列、解析进度及设置表单均使用原节点，操作栏与设计稿一致。
    requirement=figma_find(content,'card','<h2>文件要求</h2>')
    requirement_html=kb_slice(content,requirement)
    content=figma_replace(content,requirement,'')
    layout=figma_find(content,'form-layout')
    block=kb_slice(content,layout)
    note_node=figma_find(block,'note')
    if note_node:
        note_html=kb_slice(block,note_node)
        content=content.replace(note_html,'',1)
        first=figma_find(content,'card')
        at=content.rfind('</section>',first['inner'],first['end'])
        content=content[:at]+note_html+content[at:]
        first=figma_find(content,'card')
        content=content[:first['end']]+requirement_html+content[first['end']:]
    info=figma_find(content,'upload-info')
    info_html=kb_slice(content,info)
    if info:
        content=figma_replace(content,info,'')
        settings=figma_find(content,'card','<h2>入库设置</h2>')
        at=content.rfind('</section>',settings['inner'],settings['end'])
        content=content[:at]+info_html+content[at:]
    button=re.search(r'<button\b[^>]*id="parse-files".*?</button>',content,re.S)[0]
    content=content.replace(button,'')
    content=content.replace('<div class="form-actions">','<div class="form-actions deep-kb-bottom"><p>选好文件并核对入库设置后，点击解析预览。</p>',1)
    actions=figma_find(content,'form-actions')
    if actions:
        at=content.rfind('</div>',actions['inner'],actions['end'])
        content=content[:at]+button+content[at:]
    content=content.replace('class="form-layout"','class="form-layout deep-kb-layout deep-kb-upload-layout"',1)
    for title,key in [('选择来源文件','imgFrame5'),('入库设置','imgFrame3'),('文件要求','imgFrame7')]:
        content=content.replace('<h2>'+title+'</h2>','<h2>'+figma_image('deep-kb-upload',key,'')+title+'</h2>')
    return content


def deep_kb_content(content,name):
    if name=='knowledge-edit':return deep_kb_edit(content)
    if name in ['knowledge-detail','knowledge-preview']:return deep_kb_read(content,name=='knowledge-preview')
    if name=='knowledge-upload':return deep_kb_upload(content)
    if name=='knowledge-files':
        tabs=kb_slice(content,figma_find(content,'tabs'))
        content=content.replace(tabs,'',1)
        content=content.replace('<h2><div class="small-heading">','<h2><div class="small-heading">',1)
        card_node=figma_find(content,'card')
        if card_node:content=content[:card_node['inner']]+tabs+content[card_node['inner']:]
    if name=='knowledge-offline':
        original=kb_slice(content,figma_find(content,'card'))
        target='<div class="deep-kb-modal-target"><b data-bind="knowledge.title">宿舍水电费线上缴纳指南</b><small>知-0001 · 版本3 · 当前已上线</small></div>'
        original=original.replace('<form action="knowledge-archived.html"',target+'<form action="knowledge-archived.html"')
        return '<div class="deep-kb-offline-context" inert aria-hidden="true">'+deep_kb_read(CONTENTS['admin/pc/knowledge-detail.html'])+'</div><div class="deep-kb-overlay"><section class="deep-kb-modal" role="dialog" aria-modal="true" aria-label="下线知识确认"><header><h2><span class="deep-kb-modal-symbol">'+figma_image('deep-kb-offline','imgFrame10','')+'</span>下线知识确认</h2>'+link('knowledge-detail.html','关闭','deep-kb-close')+'</header>'+original+'</section></div>'
    return content


def deep_kb_skin(body,name):
    if not name.startswith('knowledge'):return body
    breadcrumb='<div class="deep-kb-toolbar"><div>'+icon('fa-house')+' 首页 / '+link('knowledge.html','知识库管理','deep-kb-crumb')+'</div></div>'
    body=body.replace('<main class="main">','<main class="main">'+breadcrumb,1)
    # 页面保留原型导航及原有账户入口，头像采用同一设计稿的素材。
    body=body.replace('<span class="avatar">管</span>',figma_image('deep-kb-edit','img1','管理员头像','deep-kb-avatar'))
    body=body.replace('<div class="section-label">管理控制台</div>','')
    body=body.replace('<a class="nav-item active" href="knowledge.html">','<div class="section-label">日常协作</div><a class="nav-item active" href="knowledge.html">',1)
    body=body.replace('<a class="nav-item" href="feedback.html">','<div class="section-label">其他服务</div><a class="nav-item" href="feedback.html">',1)
    return body

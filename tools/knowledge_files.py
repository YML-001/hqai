# 知识文件上传原型扩展：与主构建器共用布局，样式和交互内联到每页。
UPLOAD_STYLE = '''<style>
.upload-steps{display:flex;gap:22px;margin-bottom:25px;font-size:13px;color:#94a1b3}.upload-steps span{display:flex;gap:9px;align-items:center}.upload-steps b{display:grid;place-items:center;width:24px;height:24px;border:1px solid #dce5f1;border-radius:50%;font-size:12px}.upload-steps .current{color:var(--blue)}.upload-steps .current b{background:var(--blue);border-color:var(--blue);color:#fff}.drop-zone{border:1.5px dashed #bbd2f5;border-radius:14px;background:#f7faff;text-align:center;padding:43px 20px;transition:.15s}.drop-zone.dragging{border-color:var(--blue);background:#e9f2ff}.drop-zone>i{font-size:34px;color:var(--blue);margin-bottom:16px}.drop-zone h3{font-size:17px;margin-bottom:8px}.drop-zone p{font-size:12px;margin-bottom:19px}.upload-file-row{display:flex;align-items:center;justify-content:space-between;gap:20px;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-top:10px}.upload-file-row strong{font-weight:500;overflow-wrap:anywhere}.upload-file-row small{display:block;margin-top:3px}.upload-error{color:var(--red);font-size:12px;margin-top:16px;white-space:pre-line}button:disabled{opacity:.45;cursor:not-allowed}.file-text-preview{background:#fafcff;min-height:230px;line-height:1.9;font-size:13px;margin:4px 0 16px}.file-chunk{border:1px solid var(--line);border-radius:9px;margin-top:12px;padding:13px 16px}.file-chunk summary{cursor:pointer;color:#5278ab}.file-chunk p{white-space:pre-wrap;font-size:13px;margin-top:12px}.file-body{font-family:inherit;font-size:13px;line-height:1.95;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;max-height:520px;overflow:auto}.upload-info{border-radius:12px;padding:17px;background:#f7faff;margin-top:20px}.upload-info strong{display:block;margin-bottom:8px}.upload-info p{margin:0;font-size:12px}.upload-status{font-size:12px;margin-top:16px;min-height:20px}progress{display:block;width:100%;height:7px;margin:18px 0;accent-color:var(--blue)}progress[hidden]{display:none}[hidden]{display:none!important}.source-card a{white-space:normal}.file-title{overflow-wrap:anywhere}.file-stats{display:flex;gap:24px;color:#8795a9;font-size:12px;margin:8px 0 24px}.file-stats b{color:#426da5;margin-right:5px}@media(max-width:700px){.upload-steps{gap:10px;font-size:11px}.drop-zone{padding:30px 15px}}
</style>'''
FILE_JS = '<script>' + (ROOT/'tools/knowledge_files.js').read_text() + '</script>'
LIBRARIES = '<script src="../../assets/vendor/mammoth.browser.min.js"></script><script src="../../assets/vendor/pdf.min.js"></script>'
def upload_steps(active):
    return '<div class="upload-steps">'+''.join(f'<span class="{"current" if i==active else ""}"><b>{i}</b>{t}</span>' for i,t in [(1,'上传文件'),(2,'解析与预览'),(3,'确认入库')])+'</div>'
def knowledge_page(name,title,content,libraries=False):
    adminout(name,title,UPLOAD_STYLE+content+(LIBRARIES if libraries else '')+FILE_JS,'knowledge')
def replace_knowledge(name,content):
    path='admin/pc/'+name+'.html'
    item=next(p for p in PAGES if p['path']==path)
    PAGES[:]=[p for p in PAGES if p['path']!=path]
    knowledge_page(name,item['title'],content)

# 知识管理同时保留手工问答与来源文件两种维护方式。
main=CONTENTS['admin/pc/knowledge.html']
main=main.replace(link('knowledge-edit.html','新增知识','btn primary','fa-plus'),'<div class="actions">'+link('knowledge-edit.html','新增知识','btn','fa-plus')+link('knowledge-upload.html','上传文件','btn primary','fa-cloud-arrow-up')+'</div>')
main=main.replace('<section class="card "><h2>知识条目</h2>','<div class="tabs">'+link('knowledge.html','问答知识','active')+link('knowledge-files.html','来源文件')+'</div><section class="card "><h2>知识条目</h2>')
replace_knowledge('knowledge',main)

edit=CONTENTS['admin/pc/knowledge-edit.html']
edit=edit.replace('<h2>引用依据</h2>','<h2>引用依据</h2><div class="source-card" data-kb-attachments></div><hr class="divider">')
replace_knowledge('knowledge-edit',edit)
for name in ['knowledge-preview','knowledge-detail']:
    body=CONTENTS['admin/pc/'+name+'.html']
    marker='<dl class="summary-list">'
    body=body.replace(marker,marker+'<div><dt>关联来源文件</dt><dd><a data-kb-linked-source>未关联文件</a></dd></div>',1)
    replace_knowledge(name,body)

upload=heading('上传知识文件','把已有文档，整理成有依据的后勤知识',link('knowledge-files.html','文件管理','btn','fa-folder-open'))+upload_steps(1)
upload+='<div class="form-layout"><div>'+card('选择来源文件','<div class="drop-zone" id="drop-zone">'+icon('fa-cloud-arrow-up')+'<h3>将文件拖到这里，或点击选择文件</h3><p>支持PDF、DOCX、TXT、Markdown · 单个不超过20MB · 每批最多10个</p><label class="btn primary" for="knowledge-file-input" style="cursor:pointer">'+icon('fa-plus')+' 选择文件</label><input id="knowledge-file-input" class="sr-only" type="file" multiple accept=".pdf,.docx,.txt,.md" aria-label="选择知识文件"></div><div class="small-heading" style="margin-top:24px"><h3 id="queue-count">暂未选择文件</h3><span class="muted">上传前可以移除文件</span></div><div id="upload-queue"></div><div id="upload-status" class="upload-status" role="status" aria-live="polite"></div><progress id="upload-progress" max="10" value="0" hidden aria-label="文件解析进度"></progress>')+note('文件解析不会自动上线。确认入库前，请核对文档正文、来源时效与可见范围。')+'</div><div>'+card('入库设置','<form id="file-settings">'+field('所属分类',name='category',options=['水电缴纳','报修','班车','其他办事'])+field('可见范围',name='visibility',options=['公开','仅学生','仅教职工'])+field('维护责任人','张老师',name='owner')+field('资料截止日期','2026-09-17','date','sourceDate')+'</form>')+card('文件要求','<ul class="check-list"><li>DOCX需包含可复制的正文，旧版DOC请转换后上传。</li><li>PDF最多100页；扫描件先完成文字识别，加密文件先解除密码。</li><li>正文最多20万字，超出时请拆分。</li><li>收费、电话与服务时间请以最新公示核实。</li></ul><div class="upload-info"><strong>文件内容保留在当前浏览器</strong><p>当前原型在本地解析文件，尚未上传至服务器。</p></div>')+'</div></div><div class="form-actions">'+link('knowledge.html','返回知识库')+'<button class="btn primary" id="parse-files" disabled>'+icon('fa-wand-magic-sparkles')+' 解析并预览</button></div>'
upload = upload.replace('<button class="btn primary" id="parse-files" disabled>'+icon('fa-wand-magic-sparkles')+' 解析并预览</button>', '')
upload = upload.replace('</progress>', '</progress><div class="actions" style="justify-content:flex-end;margin-top:22px"><button class="btn primary" id="parse-files" disabled>'+icon('fa-wand-magic-sparkles')+' 解析并预览</button></div>')
knowledge_page('knowledge-upload','上传知识文件',upload,True)

preview=heading('解析与预览','检查识别出的正文，确认可见范围后再入库')+upload_steps(2)+'<div class="note amber" id="partial-errors" hidden style="display:block"></div><div class="file-stats"><span><b id="parsed-count">0个文件解析完成</b></span><span>文件正文将按正文长度切分为知识片段</span></div><div id="parsed-files"></div>'+card('确认入库','<form id="confirm-files"><label class="checkline"><input type="checkbox" required><span>我已核对解析正文、来源时效及可见范围，确认这些文件可以入库供后勤问答使用。</span></label><p class="muted">尚未确认的文件保持“待确认”状态，不参与问答；本原型只演示知识入库，未连接真实检索服务。</p><div class="form-actions">'+link('knowledge-upload.html','继续添加文件')+'<button class="btn primary">确认入库</button></div></form>')
knowledge_page('knowledge-upload-preview','知识文件解析预览',preview)

success=upload_steps(3)+card('','<div class="success"><div class="success-mark">'+icon('fa-check')+'</div><h1 data-kb-success>文件已确认入库</h1><p>文件和识别出的知识片段已保留在当前浏览器，可在来源文件中查看，也可以关联到问答知识的引用依据。</p><div class="actions" style="justify-content:center">'+link('knowledge-files.html','查看文件列表','btn primary')+link('knowledge-edit.html','返回编辑知识')+link('knowledge-upload.html','继续上传')+'</div></div>')
knowledge_page('knowledge-upload-success','知识文件入库完成',success)

files=heading('知识库管理','管理原始文档、解析内容与可见范围',link('knowledge-upload.html','上传文件','btn primary','fa-cloud-arrow-up'))+'<div class="tabs">'+link('knowledge.html','问答知识')+link('knowledge-files.html','来源文件','active')+'</div>'+note('已入库文件可作为问答引用依据；待确认文件不会参与问答。解析失败时请按提示修正文件后重新上传。')+card('<div class="small-heading"><span>来源文件</span><span id="file-total" class="muted">0个文件</span></div>','<div class="filters"><input id="file-search" aria-label="搜索来源文件" placeholder="搜索文件名、分类、状态或维护人"></div><div class="table-wrap"><table><thead><tr>'+''.join('<th>'+t+'</th>' for t in ['文件名称','分类','入库状态','可见范围','上传时间','操作'])+'</tr></thead><tbody id="knowledge-file-list"></tbody></table></div><div class="empty" id="files-empty">'+icon('fa-folder-open')+'<h3>暂无匹配的来源文件</h3><p>上传后可以核对正文、确认入库，并在问答知识中关联来源。</p>'+link('knowledge-upload.html','上传第一份文件','btn primary')+'</div>')
knowledge_page('knowledge-files','知识来源文件管理',files)

detail=heading('来源文件详情','追溯原始依据，核对解析正文与知识片段',link('knowledge-files.html','返回文件列表','btn'))+'<div id="knowledge-file-detail">'+card('<span class="file-title" id="file-name">来源文档</span>','<p id="file-metadata" class="muted"></p><p id="file-origin" class="muted"></p>')+'<div class="grid2">'+card('解析正文','<pre id="file-body" class="file-body"></pre>')+card('知识片段','<p class="muted">每个片段最多800字，相邻片段保留100字上下文，正式分段规则可在开发时配置。</p><div id="file-chunks" style="max-height:520px;overflow:auto"></div>')+'</div></div>'
knowledge_page('knowledge-file-detail','知识来源文件详情',detail)

error=heading('文件解析未完成','根据失败原因调整文件后，可以重新上传')+upload_steps(2)+card('需要处理的文件','<div id="failed-files"></div><div class="form-actions">'+link('knowledge-files.html','查看文件列表')+link('knowledge-upload.html','返回重新上传','btn primary')+'</div>')+note('无法识别正文的扫描PDF需要先完成文字识别；加密、损坏或格式错误的文档不会入库。')
knowledge_page('knowledge-upload-error','知识文件上传失败',error)

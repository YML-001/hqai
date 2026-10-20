# 学生消息使用独立的示例内容与阅读状态，不复用教职工会议数据。
def build_student_notification_pages():
    notices=[
        dict(id='student-maintenance',page='notification-detail',title='宿舍热水服务维护提醒',kind='服务通知',time='2026-10-20 15:00',text='演示提醒：宿舍热水设备计划维护，实际影响范围与恢复时间以能源管理中心正式公告为准。',target='contacts.html',action='查看服务中心联系方式'),
        dict(id='student-guide',page='notification-service',title='后勤办事指引已更新',kind='平台通知',time='2026-10-20 10:00',text='服务大厅现可查看报修、水电、班车等办事指引。办理步骤与终端入口将按后台发布内容同步展示。',target='services.html',action='查看服务大厅'),
    ]
    def empty():
        return '<div class="notification-empty"><div class="notification-empty-icon">'+icon('fa-bell-slash')+'</div><h2>暂无未读消息</h2><p>新的服务通知会显示在这里，你可以继续向后勤小助提问。</p>'+link('home.html','返回智能问答','btn primary')+'</div>'
    for port in ['pc','mobile']:
        def emit(name,title,body):
            output(f'student/{port}/{name}.html',title,body,role='student',port=port,active='home')
        for unread in [False,True]:
            tabs='<div class="notification-tabs"><div class="tabs">'+link('notifications.html','全部消息','' if unread else 'active')+link('notifications-unread.html','未读 <span data-unread-total>2</span>','active' if unread else '')+'</div><button class="btn sm" data-mark-all-read>全部标为已读</button></div>'
            rows='<div class="notification-list" data-notification-list="'+('unread' if unread else 'all')+'">'
            for n in notices:
                rows+='<a class="notification-item" data-notification-id="'+n['id']+'" href="'+n['page']+'.html"><div class="notification-icon">'+icon('fa-bell')+'</div><div><div class="notification-meta">'+n['kind']+' <span class="badge" data-notification-status="'+n['id']+'">未读</span></div><h3>'+n['title']+'</h3><p>'+n['text']+'</p><span class="notification-time">'+n['time']+' · 后勤服务演示</span></div>'+icon('fa-chevron-right row-chevron')+'</a>'
            rows+='</div>'
            if unread:rows+='<div data-notification-empty hidden>'+empty()+'</div>'
            body=heading('消息通知','服务动态，在问答页铃铛里及时查看')+'<div class="notification-summary"><p>本人消息，<strong><span data-unread-total>2</span>条未读</strong></p>'+badge('陈同学 · 2026******12','gray')+'</div>'+card('',tabs+rows)+note('消息内容为设计演示，未接入学校真实通知。学生与教职工消息按身份隔离，阅读状态仅影响本人。')
            emit('notifications-unread' if unread else 'notifications','未读消息' if unread else '消息通知',body)
        emit('notifications-empty','消息通知空状态',heading('消息通知','无消息时的独立展示状态')+card('',empty())+note('此页仅展示空状态样式，不修改本人未读消息。'))
        for n in notices:
            body=heading('消息详情','进入详情后自动标为本人已读',link('notifications.html','返回消息'))+'<div data-notification-detail="'+n['id']+'">'+card(n['title'],badge(n['kind'])+' <span class="badge gray" data-notification-status="'+n['id']+'">已读</span><p class="notification-detail-intro" style="margin-top:22px">陈同学，你好：<br>'+n['text']+'</p>'+details([('通知时间',n['time']),('通知对象','陈同学 · 学生'),('发布方','后勤服务 · 演示')])+'<div class="actions" style="margin-top:22px">'+link(n['target'],n['action'],'btn primary')+link('notifications-unread.html','查看其他未读')+'</div>')+'</div>'+note('此处不展示教职工会议或其他用户的个人消息。')
            emit(n['page'],'学生消息详情 · '+n['kind'],body)

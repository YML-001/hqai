# -*- coding: utf-8 -*-
# 站内通知沿用既有角色、页面布局与本地演示方式。
NOTIFICATION_STYLE = '''<style>
.notification-bell,[data-notification-link]{position:relative;display:inline-flex;align-items:center;gap:8px;min-height:34px;color:#5d7492}.notification-bell>i,[data-notification-link]>i{font-size:18px}[data-unread-count]{display:inline-grid;place-items:center;min-width:19px;height:19px;padding:0 5px;border-radius:10px;background:#e45d63;color:#fff;font-size:10px;line-height:19px}.notification-bell [data-unread-count],[data-notification-link] [data-unread-count]{position:absolute;top:-5px;right:-9px;border:2px solid #fff;min-width:20px;height:20px;line-height:16px}.notification-summary{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:22px}.notification-summary p{margin:0}.notification-summary strong{color:var(--blue);font-weight:600}.notification-tabs{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);margin-bottom:0;padding-bottom:13px}.notification-tabs .tabs{border:0;margin:0;gap:28px}.notification-tabs .tabs a{padding:8px 0}.notification-list{display:grid;gap:0}.notification-item{display:grid;grid-template-columns:48px minmax(0,1fr) 18px;gap:18px;padding:25px 2px;border-bottom:1px solid var(--line);align-items:start}.notification-item:last-child{border:0}.notification-item:hover{background:#f9fbff;color:inherit}.notification-icon{display:grid;place-items:center;width:45px;height:45px;border-radius:13px;background:#edf4ff;color:var(--blue);font-size:18px}.notification-icon.amber{background:#fff5e7;color:#b17d38}.notification-icon.gray{background:#f0f3f8;color:#8490a1}.notification-meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:8px;font-size:11px;color:#8a97a9}.notification-item h3{font-size:15px;font-weight:600;margin-bottom:8px}.notification-item p{font-size:12px;margin-bottom:7px;line-height:1.8}.notification-item .notification-time{font-size:11px;color:#9aa6b5}.notification-item .row-chevron{margin-top:23px;font-size:12px}.notification-is-read .notification-icon{opacity:.65}.notification-is-read h3{font-weight:500}.notification-unread-tag{background:#edf4ff;color:var(--blue)}.notification-detail-hero{display:flex;gap:19px;align-items:center;margin:0 0 24px;padding-bottom:24px;border-bottom:1px solid var(--line)}.notification-detail-hero .notification-icon{width:55px;height:55px;font-size:23px}.notification-detail-hero h2{font-size:21px;margin:7px 0 0}.notification-detail-intro{font-size:14px;line-height:1.95;color:#566983}.notification-channel-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px;margin:18px 0}.notification-channel{background:#f8faff;border:1px solid #e1eaf7;border-radius:12px;padding:18px}.notification-channel h3{color:#466a9b;font-size:14px;margin-bottom:10px}.notification-channel p{font-size:12px;margin:8px 0 0}.notification-channel-choice{display:flex;gap:12px;border:1px solid var(--line);border-radius:10px;padding:15px 12px;margin-bottom:11px;align-items:flex-start}.notification-channel-choice input{width:auto;margin-top:5px;accent-color:var(--blue)}.notification-channel-choice span{font-size:13px;display:block}.notification-channel-choice small{display:block;margin-top:5px;line-height:1.8}.notification-channel-choice b{font-weight:600;color:#496889}.notification-mini-entry{display:flex;align-items:center;justify-content:space-between;gap:15px}.notification-mini-entry .notification-icon{flex-shrink:0}.notification-mini-entry h3{margin:0 0 5px}.notification-mini-entry p{margin:0;font-size:12px}.notification-empty{text-align:center;padding:65px 22px}.notification-empty-icon{display:grid;place-items:center;width:76px;height:76px;border-radius:50%;background:#f0f5fe;color:#9db9df;font-size:30px;margin:0 auto 23px}.notification-empty h2{margin-bottom:12px}.notification-empty p{font-size:13px;margin-bottom:23px}.notification-change-box{padding:17px;border-radius:10px;background:#f8faff;border:1px solid var(--line);margin:18px 0}.notification-change-box p{font-size:13px;margin:0 0 8px}.notification-change-box p:last-child{margin:0}.notification-change-box del{color:#99a4b3}.notification-heading-label{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.notification-heading-label .badge{margin-top:3px}.notification-records td{min-width:110px}.notification-local-hint{font-size:11px;color:#899bb2;margin-top:15px}.notification-cancelled-banner{border-left:3px solid #a0adbf;background:#f6f8fb;padding:15px 17px;margin:15px 0;color:#74849b}.notification-unread-inline{display:inline-flex;align-items:center;gap:4px;color:var(--blue)}[hidden]{display:none!important}
.mobile .notification-label,.mobile .notification-bell .desktop-link{display:none}.mobile .notification-bell,[data-notification-link]{flex-shrink:0}.mobile .notification-summary{align-items:flex-start;gap:12px;margin-bottom:17px}.mobile .notification-summary p{font-size:12px}.mobile .notification-tabs .tabs{gap:21px}.mobile .notification-tabs>.btn{font-size:11px;padding:5px 9px}.mobile .notification-item{grid-template-columns:36px minmax(0,1fr) 9px;gap:11px;padding:21px 0}.mobile .notification-icon{width:35px;height:35px;border-radius:10px;font-size:15px}.mobile .notification-item h3{font-size:14px}.mobile .notification-meta{font-size:10px;gap:7px}.mobile .notification-item p{font-size:12px}.mobile .notification-channel-grid{grid-template-columns:1fr;gap:12px}.mobile .notification-detail-hero{gap:14px}.mobile .notification-detail-hero h2{font-size:18px}.mobile .notification-detail-hero .notification-icon{width:44px;height:44px;font-size:19px}.mobile .notification-empty{padding:45px 8px}.mobile .notification-mini-entry{gap:12px}.mobile .notification-mini-entry .btn{padding:6px 10px;font-size:11px}.mobile .notification-mini-entry h3{font-size:14px}.mobile .notification-mini-entry p{font-size:11px}@media(max-width:700px){.notification-channel-grid{grid-template-columns:1fr}.notification-bell .notification-label{display:none}}
</style>'''

def notification_assets(role, port):
    if role not in ['student', 'staff', 'admin']:
        return ''
    context={'recipient':'student-2026000012','ids':['student-maintenance','student-guide'],'label':'消息通知'} if role=='student' else {'recipient':'staff-20000118','ids':['notice-reminder','notice-change','notice-cancelled'],'label':'站内通知'}
    return NOTIFICATION_STYLE + '<script>window.CSU_NOTIFICATION_CONTEXT='+json.dumps(context,ensure_ascii=False)+';</script><script>' + (ROOT/'tools/notifications.js').read_text() + '</script>'


def build_notification_pages():
    notices = [
        dict(id='notice-cancelled', kind='会议取消', icon='fa-calendar-xmark', color='gray', title='原定服务协调会已取消', meeting='原定服务协调会', time='2026-10-20 16:10', when='2026年10月22日 14:30—15:30', place='后勤保障部会议室', text='会议因安排调整取消，请勿按原安排参会。', page='notification-cancelled', target='meeting-cancelled'),
        dict(id='notice-change', kind='会议变更', icon='fa-pen-to-square', color='amber', title='校园环境服务专题会安排有变更', meeting='校园环境服务专题会', time='2026-10-20 14:20', when='2026年10月22日 15:00—16:00', place='后勤保障部第二会议室', text='开始时间由14:30调整至15:00，地点调整为第二会议室。', page='notification-change', target='meeting-changed'),
        dict(id='notice-reminder', kind='会前提醒', icon='fa-bell', color='', title='后勤安全保障例会即将开始', meeting='后勤安全保障例会', time='2026-10-20 08:00', when='2026年10月20日 09:00—10:00', place='后勤保障部会议室', text='会议将在1小时后开始，请提前安排时间，准时参会。', page='notification-detail', target='meeting-reminded'),
    ]

    def replace_page(path, body, active=None):
        item = next(p.copy() for p in PAGES if p['path'] == path)
        PAGES[:] = [p for p in PAGES if p['path'] != path]
        current_active = active or ('notifications' if 'notification' in Path(path).stem else 'meetings')
        output(path, item['title'], body, role=item['role'], port=item['port'], active=current_active, section=item.get('section', ''))

    # 重新输出旧页面，使新导航与未读标记在所有教职工页面保持一致。
    for item in list(PAGES):
        if item['role'] != 'staff':
            continue
        path = item['path']
        name = Path(path).stem
        body = CONTENTS[path]
        body = body.replace('会前1小时通过ITS提醒', '会前1小时通过站内通知与ITS提醒')
        body = body.replace('学校ITS · 按工号投递', '站内通知 + 学校ITS · 按工号投递')
        body = body.replace('所有日程为演示数据；真实ITS通知将按工号投递。', '本人会议可在系统内接收通知，同时保留独立的ITS提醒。此处均为演示数据。')
        body = body.replace('公开问答、教职工服务、本人会议', '公开问答、教职工服务、本人会议与站内通知')
        if name == 'home':
            notice_entry = card('', '<div class="notification-mini-entry"><div class="notification-icon">'+icon('fa-bell')+'</div><div style="flex:1"><h3>我的站内通知</h3><p><span class="notification-unread-inline"><b data-unread-total>3</b>条未读</span> · 会前提醒、会议变更与取消</p></div>'+link('notifications.html', '查看通知', 'btn sm')+'</div>')
            marker = '<section class="card "><h2>下一场会议</h2>'
            body = body.replace(marker, notice_entry + marker, 1)
        if name == 'profile':
            body = body.replace('<h2>账户与隐私</h2>', '<h2>账户与隐私</h2>'+link('notifications.html', icon('fa-bell')+' 站内通知 <span class="notification-unread-inline"><b data-unread-total>3</b>条未读</span>', 'list-row'))
        active = 'home' if name in ['home', 'assistant'] or name.startswith(('chat', 'voice')) else 'profile' if name == 'profile' else 'services' if name not in ['meetings', 'meeting-detail', 'meeting-cancelled'] else 'meetings'
        replace_page(path, body, active)

    def notice_row(n):
        return '<a class="notification-item" data-notification-id="'+n['id']+'" href="'+n['page']+'.html"><div class="notification-icon '+n['color']+'">'+icon(n['icon'])+'</div><div><div class="notification-meta"><span>'+n['kind']+'</span><span data-notification-status="'+n['id']+'" class="badge notification-unread-tag">未读</span></div><h3>'+n['title']+'</h3><p>'+n['text']+'</p><span class="notification-time">'+n['time']+' · 后勤保障部</span></div>'+icon('fa-chevron-right row-chevron')+'</a>'

    def empty_body(example=False):
        return '<div class="notification-empty"><div class="notification-empty-icon">'+icon('fa-bell-slash')+'</div><h2>'+('暂无站内通知' if example else '未读通知已处理完毕')+'</h2><p>'+('新的会议提醒、变更与取消通知，将在这里展示。' if example else '后续的本人会议消息会继续显示在站内通知中。')+'</p>'+link('notifications.html', '查看全部通知', 'btn primary')+'</div>'

    def notification_list(unread=False):
        actions = '<button type="button" class="btn sm" data-mark-all-read>全部标为已读</button>'
        tabs = '<div class="notification-tabs"><div class="tabs">'+link('notifications.html', '全部通知', '' if unread else 'active')+link('notifications-unread.html', '未读 <span data-unread-total>3</span>', 'active' if unread else '')+'</div>'+actions+'</div>'
        description = '<div class="notification-summary"><p>仅接收本人参会相关消息，<strong><span data-unread-total>3</span>条未读</strong></p><span class="badge gray">陈老师 · 20****18</span></div>'
        items = '<div class="notification-list" data-notification-list="'+('unread' if unread else 'all')+'">'+''.join(notice_row(n) for n in notices)+'</div>'
        if unread:
            items += '<div data-notification-empty hidden>'+empty_body()+'</div>'
        return heading('站内通知', '会议消息，在后勤助手里也能及时查看')+description+card('', tabs+items)+note('站内通知与ITS分别投递、分别留痕。本站标为已读只影响本人站内阅读状态，不代表ITS已送达或已读。')

    for port in ['pc', 'mobile']:
        base = 'staff/'+port+'/'
        for name, title, body in [
            ('notifications', '站内通知', notification_list()),
            ('notifications-unread', '未读站内通知', notification_list(True)),
            ('notifications-empty', '站内通知空状态', heading('站内通知', '首次使用或没有消息时的独立展示状态')+card('', empty_body(True))+note('此页为无通知状态的设计示例，不清空本人演示通知或修改未读数。')),
        ]:
            output(base+name+'.html', title, body, role='staff', port=port, active='notifications')
        for n in notices:
            status = '<span data-notification-status="'+n['id']+'" class="badge gray">已读</span>'
            header = '<div class="notification-detail-hero"><div class="notification-icon '+n['color']+'">'+icon(n['icon'])+'</div><div><span class="badge '+n['color']+'">'+n['kind']+'</span><h2>'+n['title']+'</h2></div></div>'
            intro = '<p class="notification-detail-intro">陈老师，你好：<br>'+n['text']+'</p>'
            changed = ''
            if n['id'] == 'notice-change':
                changed = '<div class="notification-change-box"><p>原安排：<del>2026年10月22日 14:30—15:30 · 后勤保障部会议室</del></p><p><strong>最新安排：2026年10月22日 15:00—16:00 · 后勤保障部第二会议室</strong></p><p class="muted">变更原因：协调参会人员工作安排。</p></div>'
            if n['id'] == 'notice-cancelled':
                changed = '<div class="notification-cancelled-banner">原安排已失效。未发送的会前提醒已撤销，已到达的历史通知保留。</div>'
            info = details([('会议主题', n['meeting']), ('原定时间' if n['id']=='notice-cancelled' else '会议时间', n['when']), ('会议地点', n['place']), ('通知时间', n['time']), ('通知类型', n['kind']), ('通知对象', '陈老师 · 工号20****18'), ('站内状态', '已送达 · '+status)])
            body = heading(n['kind']+'详情', '点击进入详情后，自动标为本人已读', link('notifications.html', '返回通知'))+'<div data-notification-detail="'+n['id']+'">'+card('', header+intro+changed+info+'<div class="actions" style="margin-top:24px">'+link(n['target']+'.html', '查看已取消会议信息' if n['id']=='notice-cancelled' else '查看本人会议', 'btn primary')+link('notifications-unread.html', '查看其他未读')+'</div>')+'</div>'+note('这里展示后勤助手的站内通知；阅读状态仅记录当前本人身份，ITS回执由独立通道记录。')
            output(base+n['page']+'.html', n['kind']+'详情', body, role='staff', port=port, active='notifications')

        # 本人会议与三种通知建立明确链接，取消通知不会打开仍然有效的旧安排。
        meeting_body = heading('我的会议', '仅展示本人被列为参会人的日程', link('notifications.html', '站内通知', 'btn', 'fa-bell'))
        meeting_body += card('即将开始', '<div class="list-row"><div>'+badge('10月21日 09:30—10:30', 'green')+'<h2 style="margin:12px 0 6px">后勤服务保障工作协调会</h2><p>后勤保障部会议室 · 站内通知与ITS双通道提醒</p></div>'+link('meeting-detail.html', '会议详情', 'btn sm')+'</div><div class="list-row"><div>'+badge('已变更', 'amber')+'<h2 style="margin:12px 0 6px">校园环境服务专题会</h2><p>10月22日 15:00—16:00 · 后勤保障部第二会议室</p></div>'+link('meeting-changed.html', '最新安排', 'btn sm')+'</div>')
        meeting_body += card('历史与取消', link('meeting-reminded.html', '<div><h3>后勤安全保障例会</h3><p>10月20日 09:00—10:00 · 已结束</p></div>'+icon('fa-chevron-right'), 'list-row')+link('meeting-cancelled.html', '<div><h3>原定服务协调会</h3><p>原定10月22日 14:30—15:30 · 已取消</p></div>'+icon('fa-chevron-right'), 'list-row'))+note('会议通知可在系统内查看；ITS通知仍独立投递。会议不设置审批、报名或签到。')
        replace_page(base+'meetings.html', meeting_body)
        for name, title, meeting_title, state, when, place, intro in [
            ('meeting-reminded', '已提醒会议详情', '后勤安全保障例会', '已结束', '2026年10月20日 09:00—10:00', '后勤保障部会议室', '本次会议的会前提醒已生成站内通知，阅读通知不会改变ITS投递结果。'),
            ('meeting-changed', '变更后会议详情', '校园环境服务专题会', '已变更', '2026年10月22日 15:00—16:00', '后勤保障部第二会议室', '以此处最新安排参会。原时间14:30与原地点不再适用。'),
        ]:
            body = heading('本人会议安排', '仅本人可查看的参会信息')+card(meeting_title, badge(state, 'gray' if state=='已结束' else 'amber')+'<p style="margin-top:19px">'+intro+'</p>'+details([('会议时间', when), ('会议地点', place), ('参会身份', '陈老师 · 工号20****18'), ('组织单位', '后勤保障部'), ('提醒通道', '站内通知 + 学校ITS')])+link('meetings.html', '返回我的会议'))
            output(base+name+'.html', title, body, role='staff', port=port, active='meetings')
        cancelled = heading('已取消的会议', '原安排已失效，请勿按原时间地点参会')+card('原定服务协调会', badge('已取消', 'gray')+'<p style="margin-top:20px">取消说明：会议安排调整，原安排不再执行。</p>'+details([('原定时间', '2026年10月22日 14:30—15:30'), ('原定地点', '后勤保障部会议室'), ('取消时间', '2026年10月20日 16:10'), ('参会身份', '陈老师 · 工号20****18'), ('通知状态', '取消通知已送达站内，ITS状态独立记录'), ('会前提醒', '尚未发送的任务已撤销')])+'<div class="actions" style="margin-top:23px">'+link('notification-cancelled.html', '查看取消通知', 'btn primary')+link('meetings.html', '返回我的会议')+'</div>')
        replace_page(base+'meeting-cancelled.html', cancelled)

    channel_choices = '<div class="field"><label>提醒通道</label><label class="notification-channel-choice"><input type="checkbox" checked disabled aria-label="站内通知默认启用"><span><b>站内通知 · 默认启用</b><small>送达本人通知中心，支持未读提示及本人已读记录。</small></span></label><input type="hidden" name="station" value="站内通知"><label class="notification-channel-choice"><input type="checkbox" name="its" value="学校ITS" checked><span><b>学校ITS</b><small>按工号独立投递；通道受理与本站已读分别记录。</small></span></label></div>'
    form_body = CONTENTS['admin/pc/meeting-create.html']
    form_body = form_body.replace(field('提醒通道', name='channel', options=['学校ITS（按工号）']), channel_choices)
    form_body = form_body.replace('短信不是本期默认通道；系统不会以手机号代替工号。', '站内通知默认启用，ITS可独立配置；仅管理员名单中的本人接收通知。')
    replace_page('admin/pc/meeting-create.html', form_body)
    for name in ['meetings', 'meeting-preview', 'meeting-detail', 'meeting-cancel', 'meeting-cancelled', 'meeting-import-preview', 'meeting-import-success']:
        path = 'admin/pc/'+name+'.html'
        body = CONTENTS[path]
        body = body.replace('学校ITS · 工号投递', '<span data-meeting-channels>站内通知 + 学校ITS</span> · 工号匹配')
        body = body.replace('默认会前1小时通过ITS按工号提醒。同一会议在设定时点提醒一次，取消后撤销未发送任务。', '默认会前1小时向本人站内通知中心与ITS分别投递。每个通道独立记录结果；变更与取消另发通知，取消后撤销未发送的会前提醒。')
        body = body.replace('已投递的ITS通知无法撤回；如需补充通知，请按学校实际流程联系参会人。', '确认取消后向原参会人生成站内取消通知，并按原配置独立投递ITS；两通道历史消息保留，未发送的会前提醒撤销。')
        body = body.replace('未发送的提醒任务已撤销 · 演示状态', '未发送的会前提醒已撤销，站内取消通知已生成 · 演示状态')
        body = body.replace('并按有效名单创建ITS提醒任务。', '并按有效名单创建站内通知与独立的ITS提醒任务。')
        if name == 'meeting-detail':
            body += card('站内与ITS通知', '<div class="notification-channel-grid"><div class="notification-channel"><h3>'+icon('fa-bell')+' 站内通知</h3>'+badge('已配置 · 待计划时点', 'amber')+'<p>参会人可在电脑端、移动端通知中心查看。阅读状态按本人身份记录。</p></div><div class="notification-channel" data-meeting-its-card><h3>'+icon('fa-paper-plane')+' 学校ITS</h3><span class="badge amber" data-meeting-its-status>已配置 · 待计划时点</span><p data-meeting-its-description>使用工号独立投递；ITS成功、失败和回执不受本站阅读操作影响。</p></div></div>'+link('delivery.html', '分别查看两条通道的结果 →', 'textlink'))
        replace_page(path, body, 'meetings')

    station_status = lambda nid: '<span data-admin-station-status="'+nid+'" class="badge notification-unread-tag">已送达 · 本人未读</span>'
    delivery_body = heading('提醒记录', '两条通道，分别查看送达与阅读情况')+note('站内已送达、本人已读、ITS受理成功是不同状态，不能互相替代。以下为演示记录；站内本人已读与教职工通知中心同步。')
    delivery_body += card('按会议查看通道结果', '<div class="notification-records">'+table(['会议 / 通知类型', '通知时点', '站内通知', '学校ITS', '操作'], [
        ['后勤服务保障工作协调会<p>会前提醒 · 8人</p>', '2026-10-21 08:30', badge('待发送', 'amber'), badge('待发送', 'amber'), link('meeting-detail.html', '会议详情', 'textlink')],
        ['后勤安全保障例会<p>会前提醒 · 6人</p>', '2026-10-20 08:00', badge('6人已送达', 'green'), badge('5人成功 / 1人失败', 'red'), link('delivery-detail.html', '通道详情', 'textlink')],
        ['校园环境服务专题会<p>会议变更 · 陈老师</p>', '2026-10-20 14:20', station_status('notice-change'), badge('ITS已受理', 'green'), link('meeting-notifications.html', '变更与取消记录', 'textlink')],
        ['原定服务协调会<p>取消通知 · 陈老师</p>', '2026-10-20 16:10', station_status('notice-cancelled'), badge('ITS已受理', 'green'), link('meeting-notifications.html', '变更与取消记录', 'textlink')],
    ])+'</div>')
    replace_page('admin/pc/delivery.html', delivery_body, 'delivery')
    detail_body = heading('后勤安全保障例会', '会前提醒 · 2026年10月20日08:00 · 6位接收人')+'<div class="notification-channel-grid"><div class="notification-channel"><h3>'+icon('fa-bell')+' 站内通道</h3>'+badge('6人已送达', 'green')+'<p>陈老师：<span data-admin-station-status="notice-reminder">已送达 · 本人未读</span></p><p>其他接收人的阅读状态仅作固定演示，不能据此推断ITS回执。</p></div><div class="notification-channel"><h3>'+icon('fa-paper-plane')+' ITS通道</h3>'+badge('5人成功 / 1人失败', 'red')+'<p>仅张老师通道响应超时，可独立重试ITS。</p><p>本站送达成功的人员不会因ITS重试收到重复站内通知。</p></div></div>'
    detail_body += card('按接收人查看独立状态', '<div class="notification-records">'+table(['接收人', '工号', '站内送达', '站内阅读', 'ITS投递', 'ITS回执 / 操作'], [
        ['陈老师', '20****18', badge('已送达', 'green'), station_status('notice-reminder'), badge('ITS已受理', 'green'), '不代表ITS已读'],
        ['张老师', '20****19', badge('已送达', 'green'), badge('未读 · 演示', 'gray'), badge('失败', 'red'), '通道响应超时<br>'+link('delivery-retry.html', '仅重试ITS', 'textlink')],
        ['其他4位接收人', '已脱敏', badge('4人已送达', 'green'), '2人已读 / 2人未读 · 演示', badge('4人ITS已受理', 'green'), '各通道独立留痕'],
    ])+'</div>')+note('站内送达是通知已进入本人通知中心，站内已读只说明本人打开了本站详情。ITS受理成功不等于对方已阅读。')+link('delivery.html', '返回提醒记录')
    replace_page('admin/pc/delivery-detail.html', detail_body, 'delivery')
    for name in ['delivery-retry', 'delivery-retried']:
        path = 'admin/pc/'+name+'.html'
        body = CONTENTS[path]
        body = body.replace('仅重试失败对象', '仅重试ITS失败对象').replace('确认重试范围', '确认ITS通道重试范围')
        body = body.replace('本页演示人工重试。', '本页只重试失败的ITS通道，站内通知不重复发送。')
        body = body.replace('失败对象张老师：模拟投递成功。', '失败对象张老师：模拟ITS投递成功，原站内通知与阅读状态保持独立。')
        replace_page(path, body, 'delivery')
    changes = heading('变更与取消通知记录', '会议状态改变后，原参会人在系统内也能收到消息')+card('最近两次通知', '<div class="notification-records">'+table(['通知类型', '关联会议 / 接收人', '通知时间', '站内状态', 'ITS状态'], [
        [badge('会议变更', 'amber'), '校园环境服务专题会<p>陈老师 · 20****18</p>', '2026-10-20 14:20', station_status('notice-change'), badge('ITS已受理', 'green')],
        [badge('会议取消', 'gray'), '原定服务协调会<p>陈老师 · 20****18</p>', '2026-10-20 16:10', station_status('notice-cancelled'), badge('ITS已受理', 'green')],
    ])+'</div>')+note('变更和取消通知独立于会前提醒，不受“会前提醒只发送一次”限制。每次有效变更按会议版本与接收人分别去重；会议仍无审批。')+link('delivery.html', '返回提醒记录')
    output('admin/pc/meeting-notifications.html', '会议变更与取消通知记录', changes, role='admin', port='pc', active='delivery')

# 智能问答统一承载对话记录与本人通知入口。
def build_qa_navigation_pages():
    import re

    styles = '''<style data-qa-tools-style>
.qa-tools{display:flex;align-items:center;justify-content:space-between;gap:16px;margin:0 0 20px;min-height:42px;position:relative;z-index:1}.qa-tools-context{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:#7186a2;white-space:nowrap}.qa-tools-context>a{display:inline-flex;align-items:center;gap:8px;color:#5274a3;font-weight:500}.qa-tools-context>i{color:#7b9bc8}.qa-tools-actions{display:flex;align-items:center;gap:14px;padding-right:4px}.qa-tools .qa-history-entry{display:inline-flex;align-items:center;gap:8px;background:#fff;border-color:#dfe7f3;color:#5274a3;min-height:38px;font-size:12px;padding:9px 13px;white-space:nowrap;box-shadow:0 2px 4px #31548a03}.qa-tools .qa-history-entry:hover{border-color:#b5cef4;background:#f7faff;color:var(--blue)}.qa-tools .qa-notification-entry[data-notification-link]{display:inline-flex;align-items:center;justify-content:center;gap:0;min-height:38px;width:38px;height:38px;border:1px solid #dfe7f3;border-radius:10px;background:#fff;color:#5274a3;flex-shrink:0}.qa-tools .qa-notification-entry[data-notification-link]>i{font-size:16px}.qa-tools .qa-notification-entry[data-notification-link]:hover{border-color:#b5cef4;background:#f7faff;color:var(--blue)}.qa-tools .qa-notification-entry [data-unread-count]{top:-6px;right:-7px;min-width:19px;height:19px;font-size:9px;line-height:15px}.qa-tools a:focus-visible{outline:3px solid #a7c9ff;outline-offset:3px}.mobile .qa-tools{gap:9px;margin-bottom:15px;min-height:37px}.mobile .qa-tools-context{font-size:11px;gap:6px}.mobile .qa-tools-context>a{gap:6px}.mobile .qa-tools-actions{gap:10px;padding-right:3px}.mobile .qa-tools .qa-history-entry{font-size:11px;min-height:35px;padding:7px 10px;gap:6px;border-radius:9px}.mobile .qa-tools .qa-notification-entry[data-notification-link]{width:35px;height:35px;min-height:35px;border-radius:9px}.mobile .qa-tools .qa-notification-entry[data-notification-link]>i{font-size:15px}@media(max-width:360px){.mobile .qa-tools-context{font-size:10px}.mobile .qa-tools .qa-history-entry{padding:7px 8px}.mobile .qa-tools-actions{gap:8px}}
</style>'''

    def remove_entry_links(body):
        # 只移除个人中心入口，不影响会议中的上下文跳转。
        return re.sub(
            r'<a\b[^>]*\bhref=[\"\'](?:history|notifications)(?:-[^\"\']*)?\.html[\"\'][^>]*>.*?</a>',
            '', body, flags=re.S,
        )

    def remove_notification_card(body):
        marker = 'class="notification-mini-entry"'
        while marker in body:
            position = body.index(marker)
            start = body.rfind('<section', 0, position)
            end = body.find('</section>', position)
            if start < 0 or end < 0:
                break
            body = body[:start] + body[end + len('</section>'):]
        return body

    for item in list(PAGES):
        role = item['role']
        port = item['port']
        if role not in ['student', 'staff'] or port not in ['pc', 'mobile']:
            continue
        path = item['path']
        name = path.rsplit('/', 1)[-1].removesuffix('.html')
        is_question = name in ['home', 'assistant'] or name.startswith('chat')
        is_dependent = name.startswith(('history', 'notification'))
        if not (is_question or is_dependent or name == 'profile'):
            continue
        body = CONTENTS[path]
        page_title = item['title']
        if role == 'staff' and name == 'home':
            # 兼容旧首页地址，所有入口统一展示最新的智能问答。
            body = CONTENTS[f'staff/{port}/assistant.html']
            page_title = '教职工智能问答首页'
        if name == 'profile':
            body = remove_entry_links(body)
            active = 'profile'
        else:
            back = 'assistant.html' if role == 'staff' else 'home.html'
            if role == 'staff' and name != 'home':
                body = body.replace('href="home.html"', 'href="assistant.html"')
            if 'data-qa-tools' not in body:
                context = (
                    link(back, '返回智能问答', 'qa-back', 'fa-arrow-left')
                    if is_dependent else icon('fa-comment-dots') + '<span>智能问答</span>'
                )
                history = link(
                    'history.html', icon('fa-clock-rotate-left') + ' 对话记录',
                    'btn sm qa-history-entry',
                )
                notification = ''
                if role in ['student', 'staff']:
                    notification = (
                        '<a class="qa-notification-entry" href="notifications.html" '
                        'data-notification-link aria-label="消息通知" title="查看本人消息通知">'
                        + icon('fa-bell')
                        + '<span data-unread-count>'+('2' if role=='student' else '3')+'</span><span class="sr-only">消息通知</span></a>'
                    )
                toolbar = (
                    '<div class="qa-tools" data-qa-tools role="group" aria-label="智能问答工具">'
                    '<div class="qa-tools-context">' + context + '</div>'
                    '<div class="qa-tools-actions">' + history + notification + '</div></div>'
                )
                body = styles + toolbar + body
            active = 'home'
        PAGES[:] = [page for page in PAGES if page['path'] != path]
        output(path, page_title, body, role=role, port=port, active=active)

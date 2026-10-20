/* 登录提示保留当前意图；演示登录后仅返回允许的本地页面。 */
(() => {
  document.addEventListener('DOMContentLoaded', () => {
    const query = new URLSearchParams(location.search);
    const intent = query.get('intent') || 'home';
    const id = query.get('service') || '';
    const port = document.body.dataset.port === 'mobile' ? 'mobile' : 'pc';
    let services = window.CSU_SERVICE_DEFAULTS?.services || {};
    try {
      const saved = JSON.parse(localStorage.getItem('csu-prototype-service-content-v1') || 'null');
      services = { ...services, ...(saved?.services || {}) };
    } catch (_) {}
    const service = Object.prototype.hasOwnProperty.call(services, id) ? services[id] : null;
    const question = typeof read === 'function' ? read('question')?.text || '' : '';
    const params = new URLSearchParams();
    if (['service', 'personal', 'feedback'].includes(intent)) params.set('intent', intent);
    if (intent === 'service' && service) params.set('service', id);
    const suffix = params.size ? '?' + params.toString() : '';
    const reason = intent === 'personal' ? '这个问题需要获取本人的身份或业务信息。登录后将继续查询，不会在游客状态读取个人数据。'
      : intent === 'feedback' ? '提交问题反馈前，需要确认校园身份。公开知识和功能列表仍可直接浏览。'
      : service ? '使用“' + service.name + '”前，需要确认校园身份与适用范围。登录后返回该服务继续操作。'
      : '登录后可使用需要校园身份的后勤服务。';
    const title = document.querySelector('#access-title');
    if (title) title.textContent = intent === 'personal' ? '查询本人信息，需要先登录' : service ? '登录后使用' + service.name : '这项操作需要校园身份';
    const description = document.querySelector('#access-reason');
    if (description) description.textContent = reason;
    const pending = intent === 'personal' && question ? '刚才的问题：' + question : service ? '即将继续：' + service.name : '';
    for (const selector of ['#access-pending', '#login-pending']) {
      const node = document.querySelector(selector);
      if (node) { node.hidden = !pending; node.textContent = pending; }
    }
    const login = document.querySelector('#access-login');
    if (login) login.href = 'login.html' + suffix;
    document.querySelectorAll('a[href="login.html"]').forEach(link=>{link.href='login.html'+suffix;});
    const postpone = document.querySelector('#access-cancel');
    if (postpone) postpone.href = intent === 'service' ? 'services.html' : 'home.html';
    const cancel = document.querySelector('#login-cancel');
    if (cancel) cancel.href = intent === 'service' ? 'services.html' : 'home.html';
    document.querySelector('[data-context-login]')?.addEventListener('submit', event => {
      event.preventDefault();
      const role = new FormData(event.currentTarget).get('loginRole') === 'staff' ? 'staff' : 'student';
      if (question && intent === 'personal') {
        try { localStorage.setItem('csu-prototype-question-' + role, JSON.stringify({ text: question })); } catch (_) {}
      }
      let target = role === 'staff' ? 'assistant.html' : 'home.html';
      if (intent === 'personal') target = 'chat-personal.html';
      else if (intent === 'feedback') target = 'feedback.html';
      else if (intent === 'service' && service) target = 'service-guide.html?service=' + encodeURIComponent(id);
      location.href = '../../' + role + '/' + port + '/' + target;
    });
    const action = document.querySelector('[data-personal-action]');
    if (action) {
      const role = document.body.dataset.role;
      action.href = /报修|维修|进度/.test(question) ? 'repair.html' : /通知|会议/.test(question) ? (role === 'staff' ? 'meetings.html' : 'notifications.html') : /学号|工号|姓名|身份/.test(question) ? 'profile.html' : role === 'staff' ? 'utility-info.html' : 'utility-pay.html';
    }
  });
})();

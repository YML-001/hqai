/* 本次新增设计：本人站内通知与学校 ITS 独立记录，所有数据均为本地演示。 */
(() => {
  const context=window.CSU_NOTIFICATION_CONTEXT||{recipient:'staff-20000118',ids:['notice-reminder','notice-change','notice-cancelled'],label:'站内通知'};
  const recipient = context.recipient;
  const storageKey = 'csu-prototype-notifications-v1-' + recipient;
  const notificationIds = context.ids;
  let memoryRead = [];

  function readState() {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '{}');
      memoryRead = Array.isArray(value.read)?value.read.filter(id => notificationIds.includes(id)):[];
    } catch (_) {}
    return new Set(memoryRead);
  }

  function saveRead(ids) {
    memoryRead = [...ids];
    try {
      localStorage.setItem(storageKey, JSON.stringify({ recipient, read: memoryRead }));
    } catch (_) {}
    update();
  }

  function update() {
    const read = readState();
    const unread = notificationIds.length - read.size;
    document.querySelectorAll('[data-unread-count]').forEach(node => {
      node.textContent = String(unread);
      node.hidden = unread === 0;
      const bell = node.closest('[data-notification-link]') || node.closest('a');
      if (bell) bell.setAttribute('aria-label', context.label+'，' + unread + '条未读');
    });
    document.querySelectorAll('[data-unread-total]').forEach(node => { node.textContent = String(unread); });
    document.querySelectorAll('[data-notification-status]').forEach(node => {
      const isRead = read.has(node.dataset.notificationStatus);
      node.textContent = isRead ? '已读' : '未读';
      node.className = 'badge ' + (isRead ? 'gray' : 'notification-unread-tag');
    });
    document.querySelectorAll('[data-notification-id]').forEach(node => {
      const isRead = read.has(node.dataset.notificationId);
      node.classList.toggle('notification-is-read', isRead);
      const list = node.closest('[data-notification-list]');
      if (list) node.hidden = list.dataset.notificationList === 'unread' && isRead;
    });
    document.querySelectorAll('[data-notification-empty]').forEach(node => {
      node.hidden = unread !== 0;
    });
    document.querySelectorAll('[data-mark-all-read]').forEach(node => {
      node.disabled = unread === 0;
      node.textContent = unread === 0 ? '全部已读' : '全部标为已读';
    });
    document.querySelectorAll('[data-admin-station-status]').forEach(node => {
      const isRead = read.has(node.dataset.adminStationStatus);
      node.textContent = isRead ? '本人已读' : '已送达 · 本人未读';
      node.className = 'badge ' + (isRead ? 'green' : 'notification-unread-tag');
    });
  }

  function ready() {
    const detail = document.querySelector('[data-notification-detail]');
    if (detail && notificationIds.includes(detail.dataset.notificationDetail)) {
      const state = readState();
      state.add(detail.dataset.notificationDetail);
      saveRead(state);
    }
    document.querySelectorAll('[data-mark-all-read]').forEach(node => {
      node.addEventListener('click', () => {
        saveRead(new Set(notificationIds));
        if (typeof toast === 'function') toast('本人全部通知已标为已读');
      });
    });
    let saved;
    try { saved = JSON.parse(localStorage.getItem('csu-prototype-meeting') || 'null'); } catch (_) {}
    const itsChoice = document.querySelector('form[data-save="meeting"] input[name="its"]');
    if (itsChoice && saved && saved.station) itsChoice.checked = Boolean(saved.its);
    const channelNodes = document.querySelectorAll('[data-meeting-channels]');
    if (channelNodes.length) {
      channelNodes.forEach(node => {
        node.textContent = saved && saved.station ? '站内通知' + (saved.its ? ' + 学校ITS' : '') : '站内通知 + 学校ITS';
      });
    }
    const itsEnabled = !saved || !saved.station || Boolean(saved.its);
    document.querySelectorAll('[data-meeting-its-card]').forEach(card => {
      const status = card.querySelector('[data-meeting-its-status]');
      const description = card.querySelector('[data-meeting-its-description]');
      if (status) {
        status.textContent = itsEnabled ? '已配置 · 待计划时点' : '未启用';
        status.className = 'badge ' + (itsEnabled ? 'amber' : 'gray');
      }
      if (description) description.textContent = itsEnabled
        ? '使用工号独立投递；ITS成功、失败和回执不受本站阅读操作影响。'
        : '未启用，不向ITS投递。站内通知仍按计划发送至本人通知中心。';
    });
    update();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
  window.addEventListener('storage', event => { if (event.key === storageKey) update(); });
  window.addEventListener('pageshow', update);
  window.addEventListener('csu-prototype-reset',()=>{memoryRead=[];update();});
})();

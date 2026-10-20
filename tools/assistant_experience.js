/* 数字人表情与语音录入演示；演示录音不会启用麦克风。 */
(() => {
  let current = null;
  let visualTimer = null;
  let activeButton = null;
  const people = () => [...document.querySelectorAll('[data-digital-human]')];
  const stop = () => {
    clearTimeout(visualTimer);
    if (window.speechSynthesis) speechSynthesis.cancel();
    people().forEach(p => {
      p.classList.remove('is-speaking');
      p.querySelector('[data-human-status]').textContent = p.dataset.mode === 'listening' ? '正在聆听 · 演示' : '在线，随时为你服务';
      p.querySelector('[data-stop-speaking]').hidden = true;
    });
    if (activeButton) { activeButton.innerHTML = activeButton.dataset.originalLabel; activeButton.removeAttribute('aria-pressed'); }
    activeButton = null; current = null;
  };
  const speak = (button) => {
    if (activeButton === button) { stop(); return; }
    stop();
    const text = button.dataset.speech === 'welcome'
      ? '你好，我是后勤小助。报修、水电缴纳、班车和校园生活服务，都可以问我。你也可以点击麦克风，用语音说出你的问题。'
      : document.querySelector('[data-answer]')?.innerText || button.dataset.speechText || '你好，我是你的后勤小助。确认识别出的文字后，再发送你的问题。';
    activeButton = button;
    button.dataset.originalLabel ||= button.innerHTML;
    button.textContent = '停止播报'; button.setAttribute('aria-pressed', 'true');
    people().forEach(p => {
      p.classList.add('is-speaking');
      p.querySelector('[data-human-status]').textContent = '正在为你讲解';
      p.querySelector('[data-stop-speaking]').hidden = false;
    });
    let audioStarted = false;
    if (window.speechSynthesis && window.SpeechSynthesisUtterance) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'zh-CN'; utterance.rate = 1;
      utterance.onstart = () => { audioStarted = true; };
      utterance.onend = () => { if (current === utterance) stop(); };
      utterance.onerror = () => {
        if (current === utterance) people().forEach(p => p.querySelector('[data-human-status]').textContent = '说话动作演示 · 当前未播放声音');
      };
      current = utterance;
      speechSynthesis.speak(utterance);
    } else {
      people().forEach(p => p.querySelector('[data-human-status]').textContent = '说话动作演示 · 当前未播放声音');
    }
    const check = () => {
      if (audioStarted && window.speechSynthesis?.speaking) { visualTimer = setTimeout(check, 1000); return; }
      stop();
    };
    visualTimer = setTimeout(check, Math.max(5500, Math.min(18000, text.length * 120)));
  };
  document.addEventListener('DOMContentLoaded', () => {
    const draftTarget = document.querySelector('.composer [name=question]');
    if (draftTarget) { try { const draft = localStorage.getItem('csu-prototype-voice-draft'); if (draft) { draftTarget.value = draft; localStorage.removeItem('csu-prototype-voice-draft'); } } catch (_) {} }
    document.querySelectorAll('[data-speak]').forEach(b => b.addEventListener('click', () => speak(b)));
    document.querySelectorAll('[data-stop-speaking]').forEach(b => b.addEventListener('click', stop));
    document.querySelectorAll('[data-voice-link]').forEach(a => a.addEventListener('click', () => {
      const value = document.querySelector('[name=question]')?.value;
      if (value) { try { localStorage.setItem('csu-prototype-voice-draft', value); } catch (_) {} }
    }));
    const record = document.querySelector('[data-voice-recording]');
    if (record) {
      let seconds = 0;
      const timer = document.querySelector('#voice-timer');
      const line = document.querySelector('#voice-live-text');
      const tick = setInterval(() => {
        seconds++;
        timer.textContent = '00:' + String(Math.min(seconds, 59)).padStart(2, '0');
        if (seconds >= 2) line.textContent = '宿舍水电费';
        if (seconds >= 4) line.textContent = '宿舍水电费怎么缴纳？';
        if (seconds >= 59) { clearInterval(tick); document.querySelector('#voice-hint').textContent = '演示录音已满，请点击“结束并识别”继续'; }
      }, 1000);
      window.addEventListener('pagehide', () => clearInterval(tick), { once: true });
    }
    document.querySelector('[data-voice-review]')?.addEventListener('submit', () => {
      try { localStorage.removeItem('csu-prototype-voice-draft'); } catch (_) {}
    });
  });
  window.addEventListener('pagehide', stop);
})();

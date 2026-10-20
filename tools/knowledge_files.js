/* 知识文件在浏览器中解析，文件内容不会提交给外部服务。 */
(() => {
  const key = "csu-prototype-knowledge-files";
  const prefix = "后勤知识文件演示：";
  let state = { files: [], batch: [], errors: [] };
  try {
    state = JSON.parse(localStorage.getItem(key)) || state;
  } catch (_) {}
  try {
    if (window.name.startsWith(prefix)) {
      const carried = JSON.parse(window.name.slice(prefix.length));
      if ((carried.changed || 0) > (state.changed || 0)) state = carried;
    }
  } catch (_) {}
  const save = () => {
    state.changed = Date.now();
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch (_) {}
    window.name = prefix + JSON.stringify(state);
  };
  const el = (tag, text, className) => {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (className) n.className = className;
    return n;
  };
  const button = (text, action, cls = "btn sm") => {
    const n = el("button", text, cls);
    n.type = "button";
    n.addEventListener("click", action);
    return n;
  };
  const size = (n) =>
    n >= 1048576
      ? (n / 1048576).toFixed(1) + " MB"
      : Math.max(1, Math.ceil(n / 1024)) + " KB";
  const route = (path, id) =>
    path + (id ? "?id=" + encodeURIComponent(id) : "");
  const batches = () => state.files.filter((f) => state.batch.includes(f.id));
  const selected = () =>
    state.files.find(
      (f) => f.id === new URLSearchParams(location.search).get("id"),
    );
  const makeChunks = (text) => {
    const result = [];
    for (let i = 0; i < text.length; i += 700) {
      result.push({
        title: "知识片段 " + (result.length + 1),
        text: text.slice(i, i + 800),
      });
      if (i + 800 >= text.length) break;
    }
    return result;
  };
  async function extract(file) {
    const ext = file.name.split(".").pop().toLowerCase();
    let text = "";
    if (ext === "docx") {
      if (!window.mammoth) throw new Error("文件解析组件未加载，请刷新后重试");
      try { text = (await mammoth.extractRawText({ arrayBuffer: await file.arrayBuffer() })).value; } catch (_) { throw new Error('Word文件无法解析，请确认文件完整有效，并使用DOCX格式'); }
    } else if (ext === "pdf") {
      if (!window.pdfjsLib) throw new Error("文件解析组件未加载，请刷新后重试");
      pdfjsLib.GlobalWorkerOptions.workerSrc =
        "../../assets/vendor/pdf.worker.min.js";
      let doc;
      try {
        doc = await pdfjsLib.getDocument({
          data: new Uint8Array(await file.arrayBuffer()),
        }).promise;
      } catch (e) {
        throw new Error(
          e.name === "PasswordException"
            ? "文件已加密，请解除密码后重新上传"
            : "文件无法读取，请确认是完整有效的PDF文件",
        );
      }
      try {
        if (doc.numPages > 100) throw new Error("文件超过100页，请拆分后上传");
        for (let i = 1; i <= doc.numPages; i++) {
          const page = await doc.getPage(i);
          const data = await page.getTextContent();
          const pageText = data.items
            .map((x) => x.str + (x.hasEOL ? "\n" : " "))
            .join("")
            .trim();
          if (pageText) text += "\n【第" + i + "页】\n" + pageText;
        }
      } finally {
        await doc.destroy();
      }
    } else {
      const raw = await file.arrayBuffer();
      try {
        text = new TextDecoder("utf-8", { fatal: true }).decode(raw);
      } catch (_) {
        text = new TextDecoder("gb18030").decode(raw);
      }
    }
    text = text
      .replace(/\r\n/g, "\n")
      .replace(/\u0000/g, "")
      .trim();
    if (text.replace(/【第\d+页】/g, "").trim().length < 2)
      throw new Error("未识别到可用正文；扫描件请先完成文字识别");
    if (text.length > 200000)
      throw new Error("正文超过20万字，请拆分文件后上传");
    return text;
  }
  function attachmentPanel() {
    const host = document.querySelector("[data-kb-attachments]");
    if (!host) return;
    const files = state.files.filter((f) => f.status === "已入库");
    if (state.knowledgeDraft)
      document
        .querySelectorAll("form[data-save=knowledge] [name]")
        .forEach((n) => {
          if (n.name in state.knowledgeDraft)
            n.value = state.knowledgeDraft[n.name];
        });
    const existing = document.querySelector("[name=sourceFile]");
    let current = existing?.value || "";
    if (!current) current = state.linkedFile || "";
    if (!current) {
      try {
        current =
          JSON.parse(localStorage.getItem("csu-prototype-knowledge") || "{}")
            .sourceFile || "";
      } catch (_) {}
    }
    const label = el("label", "关联已入库的来源文件");
    label.htmlFor = "source-file-select";
    const select = el("select");
    select.id = "source-file-select";
    select.name = "sourceFile";
    const none = el("option", "暂不关联文件");
    none.value = "";
    select.append(none);
    files.forEach((f) => {
      const o = el("option", f.name);
      o.value = f.id;
      select.append(o);
    });
    select.value = current;
    const description = el(
      "p",
      files.length
        ? "选择文件后，引用依据将关联到对应文档。"
        : "还没有已入库文件，可先上传并确认入库，再返回关联。",
      "muted",
    );
    const a = el("a", "上传来源文件 →", "textlink");
    a.href = "knowledge-upload.html?from=edit";
    a.addEventListener("click", () => {
      state.knowledgeDraft = Object.fromEntries(
        new FormData(document.querySelector("form[data-save=knowledge]")),
      );
      try {
        localStorage.setItem(
          "csu-prototype-knowledge",
          JSON.stringify(state.knowledgeDraft),
        );
      } catch (_) {}
      save();
    });
    const detail = el("a", "查看关联文件", "textlink");
    const sync = () => {
      detail.hidden = !select.value;
      detail.href = route("knowledge-file-detail.html", select.value);
    };
    select.addEventListener("change", () => {
      state.linkedFile = select.value;
      save();
      const f = state.files.find((x) => x.id === select.value);
      const source = document.querySelector("[name=source]");
      if (f && source) source.value = f.name;
      sync();
    });
    const field = el("div", undefined, "field");
    field.append(label, select, description);
    const actions = el("div", undefined, "actions");
    actions.append(a, detail);
    host.append(field, actions);
    sync();
  }
  document.addEventListener("DOMContentLoaded", () => {
    attachmentPanel();
    document.querySelectorAll("[data-kb-linked-source]").forEach((host) => {
      let id = "";
      try {
        id = JSON.parse(
          localStorage.getItem("csu-prototype-knowledge") || "{}",
        ).sourceFile;
      } catch (_) {}
      const f = state.files.find((f) => f.id === (id || state.linkedFile));
      host.textContent = f ? f.name : "未关联文件，使用手工填写的来源依据";
      if (f) {
        host.href = route("knowledge-file-detail.html", id);
        host.classList.add("textlink");
      }
    });
    const input = document.querySelector("#knowledge-file-input");
    if (input) {
      let queue = [];
      let busy = false;
      const queueHost = document.querySelector("#upload-queue");
      const start = document.querySelector("#parse-files");
      const status = document.querySelector("#upload-status");
      const progress = document.querySelector("#upload-progress");
      const render = () => {
        queueHost.replaceChildren();
        queue.forEach((file, i) => {
          const row = el("div", undefined, "upload-file-row");
          const text = el("div");
          text.append(
            el("strong", file.name),
            el("small", size(file.size) + " · 待解析"),
          );
          row.append(
            text,
            button("移除", () => {
              queue.splice(i, 1);
              render();
            }),
          );
          queueHost.append(row);
        });
        start.disabled = queue.length === 0;
        document.querySelector("#queue-count").textContent = queue.length
          ? "已选择 " + queue.length + " 个文件"
          : "暂未选择文件";
      };
      const add = (files) => {
        if (busy) return;
        const supported = ["pdf", "docx", "txt", "md"];
        const errors = [];
        for (const f of files) {
          const ext = f.name.split(".").pop().toLowerCase();
          if (!supported.includes(ext)) {
            errors.push(f.name + "：暂不支持此格式，请使用PDF、DOCX、TXT或MD");
            continue;
          }
          if (!f.size) {
            errors.push(f.name + "：文件为空");
            continue;
          }
          if (f.size > 20 * 1024 * 1024) {
            errors.push(f.name + "：超过20MB限制");
            continue;
          }
          if (queue.length >= 10) {
            errors.push("每次最多选择10个文件");
            break;
          }
          if (queue.some((x) => x.name === f.name && x.size === f.size)) {
            errors.push(f.name + "：已在待上传列表");
            continue;
          }
          queue.push(f);
        }
        status.textContent = errors.join("；");
        status.className = errors.length ? "upload-error" : "muted";
        render();
      };
      input.addEventListener("change", () => {
        add([...input.files]);
        input.value = "";
      });
      const zone = document.querySelector("#drop-zone");
      ["dragenter", "dragover"].forEach((t) =>
        zone.addEventListener(t, (e) => {
          e.preventDefault();
          zone.classList.add("dragging");
        }),
      );
      ["dragleave", "drop"].forEach((t) =>
        zone.addEventListener(t, (e) => {
          e.preventDefault();
          zone.classList.remove("dragging");
        }),
      );
      zone.addEventListener("drop", (e) => add([...e.dataTransfer.files]));
      start.addEventListener("click", async () => {
        if (
          !queue.length ||
          !document.querySelector("#file-settings").reportValidity()
        )
          return;
        progress.max = queue.length;
        busy = true;
        start.disabled = true;
        input.disabled = true;
        queueHost
          .querySelectorAll("button")
          .forEach((b) => (b.disabled = true));
        const metadata = Object.fromEntries(
          new FormData(document.querySelector("#file-settings")),
        );
        state.batch = [];
        state.errors = [];
        const records = [];
        for (let i = 0; i < queue.length; i++) {
          const f = queue[i];
          status.className = "muted";
          status.textContent =
            "正在解析 " + (i + 1) + "/" + queue.length + "：" + f.name;
          progress.hidden = false;
          progress.value = i;
          try {
            const text = await extract(f);
            const signature = f.name + ":" + f.size + ":" + f.lastModified;
            if (state.files.some((x) => x.signature === signature))
              throw new Error("该文件已在知识文件列表，请勿重复入库");
            const record = {
              id: "file-" + Date.now() + "-" + i,
              name: f.name,
              size: f.size,
              signature,
              text,
              chunks: makeChunks(text),
              category: metadata.category,
              visibility: metadata.visibility,
              owner: metadata.owner.trim(),
              sourceDate: metadata.sourceDate,
              status: "待确认",
              uploaded: new Date().toLocaleString("zh-CN"),
              note: "",
            };
            records.push(record);
            state.batch.push(record.id);
          } catch (e) {
            state.errors.push({
              name: f.name,
              reason: e.message || "文件解析失败，请检查文件后重试",
            });
          }
          progress.value = i + 1;
        }
        state.files.push(...records);
        save();
        location.href = state.batch.length
          ? "knowledge-upload-preview.html"
          : "knowledge-upload-error.html";
      });
      document.querySelector("#file-settings").addEventListener("input", () => {
        start.disabled =
          queue.length === 0 ||
          !document.querySelector("#file-settings").checkValidity();
      });
      render();
    }
    const preview = document.querySelector("#parsed-files");
    if (preview) {
      const files = batches();
      preview.replaceChildren();
      document.querySelector("#parsed-count").textContent =
        files.length + " 个文件解析完成";
      files.forEach((f) => {
        const section = el("section", undefined, "card");
        section.append(el("h2", f.name));
        const meta = el(
          "p",
          size(f.size) +
            " · " +
            f.text.length.toLocaleString() +
            " 字 · " +
            f.chunks.length +
            " 个片段 · " +
            f.visibility,
          "muted",
        );
        section.append(meta);
        const snippet = el(
          "textarea",
          f.text.slice(0, 2400),
          "file-text-preview",
        );
        snippet.readOnly = true;
        snippet.setAttribute("aria-label", f.name + "解析正文预览");
        section.append(snippet);
        const a = el("a", "查看全文与知识片段 →", "textlink");
        a.href = route("knowledge-file-detail.html", f.id);
        section.append(a);
        preview.append(section);
      });
      const errors = document.querySelector("#partial-errors");
      if (state.errors.length) {
        errors.hidden = false;
        errors.append(
          el(
            "strong",
            "有 " + state.errors.length + " 个文件未能解析，本次不会入库",
          ),
        );
        state.errors.forEach((e) =>
          errors.append(el("p", e.name + "：" + e.reason)),
        );
      }
      document
        .querySelector("#confirm-files")
        .addEventListener("submit", (e) => {
          e.preventDefault();
          if (!files.length) return;
          files.forEach((f) => (f.status = "已入库"));
          save();
          location.href = "knowledge-upload-success.html";
        });
      document.querySelector("#confirm-files button").disabled =
        files.length === 0;
    }
    const list = document.querySelector("#knowledge-file-list");
    if (list) {
      const render = () => {
        list.replaceChildren();
        const q = (document.querySelector("#file-search")?.value || "").trim();
        const files = state.files.filter((f) =>
          (f.name + f.category + f.status + f.owner).includes(q),
        );
        document.querySelector("#file-total").textContent =
          state.files.length + " 个文件";
        files.forEach((f) => {
          const row = el("tr");
          const title = el("td");
          title.append(
            el("strong", f.name),
            el("p", size(f.size) + " · " + f.chunks.length + "个片段"),
          );
          const status = el("td");
          status.append(
            el(
              "span",
              f.status,
              "badge " + (f.status === "已入库" ? "green" : "amber"),
            ),
          );
          const action = el("td");
          const a = el("a", "查看文件", "textlink");
          a.href = route("knowledge-file-detail.html", f.id);
          action.append(a);
          row.append(
            title,
            el("td", f.category),
            status,
            el("td", f.visibility),
            el("td", f.uploaded),
            action,
          );
          list.append(row);
        });
        document.querySelector("#files-empty").hidden = files.length > 0;
      };
      document.querySelector("#file-search").addEventListener("input", render);
      render();
    }
    const detail = document.querySelector("#knowledge-file-detail");
    if (detail) {
      const f = selected();
      if (!f) {
        detail.replaceChildren(
          el("h2", "尚未选择来源文件"),
          el("p", "请先上传文件，或从文件列表选择一份来源文档。"),
        );
        return;
      }
      document.querySelector("#file-name").textContent = f.name;
      document.querySelector("#file-body").textContent = f.text;
      document.querySelector("#file-metadata").textContent =
        f.category +
        " · " +
        f.visibility +
        " · " +
        f.status +
        " · " +
        size(f.size);
      document.querySelector("#file-origin").textContent =
        "维护人：" +
        f.owner +
        "　资料日期：" +
        (f.sourceDate || "未填写") +
        "　上传时间：" +
        f.uploaded;
      const chunks = document.querySelector("#file-chunks");
      f.chunks.forEach((c) => {
        const d = el("details", undefined, "file-chunk");
        d.append(el("summary", c.title), el("p", c.text));
        chunks.append(d);
      });
    }
    document.querySelectorAll("[data-kb-success]").forEach((n) => {
      n.textContent = batches().length + " 个文件已确认入库";
    });
    const error = document.querySelector("#failed-files");
    if (error) {
      if (!state.errors.length)
        error.append(el("p", "尚无失败记录，请返回上传文件。"));
      state.errors.forEach((f) => {
        const row = el("div", undefined, "list-row");
        const text = el("div");
        text.append(el("h3", f.name), el("p", f.reason));
        row.append(text);
        error.append(row);
      });
    }
  });
})();

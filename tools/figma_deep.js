/* 内页只重排展示节点；权限、保存、阅读状态与跳转沿用业务脚本。 */
function figmaDeepScreens() {
  const knowledgeConfirm = document.querySelector(
    'form[action="knowledge-published.html"]',
  );
  if (knowledgeConfirm && !knowledgeConfirm.dataset.deepReady) {
    knowledgeConfirm.dataset.deepReady = "true";
    const choice = knowledgeConfirm.querySelector('input[type="checkbox"]');
    const button = knowledgeConfirm.querySelector("button");
    if (choice && button) {
      const sync = () => {
        button.disabled = !choice.checked;
      };
      choice.addEventListener("change", sync);
      sync();
    }
  }
  const offlineForm = document.querySelector('form[data-save="offline"]');
  if (offlineForm && !offlineForm.dataset.deepReady) {
    offlineForm.dataset.deepReady = "true";
    const reason = offlineForm.querySelector("textarea");
    const button = offlineForm.querySelector("button");
    if (reason && button) {
      const sync = () => {
        button.disabled = !reason.value.trim();
      };
      reason.addEventListener("input", sync);
      sync();
    }
  }
  document.querySelectorAll(".service-preview-phone").forEach((preview) => {
    preview.classList.add("mobile", "deep-preview");
  });
  const mobile = document.querySelector(".mobile");
  if (!mobile) return;
  const role = document.body.dataset.role;
  const page = document.body.dataset.page;
  const brand = mobile.querySelector(".figma-mobile-brand strong");
  mobile.querySelectorAll('[data-screen^="chat"] .answer').forEach((answer) => {
    if (answer.querySelector(".deep-chat-avatar")) return;
    const avatar = document.createElement("span");
    avatar.className = "deep-chat-avatar";
    avatar.setAttribute("aria-hidden", "true");
    answer.prepend(avatar);
  });
  const catalog = mobile.querySelector("[data-service-catalog]");
  if (
    catalog &&
    role === "staff" &&
    !catalog.querySelector(".deep-campus-hero")
  ) {
    const template = document.querySelector("#deep-hall-hero");
    if (template)
      catalog
        .querySelector(".filters")
        ?.after(template.content.cloneNode(true));
  }
  mobile.querySelectorAll(".detail-banner").forEach((banner) => {
    const root = banner.closest(".service-config-guide");
    if (!root || root.classList.contains("deep-service-guide")) return;
    root.classList.add("deep-service-guide");
    const description = root.querySelector(".service-content-body");
    const steps = root.querySelector(".steps");
    const information = [...root.querySelectorAll(".card")].find((card) =>
      card.querySelector(".summary-list"),
    );
    const notice = root.querySelector(".note");
    const action = information?.querySelector(".actions");
    const oldBody = banner.closest(".card");
    const hero = document.createElement("div");
    hero.className = "deep-service-hero";
    const school = document.createElement("div");
    school.className = "deep-service-school";
    school.textContent = "中南大学 · 智慧后勤";
    banner.querySelector("h1")?.before(school);
    hero.append(banner);
    const overview = document.createElement("section");
    overview.className = "deep-service-overview";
    const overviewTitle = document.createElement("h2");
    overviewTitle.className = "deep-underlined";
    overviewTitle.textContent = "服务说明";
    overview.append(overviewTitle);
    if (description) overview.append(description);
    const timeline = document.createElement("section");
    timeline.className = "deep-service-timeline";
    const timelineTitle = document.createElement("h2");
    timelineTitle.className = "deep-underlined";
    timelineTitle.textContent = "办理步骤";
    timeline.append(timelineTitle);
    if (steps) {
      steps.querySelectorAll(".service-content-step").forEach((step, index) => {
        const code = document.createElement("small");
        code.className = "deep-step-code";
        code.textContent = "步骤 " + String(index + 1).padStart(2, "0");
        step.querySelector("h3")?.before(code);
      });
      timeline.append(steps);
    }
    const layout = document.createElement("div");
    layout.className = "deep-service-sections";
    layout.append(hero);
    if (notice) layout.append(notice);
    layout.append(overview, timeline);
    if (information) {
      information.className = "deep-service-information";
      information.querySelector("h2")?.classList.add("deep-underlined");
      if (action) {
        action.classList.add("deep-service-action");
        action.removeAttribute("style");
      }
      layout.append(information);
      if (action) layout.append(action);
    }
    root.querySelector(".page-heading")?.classList.add("deep-guide-context");
    oldBody?.remove();
    root.querySelector(".split-detail")?.remove();
    root.append(layout);
    if (brand)
      brand.textContent =
        banner.querySelector("h1")?.textContent || brand.textContent;
  });
  if (page === "meetings") {
    mobile.querySelectorAll(".deep-meetings .list-row").forEach((row) => {
      if (row.classList.contains("deep-meeting-card")) return;
      row.classList.add("deep-meeting-card");
      const target = row.matches("a") ? row : row.querySelector("a[href]");
      if (!row.matches("a") && target) {
        if (target.textContent.includes("最新安排")) {
          const latest = document.createElement("span");
          latest.className = "badge deep-latest-arrangement";
          latest.textContent = "最新安排";
          row.querySelector(".badge")?.after(latest);
        }
        target.className = "deep-meeting-open";
        target.setAttribute(
          "aria-label",
          "查看" + (row.querySelector("h2,h3")?.textContent || "会议"),
        );
      }
      if (row.matches("a")) {
        const description = row.querySelector("p");
        const status = description?.textContent.includes("已结束")
          ? "已结束"
          : description?.textContent.includes("已取消")
            ? "已取消"
            : "";
        if (status) {
          const badge = document.createElement("span");
          badge.className =
            "badge " + (status === "已取消" ? "deep-cancelled" : "gray");
          badge.textContent = status;
          row.querySelector("h3")?.before(badge);
          description.textContent = description.textContent.replace(
            " · " + status,
            "",
          );
        }
      }
    });
  }
}
document.addEventListener("DOMContentLoaded", figmaDeepScreens);
window.addEventListener("pageshow", figmaDeepScreens);
window.addEventListener("storage", figmaDeepScreens);
window.addEventListener("csu-prototype-reset", figmaDeepScreens);

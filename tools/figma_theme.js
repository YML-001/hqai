/* 管理菜单的筛选只影响展示，不改变菜单地址和权限。 */
function figmaServiceSearch() {
  const catalog = document.querySelector("[data-service-catalog]");
  const query = catalog?.querySelector("input");
  if (query && !catalog.querySelector(".figma-service-search")) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "figma-service-search";
    button.textContent = "搜索";
    button.addEventListener("click", () => {
      query.dispatchEvent(new Event("input", { bubbles: true }));
      query.focus();
    });
    query.parentElement.append(button);
  }
}
window.addEventListener("pageshow", figmaServiceSearch);
window.addEventListener("storage", figmaServiceSearch);
window.addEventListener("csu-prototype-reset", figmaServiceSearch);
document.addEventListener("DOMContentLoaded", () => {
  figmaServiceSearch();
  const search = document.querySelector("[data-figma-menu-search]");
  if (!search) return;
  const menus = [...document.querySelectorAll(".sidebar .nav-item")];
  const empty = document.createElement("p");
  empty.className = "figma-menu-empty";
  empty.textContent = "没有找到相关菜单";
  empty.hidden = true;
  search.closest("label").after(empty);
  search.addEventListener("input", () => {
    const keyword = search.value.trim();
    menus.forEach((menu) => {
      menu.hidden = !menu.textContent.includes(keyword);
    });
    empty.hidden = menus.some((menu) => !menu.hidden);
  });
});

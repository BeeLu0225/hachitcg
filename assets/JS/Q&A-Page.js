// 導入 Bootstrap 的 JavaScript
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// 導入這個頁面專屬的 SCSS 檔案
import "../scss/_custom.scss";

const siteApp = document.querySelector('[data-app="site"]');

if (siteApp) {
  console.log("這段程式只在 site 區域執行");

  const btn = siteApp.querySelector(".btn");
  btn.addEventListener("click", () => {
    alert("這是 site 區域的按鈕！");
  });
}

// 購物車庫存-數量控制器元件
document.addEventListener("DOMContentLoaded", () => {
  const boxes = document.querySelectorAll(".quantity-box");
  // 如果頁面上沒有這個元件，就直接返回，不執行
  if (!boxes.length) return;

  boxes.forEach((box) => {
    const minusBtn = box.querySelector(".btn-minus");
    const plusBtn = box.querySelector(".btn-plus");
    const valueDisplay = box.querySelector(".quantity-value");

    let quantity = parseInt(valueDisplay.textContent);

    minusBtn.addEventListener("click", () => {
      if (quantity > 1) quantity--;
      valueDisplay.textContent = quantity;
    });

    plusBtn.addEventListener("click", () => {
      quantity++;
      valueDisplay.textContent = quantity;
    });
  });
});

// 愛心收藏按鈕功能
document.addEventListener("DOMContentLoaded", () => {
  // 尋找頁面上「所有」的收藏按鈕
  const favBtns = document.querySelectorAll(".btn-fav");

  // 如果這個頁面沒有收藏按鈕，就直接結束，不執行
  if (!favBtns.length) return;

  // 為每一個按鈕加上點擊事件
  favBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const icon = btn.querySelector("i");

      // 切換按鈕的 .active 狀態
      btn.classList.toggle("active");

      // 根據 .active 狀態來切換愛心圖示
      if (btn.classList.contains("active")) {
        // 變成實心
        icon.classList.replace("bi-heart", "bi-heart-fill");
      } else {
        // 變回空心
        icon.classList.replace("bi-heart-fill", "bi-heart");
      }
    });
  });
});

console.log("✅ JS 已載入成功！");
// input
document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("quantityBox");
  if (!box) return;

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
// input end

// 愛心通用icon
// 🟡 改為 querySelectorAll 支援多個收藏按鈕
const favBtns = document.querySelectorAll(".btn-fav");

favBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const icon = btn.querySelector("i");
    btn.classList.toggle("active");
    if (btn.classList.contains("active")) {
      icon.classList.replace("bi-heart", "bi-heart-fill");
    } else {
      icon.classList.replace("bi-heart-fill", "bi-heart");
    }
  });
});

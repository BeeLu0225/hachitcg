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

// 愛心icon

const favBtn = document.getElementById("favBtn");

favBtn.addEventListener("click", () => {
  const icon = favBtn.querySelector("i");
  favBtn.classList.toggle("active");
  if (favBtn.classList.contains("active")) {
    icon.classList.replace("bi-heart", "bi-heart-fill"); // 變實心
  } else {
    icon.classList.replace("bi-heart-fill", "bi-heart"); // 變空心
  }
});
// 愛心icon end

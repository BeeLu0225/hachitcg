console.log("✅ JS 已載入成功！");

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

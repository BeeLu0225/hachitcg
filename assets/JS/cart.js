let cartItems = document.querySelectorAll(".cart-items"); 
const totalPrice = document.querySelector(".total-price");
const allSelectedBtn = document.querySelector(".all-selected");
console.log(cartItems);
refreshAllSelectBtn();
refreshAllPrice();

// 監聽 start
document.addEventListener("DOMContentLoaded", () => {
    allSelectedBtn.addEventListener("click", () => {
        let isAllSelected = true;
        cartItems.forEach((item) => {
            const selectBtn = item.querySelector(".form-check-input");
            let isSelected = selectBtn.checked;
            if(!isSelected){
                selectBtn.checked = true;
                isAllSelected = false;
            };            
        })
        if(isAllSelected){
            cartItems.forEach((item) => {
                const selectBtn = item.querySelector(".form-check-input");
                selectBtn.checked = false;
            });         
        };
        refreshAllPrice()
    });

    cartItems.forEach((item,index) => {
        const selectBtn = item.querySelector(".form-check-input");
        const minusBtn = item.querySelector(".btn-minus");
        const plusBtn = item.querySelector(".btn-plus");
        const deleteBtn = item.querySelector(".btn-delete");
        const valueDisplay = item.querySelector(".quantity-value");

        let quantity = parseInt(valueDisplay.textContent);
        // console.log(selectBtn.checked);

        selectBtn.addEventListener("click", () => {
            refreshAllSelectBtn();
            refreshAllPrice();
        });

        minusBtn.addEventListener("click", () => {
            if (quantity > 1) quantity--;
            valueDisplay.textContent = quantity;
            refreshAllPrice()
        });

        plusBtn.addEventListener("click", () => {
            quantity++;
            valueDisplay.textContent = quantity;
            refreshAllPrice()
        });

        deleteBtn.addEventListener("click", () => {
            item.parentNode.removeChild(item);
            cartItems = document.querySelectorAll(".cart-items");
            refreshAllSelectBtn();
            refreshAllPrice();
            refreshCartList();
        });
    })
});
// 監聽 end

// 刷新所有價格
function refreshAllPrice(){ 
    let totalPriceCal = 0;
    cartItems.forEach((item) => {        
        const selectBtn = item.querySelector(".form-check-input");
        const priceSingle = parseInt(item.querySelector(".price-single").textContent);
        const priceSum = item.querySelector(".price-sum");
        const quantity = parseInt(item.querySelector(".quantity-value").textContent);
        priceSum.textContent = priceSingle * quantity;

        let isSelected = selectBtn.checked
        if (isSelected){
            totalPriceCal += parseInt(priceSum.textContent);
        }
    });
    totalPrice.textContent = totalPriceCal
}

// 刷新按鈕
function refreshAllSelectBtn(){ 
    let isAllSelected = true;
    cartItems.forEach((item) => {        
        const selectBtn = item.querySelector(".form-check-input");
        if (!selectBtn.checked){
            isAllSelected = false;
        }
    });

    if (isAllSelected){
        allSelectedBtn.checked = true;
    } else{
        allSelectedBtn.checked = false;
    }
}

// 購物車是否為空
function refreshCartList(){
    if(!cartItems.length){
        const hasProduct = document.querySelectorAll(".has-product");
        const noneProduct = document.querySelectorAll(".none-product");
        hasProduct.forEach((element) => {
            let selfClass = element.getAttribute("class");
            console.log(selfClass);
            selfClass += " d-none"
            element.setAttribute("class",selfClass);
        })
        noneProduct.forEach((element) => {
            let selfClass = element.getAttribute("class").replace(/d-none/g, "");
            console.log(selfClass);
            element.setAttribute("class",selfClass);
        })
    }
}
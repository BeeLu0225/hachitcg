// /assets/JS/team-carousel.js
const teamMembers = [
  { name: "寶可夢",       role: "Pokémon 集換式卡牌遊戲" },
  { name: "Vanguard", role: "卡片戰鬥先導者 TCG" },
  { name: "遊戲王",  role: "Yu-Gi-Oh! 決鬥卡牌" },
  { name: "海賊王",    role: "ONE PIECE 卡牌遊戲" },
  { name: "Weiβ Schwarz",   role: "日系跨作品對戰卡牌" },
];

const cards = [...document.querySelectorAll(".bc-card")];
const dots = [...document.querySelectorAll(".bc-dot")];
const memberName = document.querySelector(".bc-member-name");
const memberRole = document.querySelector(".bc-member-role");
const leftArrow = document.querySelector(".bc-nav-arrow.left");
const rightArrow = document.querySelector(".bc-nav-arrow.right");

// 若該頁沒有這組 DOM，直接跳出避免報錯
if (cards.length && dots.length && memberName && memberRole && leftArrow && rightArrow) {
  const fallbackFromDom = (i, key) => {
    const el = cards[i];
    if (!el) return "";
    if (key === "name") return el.dataset.name || el.querySelector("img")?.alt || "";
    if (key === "role") return el.dataset.role || "";
    return "";
  };
  const getName = (i) => (teamMembers[i]?.name ?? fallbackFromDom(i, "name"));
  const getRole = (i) => (teamMembers[i]?.role ?? fallbackFromDom(i, "role"));

  let currentIndex = 0;
  let isAnimating = false;

  const CLASS_SET = ["center","left-1","left-2","right-1","right-2","hidden"];
  const clearClasses = (el) => el.classList.remove(...CLASS_SET);

  function updateDots() {
    dots.forEach((d, i) => {
      const active = i === currentIndex;
      d.classList.toggle("active", active);
      d.setAttribute("aria-selected", active ? "true" : "false");
    });
  }

  function placeCards() {
    const n = cards.length;
    cards.forEach((card, i) => {
      clearClasses(card);
      const offset = (i - currentIndex + n) % n;
      if (offset === 0) card.classList.add("center");
      else if (offset === 1) card.classList.add("right-1");
      else if (offset === 2) card.classList.add("right-2");
      else if (offset === n - 1) card.classList.add("left-1");
      else if (offset === n - 2) card.classList.add("left-2");
      else card.classList.add("hidden");
    });
  }

  function updateInfo() {
    memberName.style.opacity = "0";
    memberRole.style.opacity = "0";
    setTimeout(() => {
      memberName.textContent = getName(currentIndex);
      memberRole.textContent = getRole(currentIndex);
      memberName.style.opacity = "1";
      memberRole.style.opacity = "1";
    }, 150);
  }

  function waitTransitionEnd() {
    return new Promise((resolve) => {
      const center = cards[currentIndex];
      let done = false;
      const onEnd = (e) => {
        if (done) return;
        if (e.propertyName && !/transform|opacity/.test(e.propertyName)) return;
        done = true;
        resolve();
      };
      center.addEventListener("transitionend", onEnd, { once: true });
      setTimeout(() => { if (!done) resolve(); }, 600);
    });
  }

  async function updateCarousel(newIndex) {
    if (isAnimating) return;
    isAnimating = true;
    const n = cards.length;
    currentIndex = ((newIndex % n) + n) % n;
    placeCards();
    updateDots();
    updateInfo();
    await waitTransitionEnd();
    isAnimating = false;
  }

  leftArrow.addEventListener("click", () => updateCarousel(currentIndex - 1));
  rightArrow.addEventListener("click", () => updateCarousel(currentIndex + 1));
  dots.forEach((dot, i) => dot.addEventListener("click", () => updateCarousel(i)));
  cards.forEach((card, i) => card.addEventListener("click", () => updateCarousel(i)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") updateCarousel(currentIndex - 1);
    if (e.key === "ArrowRight") updateCarousel(currentIndex + 1);
  });

  let touchStartX = 0;
  document.addEventListener("touchstart", (e) => (touchStartX = e.changedTouches[0].screenX), { passive: true });
  document.addEventListener("touchend", (e) => {
    const diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > 50) updateCarousel(currentIndex + (diff > 0 ? 1 : -1));
  }, { passive: true });

  updateCarousel(0);
}
 
 // 計算 header 高度，讓背景從 header 下方開始
  function setHeaderOffset() {
    const header = document.querySelector('header');
    const h = header ? header.offsetHeight : 0;
    document.documentElement.style.setProperty('--header-h', h + 'px');
  }
  window.addEventListener('load', setHeaderOffset);
  window.addEventListener('resize', setHeaderOffset);
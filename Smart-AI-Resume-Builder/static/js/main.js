/* ResumeLens AI — main.js */

// ── Flash auto-dismiss ───────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((f, i) => {
    setTimeout(() => f.remove(), 5000 + i * 300);
  });
});

// ── User dropdown ────────────────────────────────────────────────────────────
function toggleUserMenu() {
  const dd = document.getElementById("userDropdown");
  const ch = document.getElementById("userChevron");
  if (!dd) return;
  const open = dd.classList.toggle("open");
  if (ch) ch.style.transform = open ? "rotate(180deg)" : "";
}

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  const chip = document.querySelector(".nav-user-chip");
  const dd   = document.getElementById("userDropdown");
  if (chip && dd && !chip.contains(e.target)) {
    dd.classList.remove("open");
    const ch = document.getElementById("userChevron");
    if (ch) ch.style.transform = "";
  }
});

// ── Mobile nav toggle ────────────────────────────────────────────────────────
function toggleMobileNav() {
  const sidebar  = document.getElementById("sidebar");
  const overlay  = document.getElementById("sidebarOverlay");
  const burger   = document.getElementById("navBurger");
  if (!sidebar) return;
  const open = sidebar.classList.toggle("open");
  if (overlay) overlay.classList.toggle("active", open);
  if (burger) burger.innerHTML = open
    ? '<i class="fas fa-times"></i>'
    : '<i class="fas fa-bars"></i>';
}

function closeSidebar() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");
  const burger  = document.getElementById("navBurger");
  if (sidebar) sidebar.classList.remove("open");
  if (overlay) overlay.classList.remove("active");
  if (burger) burger.innerHTML = '<i class="fas fa-bars"></i>';
}

// ── Score bar animation ──────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const bars = document.querySelectorAll(".bar-fill, .sp-fill, .kw-fill, .mini-fill");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.transition = "width 0.8s cubic-bezier(.4,0,.2,1)";
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  bars.forEach(b => {
    const target = b.style.width;
    b.style.width = "0";
    observer.observe(b);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { b.style.width = target; });
    });
  });
});

// ── Navbar scroll shadow ─────────────────────────────────────────────────────
window.addEventListener("scroll", () => {
  const nav = document.getElementById("navbar");
  if (nav) nav.classList.toggle("scrolled", window.scrollY > 10);
}, { passive: true });

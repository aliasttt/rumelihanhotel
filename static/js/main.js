const navToggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");
const header = document.querySelector("[data-header]");

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    nav.classList.toggle("open");
    navToggle.classList.toggle("open");
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

document.querySelectorAll(".reveal, .reveal-left, .reveal-right").forEach((item) => revealObserver.observe(item));

document.querySelectorAll(".video-play").forEach((button) => {
  button.addEventListener("click", () => {
    const wrapper = button.closest(".video-card, .video-band");
    const video = wrapper?.querySelector("video");
    if (!wrapper || !video) return;

    document.querySelectorAll(".video-card.playing video, .video-band.playing video").forEach((item) => {
      if (item !== video) {
        item.pause();
        item.closest(".video-card, .video-band")?.classList.remove("playing");
      }
    });

    video.controls = true;
    video.muted = false;
    video.play().then(() => wrapper.classList.add("playing")).catch(() => {
      video.muted = true;
      video.play().then(() => wrapper.classList.add("playing")).catch(() => {});
    });
  });
});

window.addEventListener("scroll", () => {
  if (header) header.classList.toggle("scrolled", window.scrollY > 18);
  updateScrollEffects();
});

window.addEventListener("resize", updateScrollEffects);

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function updateScrollEffects() {
  const viewport = window.innerHeight || 1;

  document.querySelectorAll("[data-parallax-section]").forEach((section) => {
    const rect = section.getBoundingClientRect();
    const progress = clamp((viewport - rect.top) / (viewport + rect.height), 0, 1);
    section.querySelectorAll("[data-parallax-speed]").forEach((layer) => {
      if (window.innerWidth <= 560 && layer.classList.contains("hero-ornament")) {
        layer.style.transform = "";
        return;
      }
      const speed = Number(layer.dataset.parallaxSpeed || 0);
      layer.style.transform = `translate3d(0, ${(progress - 0.5) * speed * 220}px, 0)`;
    });
  });

  document.querySelectorAll("[data-showcase]").forEach((section) => {
    const rect = section.getBoundingClientRect();
    const progress = clamp((viewport - rect.top) / (viewport + rect.height), 0, 1);
    const frame = section.querySelector(".showcase-frame");
    const text = section.querySelector("[data-scroll-text]");
    if (frame) {
      frame.style.setProperty("--showcase-y", `${(0.5 - progress) * 34}px`);
      frame.style.setProperty("--showcase-scale", `${0.94 + progress * 0.08}`);
    }
    if (text) {
      text.style.opacity = `${clamp(progress * 1.4, 0.18, 1)}`;
      text.style.transform = `translateY(${(1 - progress) * 18}px)`;
    }
  });

  document.querySelectorAll("[data-horizontal-scroll]").forEach((section) => {
    const rect = section.getBoundingClientRect();
    const track = section.querySelector(".scroll-track");
    if (!track) return;
    const overflow = Math.max(track.scrollWidth - window.innerWidth, 0);
    const progress = clamp((viewport - rect.top) / (viewport + rect.height), 0, 1);
    track.style.setProperty("--scroll-x", `${-overflow * progress}px`);
  });
}

updateScrollEffects();

const navToggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");
const header = document.querySelector("[data-header]");

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    nav.classList.toggle("open");
    navToggle.classList.toggle("open");
  });
}

const campaignPopup = document.querySelector("[data-campaign-popup]");
if (campaignPopup) {
  const storageKey = "rumelihan-campaign-dismissed";
  if (sessionStorage.getItem(storageKey) === "1") {
    campaignPopup.hidden = true;
  }
  campaignPopup.querySelectorAll("[data-campaign-close]").forEach((button) => {
    button.addEventListener("click", () => {
      campaignPopup.hidden = true;
      sessionStorage.setItem(storageKey, "1");
    });
  });
  campaignPopup.querySelectorAll("[data-campaign-action]").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      sessionStorage.setItem(storageKey, "1");
      window.location.assign(link.href);
    });
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

document.querySelectorAll("[data-video-carousel]").forEach((carousel) => {
  const slides = Array.from(carousel.querySelectorAll("[data-video-slide]"));
  const dots = Array.from(carousel.querySelectorAll("[data-video-dot]"));
  const prev = carousel.querySelector("[data-video-prev]");
  const next = carousel.querySelector("[data-video-next]");
  let activeIndex = 0;

  function showSlide(index) {
    if (!slides.length) return;
    activeIndex = (index + slides.length) % slides.length;

    slides.forEach((slide, slideIndex) => {
      const video = slide.querySelector("video");
      const isActive = slideIndex === activeIndex;
      slide.classList.toggle("active", isActive);
      if (!video) return;
      if (isActive) {
        video.currentTime = 0;
        video.muted = true;
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });

    dots.forEach((dot, dotIndex) => dot.classList.toggle("active", dotIndex === activeIndex));
  }

  slides.forEach((slide, index) => {
    const video = slide.querySelector("video");
    if (video) video.addEventListener("ended", () => showSlide(index + 1));
  });

  prev?.addEventListener("click", () => showSlide(activeIndex - 1));
  next?.addEventListener("click", () => showSlide(activeIndex + 1));
  dots.forEach((dot, index) => dot.addEventListener("click", () => showSlide(index)));

  const carouselObserver = new IntersectionObserver(
    ([entry]) => {
      const video = slides[activeIndex]?.querySelector("video");
      if (!video) return;
      if (entry.isIntersecting) video.play().catch(() => {});
      else video.pause();
    },
    { threshold: 0.45 }
  );

  carouselObserver.observe(carousel);
  showSlide(0);
});

document.querySelectorAll("[data-drag-scroll]").forEach((track) => {
  let isDown = false;
  let startX = 0;
  let scrollLeft = 0;
  let userScrollTimeout = null;

  track.dataset.autoScroll = "1";

  track.addEventListener("pointerdown", (event) => {
    isDown = true;
    startX = event.clientX;
    scrollLeft = track.scrollLeft;
    track.dataset.userDragging = "1";
    track.classList.add("dragging");
    track.setPointerCapture(event.pointerId);
  });

  track.addEventListener("pointermove", (event) => {
    if (!isDown) return;
    event.preventDefault();
    track.scrollLeft = scrollLeft - (event.clientX - startX);
  });

  ["pointerup", "pointercancel", "pointerleave"].forEach((eventName) => {
    track.addEventListener(eventName, () => {
      isDown = false;
      track.classList.remove("dragging");
      window.clearTimeout(userScrollTimeout);
      userScrollTimeout = window.setTimeout(() => {
        track.dataset.userDragging = "0";
      }, 900);
    });
  });

  track.addEventListener("wheel", () => {
    track.dataset.userDragging = "1";
    window.clearTimeout(userScrollTimeout);
    userScrollTimeout = window.setTimeout(() => {
      track.dataset.userDragging = "0";
    }, 900);
  }, { passive: true });
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

  document.querySelectorAll(".scroll-gallery").forEach((section) => {
    const track = section.querySelector("[data-drag-scroll]");
    if (!track || track.dataset.userDragging === "1") return;
    const rect = section.getBoundingClientRect();
    const progress = clamp((viewport - rect.top) / (viewport + rect.height), 0, 1);
    const overflow = Math.max(track.scrollWidth - track.clientWidth, 0);
    track.scrollLeft = overflow * progress;
  });

}

updateScrollEffects();

// Slider's Code

var swiper = new Swiper(".slide-content", {
  slidesPerView: 7,
  spaceBetween: 20,
  slidesPerGroup: 1,
  centerSlide: "true",
  grabCursor: "true",
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    0: {
      slidesPerView: 2,
    },
    468: {
      slidesPerView: 3,
    },
    768: {
      slidesPerView: 4,
    },
    950: {
      slidesPerView: 5,
    },
    1024: {
      slidesPerView: 7,
    },
  },
});

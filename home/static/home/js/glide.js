const Config = {
    type: 'carousel',
    startAt: 0,
    perView: 3,
    focusAt: 0,
    autoplay: 8000,
    hoverpause: true,
    breakpoints: {
    1700: {
        perView: 2
        },
      1200: {
        perView: 1
      }
    },
  };
  new Glide('.glide', Config).mount();

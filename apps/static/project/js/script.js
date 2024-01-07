window.addEventListener("DOMContentLoaded" , () => {
  const loader = document.querySelector(".loader-page");
  setTimeout(function () {
    setTimeout(function () {
      loader.style.display = "none";
    }, 1500);
  }, 2000);
})


window.addEventListener('scroll', () => {
  let navbar = document.querySelector('.nav');
  navbar.classList.toggle('navbar-fixed-bg', window.scrollY > 5);
})



const counters = document.querySelectorAll('.value');
const speed = 200;
const statistics = document.querySelector('.statistics')
const windowHeight = window.innerHeight / 2
window.addEventListener('scroll', () => {
  if ((statistics.offsetTop - windowHeight) < window.pageYOffset) {
    counters.forEach(counter => {
      const animate = () => {
        const value = +counter.getAttribute('akhi');
        const data = +counter.innerText;

        const time = value / speed;
        if (data < value) {
          counter.innerText = Math.ceil(data + time);
          setTimeout(animate, 4);
        } else {
          counter.innerText = value;
        }
      }
      animate();
    });
  }
})

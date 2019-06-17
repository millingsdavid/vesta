$('.menu').on('click', function() {
    $(this).toggleClass('active');
    $('.overlay').toggleClass('menu-open');
});

$('.nav a').on('click', function (){
    $('.menu').removeClass('active');
    $('.overlay').removeClass('menu-open')
});
const items = document.querySelectorAll(".accordion a");

function toggleAccordion(){
  this.classList.toggle('active');
  this.nextElementSibling.classList.toggle('active');
}

items.forEach(item => item.addEventListener('click', toggleAccordion));
// elements from html
const hamMenu       = document.querySelector(".nav_menu");
const offScreenMenu = document.querySelector(".off_screen_menu");
const header        = document.querySelector(".header_container");
const extra         = document.querySelector("#extra");
const checkButton   = document.querySelector("#id_reclamante_menor_edad");
const parentForm    = document.querySelector(".form_cotainer_parent");

// click event : menu
hamMenu.addEventListener("click", () => {
  hamMenu.classList.toggle("active");
  offScreenMenu.classList.toggle("active");
});


// window event
window.addEventListener("scroll", ()=>{
  if (window.scrollY > 300) {
    header.classList.add("active");
    extra.classList.add("active");
  } else {
    header.classList.remove("active");
    extra.classList.remove("active");
  }
});

// checkbox event : main
checkButton.addEventListener("click", ()=>{

    parentForm.classList.toggle("active");

})
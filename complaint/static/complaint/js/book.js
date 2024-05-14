// elements from html
const nav_menu        = document.querySelector(".nav_menu");
const off_screen_menu = document.querySelector(".off_screen_menu");
const nav_container   = document.querySelector(".nav_container");
const extra           = document.querySelector("#extra")
const checkButton     = document.querySelector("#id_reclamante_menor_edad");
const parentForm      = document.querySelector(".form_cotainer_parent");

// window event
window.addEventListener("scroll", ()=>{
  if (window.scrollY > 300) {
    nav_container.classList.add("active");
    extra.classList.add("active");
  } else {
    nav_container.classList.remove("active");
    extra.classList.remove("active");
  }
});

// click event : menu
nav_menu.addEventListener("click", () => {
  nav_menu.classList.toggle("active");
  off_screen_menu.classList.toggle("active");
});

// checkbox event : main
checkButton.addEventListener("click", ()=>{

  if (checkButton.checked == true){
    parentForm.classList.add("active");
  } else {
    parentForm.classList.remove("active");
  }

})
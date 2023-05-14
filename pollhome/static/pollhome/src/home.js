const bar1 = document.querySelector(".bar1");
const bar2 = document.querySelector(".bar2");
let count = document.getElementsByClassName("textdisplay");

bar1.style.height = count[0].innerText;
bar2.style.height = count[1].innerText;

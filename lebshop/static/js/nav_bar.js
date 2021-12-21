function toggleNavBar(element) {
  let my_nav = document.getElementsByTagName("nav")[0];
  let navCont = document.getElementsByClassName("my_nav-flex-cont")[0];
  let body = document.getElementsByTagName("body")[0];

  if (element.value == "on") {
    navCont.style.overflow = "visible";
    my_nav.style.left = "0";
    my_nav.style.zIndex = "9999999999";
    my_nav.style.overflow = "visible";
    element.value = "off";
    body.style.overflow = "hidden";
  } else {
    my_nav.style.zIndex = "-9999";
    my_nav.style.left = "120%";
    body.style.overflow = "visible";
    my_nav.style.overflow = "hidden";
    setTimeout(() => {
      navCont.style.overflow = "hidden";
    }, 100);
    element.value = "on";
  }
}
function expandShop() {
  let shopItems = document.getElementsByClassName("shop-link-items-cont")[0];

  if (screen.width <= 768) {
    if (shopItems.style.maxHeight != "2000px") {
      shopItems.style.overflowY = "scroll";
      shopItems.style.maxHeight = "2000px";
      shopItems.style.height = "300px";
    } else {
      shopItems.style.maxHeight = "0";
      shopItems.style.height = "0";
      shopItems.style.overflowY = "hidden";
    }
  }
}
function expandUser() {
  let userItems = document.getElementsByClassName("user-menu-items")[0];

  if (screen.width <= 768) {
    if (userItems.style.maxHeight != "300px") {
      userItems.style.overflowY = "scroll";
      userItems.style.maxHeight = "300px";
      userItems.style.height = "100%";
    } else {
      userItems.style.maxHeight = "0";
      userItems.style.height = "0";
      userItems.style.overflowY = "hidden";
    }
  }
}

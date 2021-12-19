function toggleNavBar(element) {
  let my_nav = document.getElementsByTagName("nav")[0];
  // let my_nav_items = document.getElementsByClassName("my_nav-item");
  if (element.value == "on") {
    my_nav.style.top = "100%";
    my_nav.style.zIndex = "9999";
    element.value = "off";
    // for (let i = 0; i < my_nav_items.length; i++) {
    //   my_nav_items[i].style.zIndex = "999999999999";
    // }
  } else {
    my_nav.style.top = "-500%";
    my_nav.style.zIndex = "-9999";
    // for (let i = 0; i < my_nav_items.length; i++) {
    //   my_nav_items[i].style.zIndex = "-999999999999";
    // }
    element.value = "on";
  }
}
function expandShop() {
  let shopItems = document.getElementsByClassName("shop-link-items-cont")[0];

  if (screen.width <= 768) {
    if (shopItems.style.display != "block") {
      shopItems.style.display = "block";
    } else {
      shopItems.style.display = "none";
    }
  }
}

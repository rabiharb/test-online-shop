function checkValue(element) {
  if (element.value < 1) {
    element.value = 1;
  } else if (element.value > 9999) {
    element.value = 9999;
  }
  if (!Number.isInteger(element.value * 2)) {
    element.value = parseInt(element.value);
  }
  updatePrice(element.value);
}
function decreaseAmount() {
  let amountBox = document.getElementById("amountBox");
  if (amountBox.value > 1) {
    amountBox.value -= 0.5;
    updatePrice(amountBox.value);
  }
}
function increaseAmount() {
  let amountBox = document.getElementById("amountBox");
  if (amountBox.value < 9999) {
    if (!Number.isInteger(amountBox.value)) {
      amountBox.value = parseFloat(amountBox.value) + 0.5;
    } else {
      amountBox.value = parseInt(amountBox.value) + 0.5;
    }
    updatePrice(amountBox.value);
  }
}
function enterUpdate(event, input) {
  if (event.key == "Enter") {
    input.blur();
    updatePrice(input.value);
  } else {
    console.log(event.key);
  }
}

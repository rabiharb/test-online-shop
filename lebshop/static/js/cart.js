function checkValue(element, index) {
  if (element.value < 1) {
    element.value = 1;
  } else if (element.value > 9999) {
    element.value = 9999;
  }
  if (!Number.isInteger(element.value * 2)) {
    element.value = parseInt(element.value);
  }
  updatePrice(element.value, index - 1);
}
function decreaseAmount(index) {
  let amountBox = document.getElementsByClassName("amount-box")[index - 1];
  if (amountBox.value > 1) {
    amountBox.value -= 0.5;
    amountBox.value = parseFloat(amountBox.value);
    updatePrice(amountBox.value, index - 1);
  }
}
function increaseAmount(index) {
  let amountBox = document.getElementsByClassName("amount-box")[index - 1];
  if (amountBox.value < 9999) {
    if (!Number.isInteger(amountBox.value)) {
      amountBox.value = parseFloat(amountBox.value) + 0.5;
    } else {
      amountBox.value = parseInt(amountBox.value) + 0.5;
    }
    updatePrice(amountBox.value, index - 1);
  }
}
function enterUpdate(event, input, index) {
  if (event.key == "Enter") {
    input.blur();
    updatePrice(input.value, index - 1);
  }
}

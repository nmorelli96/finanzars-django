document.addEventListener("DOMContentLoaded", function() {
  const fiatHoraHeader = document.querySelector('.fiat-hora-header');
  const new_element = document.createElement('th');
  const formattedHora = hora.substring(11, 16);
  new_element.classList = fiatHoraHeader.classList
  new_element.scope = "col"
  new_element.innerHTML = `<a>${formattedHora}</a>`;
  new_element.title = hora
  fiatHoraHeader.parentNode.replaceChild(new_element, fiatHoraHeader);
});

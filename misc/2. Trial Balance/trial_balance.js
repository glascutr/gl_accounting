
function printTable() {
  let printContents = document.getElementById("print-area").innerHTML;
  let originalContents = document.body.innerHTML;

  document.body.innerHTML = printContents;
  window.print();
  document.body.innerHTML = originalContents;

  location.reload();
}

